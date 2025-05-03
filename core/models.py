from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .choices import SURAH_CHOICES


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(_("phone number"), max_length=15)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    job = models.CharField(_("job"), max_length=100, null=True, blank=True)
    education = models.CharField(_("education"), max_length=100, null=True, blank=True)
    notes = models.TextField(_("notes"), null=True, blank=True)

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return f"{self.user.get_full_name()}"

    @property
    def age(self):
        if self.date_of_birth:
            return timezone.now().year - self.date_of_birth.year
        return None


class Student(models.Model):
    full_name = models.CharField(_("full name"), max_length=100)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    phone_number = models.CharField(
        _("phone number"), max_length=15, null=True, blank=True
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name=_("teacher"),
    )
    notes = models.TextField(_("notes"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        if self.date_of_birth:
            return timezone.now().year - self.date_of_birth.year
        return None


class Session(models.Model):
    date = models.DateField(_("date"), unique=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

    def __str__(self):
        return str(self.date)


# class Attendance(models.Model):
#     student = models.ForeignKey(
#         Student,
#         on_delete=models.CASCADE,
#         related_name="attendances",
#         verbose_name=_("student"),
#     )
#     session = models.ForeignKey(
#         Session,
#         on_delete=models.CASCADE,
#         related_name="attendances",
#         verbose_name=_("session"),
#     )
#     is_present = models.BooleanField(_("is present"), default=True)
#     created_at = models.DateTimeField(_("created at"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("updated at"), auto_now=True)

#     class Meta:
#         unique_together = ("student", "session")
#         verbose_name = _("attendance")
#         verbose_name_plural = _("attendances")

#     def __str__(self):
#         return f"{self.student} - {self.session}"


class MemorizationRecord(models.Model):
    LEVEL_CHOICES = [
        ("bad", _("Bad")),
        ("good", _("Good")),
        ("excellent", _("Excellent")),
    ]
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
    surah = models.CharField(
        _("Surah"),
        max_length=10,
        choices=SURAH_CHOICES,
        null=True,
        blank=True,
    )
    level = models.CharField(
        _("level"),
        max_length=100,
        choices=LEVEL_CHOICES,
        null=True,
        blank=True,
        default="good",
    )
    pages_memorized = models.PositiveIntegerField(_("pages memorized"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        unique_together = ("student", "session")
        verbose_name = _("Memorization record")
        verbose_name_plural = _("Memorization records")

    def __str__(self):
        return f"{self.student} - {self.session} - {self.pages_memorized} pages"
