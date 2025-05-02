from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(_("phone number"), max_length=15)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Student(models.Model):
    full_name = models.CharField(_("full name"), max_length=100)
    date_of_birth = models.DateField(_("date of birth"))
    phone_number = models.CharField(_("phone number"), max_length=15)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name="students",
        verbose_name=_("teacher"),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.full_name


class Session(models.Model):
    date = models.DateField(_("date"), unique=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return str(self.date)


class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name=_("student"),
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name=_("session"),
    )
    is_present = models.BooleanField(_("is present"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        unique_together = ("student", "session")
        verbose_name = _("attendance")
        verbose_name_plural = _("attendances")

    def __str__(self):
        return f"{self.student} - {self.session}"


class MemorizationRecord(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="memorization_records",
        verbose_name=_("student"),
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="memorization_records",
        verbose_name=_("session"),
    )
    pages_memorized = models.PositiveIntegerField(_("pages memorized"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        unique_together = ("student", "session")
        verbose_name = _("memorization record")
        verbose_name_plural = _("memorization records")

    def __str__(self):
        return f"{self.student} - {self.session} - {self.pages_memorized} pages"
