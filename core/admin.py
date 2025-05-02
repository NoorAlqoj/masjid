from unfold.admin import ModelAdmin
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from django.contrib.auth import admin as auth_admin

from .models import Teacher, Student, Session, Attendance, MemorizationRecord
from django.db.models import Count, Sum, Avg
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.db.models import Q

from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
# from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin
# from django.contrib.sites.models import Site
admin.site.unregister(Group)
# admin.site.unregister(Site)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# @admin.register(Site)
# class SiteAdmin(BaseSiteAdmin, ModelAdmin):
#     pass
class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = "Teacher"


@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ("user", "phone_number", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    date_hierarchy = "created_at"


class CustomUserAdmin(UserAdmin, ModelAdmin):
    # inlines = (TeacherInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ("full_name", "date_of_birth", "phone_number", "teacher")
    list_filter = ("teacher",)
    search_fields = ("full_name", "phone_number")
    date_hierarchy = "date_of_birth"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is not a superuser, filter to show only their students
        if not request.user.is_superuser:
            try:
                teacher = Teacher.objects.get(user=request.user)
                return qs.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                return Student.objects.none()
        return qs

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            try:
                teacher = Teacher.objects.get(user=request.user)
                if obj and obj.teacher != teacher:
                    return False
            except Teacher.DoesNotExist:
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            try:
                teacher = Teacher.objects.get(user=request.user)
                if obj and obj.teacher != teacher:
                    return False
            except Teacher.DoesNotExist:
                return False
        return super().has_delete_permission(request, obj)


@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ("date", "created_at")
    date_hierarchy = "date"
    ordering = ("-date",)


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = ("student", "session", "is_present")
    list_filter = ("is_present", "session", "student__teacher")
    search_fields = ("student__full_name",)
    date_hierarchy = "session__date"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            try:
                teacher = Teacher.objects.get(user=request.user)
                return qs.filter(student__teacher=teacher)
            except Teacher.DoesNotExist:
                return Attendance.objects.none()
        return qs


@admin.register(MemorizationRecord)
class MemorizationRecordAdmin(ModelAdmin):
    list_display = ("student", "session", "pages_memorized")
    list_filter = ("session", "student__teacher")
    search_fields = ("student__full_name",)
    date_hierarchy = "session__date"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            try:
                teacher = Teacher.objects.get(user=request.user)
                return qs.filter(student__teacher=teacher)
            except Teacher.DoesNotExist:
                return MemorizationRecord.objects.none()
        return qs


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class StatisticsAdmin(ModelAdmin):
    change_list_template = "admin/statistics.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "statistics/",
                self.admin_site.admin_view(self.statistics_view),
                name="statistics",
            ),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        # Get filter parameters
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        teacher_id = request.GET.get("teacher")
        student_id = request.GET.get("student")
        month = request.GET.get("month")

        # Base queryset
        attendance_qs = Attendance.objects.all()
        memorization_qs = MemorizationRecord.objects.all()

        # Apply filters
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            attendance_qs = attendance_qs.filter(session__date__gte=start_date)
            memorization_qs = memorization_qs.filter(session__date__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            attendance_qs = attendance_qs.filter(session__date__lte=end_date)
            memorization_qs = memorization_qs.filter(session__date__lte=end_date)

        if teacher_id:
            attendance_qs = attendance_qs.filter(student__teacher_id=teacher_id)
            memorization_qs = memorization_qs.filter(student__teacher_id=teacher_id)

        if student_id:
            attendance_qs = attendance_qs.filter(student_id=student_id)
            memorization_qs = memorization_qs.filter(student_id=student_id)

        if month:
            month = datetime.strptime(month, "%Y-%m").date()
            next_month = (month.replace(day=1) + timedelta(days=32)).replace(day=1)
            attendance_qs = attendance_qs.filter(
                session__date__gte=month, session__date__lt=next_month
            )
            memorization_qs = memorization_qs.filter(
                session__date__gte=month, session__date__lt=next_month
            )

        # Calculate statistics
        total_sessions = Session.objects.count()
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()

        # Attendance statistics
        attendance_stats = attendance_qs.values(
            "student__full_name", "student__teacher__user__first_name"
        ).annotate(
            total_sessions=Count("session", distinct=True),
            present_sessions=Count("session", filter=Q(is_present=True), distinct=True),
            attendance_rate=Avg("is_present") * 100,
        )

        # Memorization statistics
        memorization_stats = memorization_qs.values(
            "student__full_name", "student__teacher__user__first_name"
        ).annotate(
            total_pages=Sum("pages_memorized"), average_pages=Avg("pages_memorized")
        )

        # Combine statistics
        combined_stats = []
        for att in attendance_stats:
            mem = next(
                (
                    m
                    for m in memorization_stats
                    if m["student__full_name"] == att["student__full_name"]
                ),
                None,
            )
            combined_stats.append(
                {
                    "student_name": att["student__full_name"],
                    "teacher_name": att["student__teacher__user__first_name"],
                    "total_sessions": att["total_sessions"],
                    "present_sessions": att["present_sessions"],
                    "attendance_rate": round(att["attendance_rate"], 2),
                    "total_pages": mem["total_pages"] if mem else 0,
                    "average_pages": round(mem["average_pages"], 2) if mem else 0,
                }
            )

        context = {
            "title": "Statistics",
            "total_sessions": total_sessions,
            "total_students": total_students,
            "total_teachers": total_teachers,
            "statistics": combined_stats,
            "teachers": Teacher.objects.all(),
            "students": Student.objects.all(),
            "months": Session.objects.dates("date", "month"),
        }
        return render(request, "admin/statistics.html", context)


# Register the statistics view
# admin.site.register(StatisticsAdmin)
