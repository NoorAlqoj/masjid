from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Teacher, Student, Session, Attendance, MemorizationRecord
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = (
        "Adds dummy data for teachers, students, attendance, and memorization records"
    )

    def handle(self, *args, **options):
        # Clear existing data
        Attendance.objects.all().delete()
        MemorizationRecord.objects.all().delete()
        Session.objects.all().delete()
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        User.objects.filter(username__in=["enas", "sara", "haya"]).delete()

        # Create teachers
        teachers_data = [
            {
                "username": "enas",
                "first_name": "Enas",
                "last_name": "Ahmed",
                "email": "enas@example.com",
                "students": [
                    "Noor Abdullah Al-Saud",
                    "Fatima Mohammed Al-Qahtani",
                    "Aisha Ahmad Al-Harbi",
                ],
            },
            {
                "username": "sara",
                "first_name": "Sara",
                "last_name": "Mohammed",
                "email": "sara@example.com",
                "students": [
                    "Maryam Khalid Al-Otaibi",
                    "Layla Hassan Al-Ghamdi",
                    "Reem Sultan Al-Dossari",
                ],
            },
            {
                "username": "haya",
                "first_name": "Haya",
                "last_name": "Ali",
                "email": "haya@example.com",
                "students": [
                    "Sarah Fahad Al-Shammari",
                    "Amira Nasser Al-Mutairi",
                    "Hessa Turki Al-Subaie",
                ],
            },
        ]

        for teacher_data in teachers_data:
            # Create user
            user = User.objects.create_user(
                username=teacher_data["username"],
                email=teacher_data["email"],
                password="password123",
                first_name=teacher_data["first_name"],
                last_name=teacher_data["last_name"],
                is_staff=True,
            )

            # Create teacher profile
            teacher = Teacher.objects.create(user=user, phone_number="+966501234567")

            # Create students for this teacher
            for student_name in teacher_data["students"]:
                Student.objects.create(
                    full_name=student_name,
                    date_of_birth=date(2010, 1, 1),
                    phone_number=f"+96650{random.randint(1000000, 9999999)}",
                    teacher=teacher,
                )

        # Create some sessions and attendance records
        today = date.today()
        for i in range(0, 30, 2):  # Create 15 sessions
            session_date = today + timedelta(days=i)
            if session_date.weekday() in [1, 5]:  # Tuesday or Saturday
                session = Session.objects.create(date=session_date)

                # For each session, create attendance and memorization records for all students
                for student in Student.objects.all():
                    # Create attendance record (80% chance of being present)
                    is_present = random.random() < 0.8
                    Attendance.objects.create(
                        student=student, session=session, is_present=is_present
                    )

                    # Create memorization record if student was present
                    if is_present:
                        MemorizationRecord.objects.create(
                            student=student,
                            session=session,
                            pages_memorized=random.randint(
                                1, 5
                            ),  # Random number of pages between 1 and 5
                        )

        self.stdout.write(
            self.style.SUCCESS("Successfully added dummy data with real student names")
        )
