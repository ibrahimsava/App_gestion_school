from django.core.management.base import BaseCommand
from django.utils import timezone
from account.models import User, Student, Teacher, Parent
from academic.models import Subject, Class, Exam, ExamResult
from attendance.models import Attendance
from communications.models import Message, Announcement
from fees.models import FeeStructure, StudentFee, Payment
from librairy.models import Book, BookIssue
from timetables.models import Timetable
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with example data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate database...'))

        # Create Sample Subjects
        subjects = []
        subject_names = ['Mathematics', 'English', 'Science', 'History', 'Geography', 'Chemistry', 'Physics', 'Biology']
        for name in subject_names:
            subject, created = Subject.objects.get_or_create(
                name=name,
                defaults={'code': name[:3].upper(), 'description': f'{name} course'}
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'✓ Created Subject: {name}')

        # Create Sample Classes
        classes = []
        for level in [9, 10, 11, 12]:
            for section in ['A', 'B']:
                cls, created = Class.objects.get_or_create(
                    level=level,
                    section=section,
                    defaults={
                        'name': f'Class {level}{section}',
                        'code': f'CLS{level}{section}'
                    }
                )
                cls.subjects.set(random.sample(subjects, 5))
                classes.append(cls)
                if created:
                    self.stdout.write(f'✓ Created Class: Class {level}{section}')

        # Create Sample Teachers
        teacher_names = [
            ('John', 'Smith'), ('Sarah', 'Johnson'), ('Michael', 'Brown'),
            ('Emily', 'Davis'), ('Robert', 'Wilson'), ('Lisa', 'Anderson')
        ]
        teachers = []
        for i, (first, last) in enumerate(teacher_names):
            user, created = User.objects.get_or_create(
                username=f'teacher{i+1}',
                defaults={
                    'email': f'teacher{i+1}@school.com',
                    'first_name': first,
                    'last_name': last,
                    'user_type': 'teacher',
                    'phone': f'555000{i+1}',
                    'is_staff': True,
                    'is_active': True
                }
            )
            user.set_password('password123')
            user.save()

            teacher, created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': f'EMP00{i+1}',
                    'joining_date': timezone.now().date(),
                    'qualification': 'Bachelor\'s Degree'
                }
            )
            teacher.subjects.set(random.sample(subjects, 3))
            teachers.append(teacher)
            if created:
                self.stdout.write(f'✓ Created Teacher: {first} {last}')

        # Create Sample Parents
        parents = []
        parent_names = [
            ('James', 'Davis'), ('Patricia', 'Miller'), ('Christopher', 'Wilson'),
            ('Jennifer', 'Moore'), ('Daniel', 'Taylor'), ('Mary', 'Anderson')
        ]
        for i, (first, last) in enumerate(parent_names):
            user, created = User.objects.get_or_create(
                username=f'parent{i+1}',
                defaults={
                    'email': f'parent{i+1}@school.com',
                    'first_name': first,
                    'last_name': last,
                    'user_type': 'parent',
                    'phone': f'555100{i+1}'
                }
            )
            user.set_password('password123')
            user.save()

            parent, created = Parent.objects.get_or_create(
                user=user,
                defaults={'occupation': 'Professional'}
            )
            parents.append(parent)
            if created:
                self.stdout.write(f'✓ Created Parent: {first} {last}')

        # Create Sample Students
        students = []
        student_names = [
            ('Alice', 'Johnson'), ('Bob', 'Smith'), ('Charlie', 'Brown'),
            ('Diana', 'Davis'), ('Ethan', 'Wilson'), ('Fiona', 'Moore'),
            ('George', 'Taylor'), ('Hannah', 'Anderson'), ('Isaac', 'Thomas'),
            ('Julia', 'Jackson'), ('Kevin', 'White'), ('Laura', 'Harris')
        ]
        for i, (first, last) in enumerate(student_names):
            user, created = User.objects.get_or_create(
                username=f'student{i+1}',
                defaults={
                    'email': f'student{i+1}@school.com',
                    'first_name': first,
                    'last_name': last,
                    'user_type': 'student',
                    'phone': f'555200{i+1}'
                }
            )
            user.set_password('password123')
            user.save()

            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'admission_number': f'ADM2024{i+1:03d}',
                    'admission_date': timezone.now().date(),
                    'current_class': random.choice(classes),
                    'parent': random.choice(parents),
                    'blood_group': random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
                    'emergency_contact': f'555300{i+1}'
                }
            )
            students.append(student)
            if created:
                self.stdout.write(f'✓ Created Student: {first} {last}')

        # Create Sample Exams
        for cls in classes:
            for subject in cls.subjects.all()[:3]:
                exam, created = Exam.objects.get_or_create(
                    name=f'{subject.name} - {cls.name}',
                    defaults={
                        'exam_type': random.choice(['midterm', 'final', 'quiz']),
                        'class_obj': cls,
                        'subject': subject,
                        'exam_date': timezone.now().date() + timedelta(days=random.randint(5, 30)),
                        'exam_time': '10:00:00',
                        'total_marks': 100,
                        'passing_marks': 40,
                        'duration_minutes': 60
                    }
                )
                if created:
                    self.stdout.write(f'✓ Created Exam: {exam.name}')

        # Create Sample Exam Results
        for student in students[:6]:
            for exam in Exam.objects.all()[:3]:
                result, created = ExamResult.objects.get_or_create(
                    student=student,
                    exam=exam,
                    defaults={
                        'marks_obtained': random.randint(30, 100),
                        'percentage': random.uniform(30, 100)
                    }
                )
                if created:
                    self.stdout.write(f'✓ Created Exam Result for {student.user.first_name}')

        # Create Sample Books
        book_titles = [
            ('Mathematics: Advanced Concepts', 'Dr. Paul', '978-0-123456-78-9', 'Math', 2020),
            ('English Literature Classics', 'Prof. Emma', '978-0-234567-89-0', 'Literature', 2019),
            ('Modern Physics Guide', 'Dr. Newton', '978-0-345678-90-1', 'Science', 2021),
            ('World History Encyclopedia', 'Dr. Churchill', '978-0-456789-01-2', 'History', 2020),
            ('Geography of the Globe', 'Prof. Marco', '978-0-567890-12-3', 'Geography', 2021),
        ]
        books = []
        for title, author, isbn, category, year in book_titles:
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'publisher': 'Educational Press',
                    'publication_year': year,
                    'category': category,
                    'quantity': 10,
                    'available_quantity': 10,
                    'price': random.uniform(10, 50),
                    'book_shelf': f'A{random.randint(1, 5)}'
                }
            )
            books.append(book)
            if created:
                self.stdout.write(f'✓ Created Book: {title}')

        # Create Sample Fee Structures
        for cls in classes[:4]:
            for fee_type in ['Tuition', 'Exam Fee', 'Activity Fee']:
                fee_struct, created = FeeStructure.objects.get_or_create(
                    class_obj=cls,
                    fee_type=fee_type,
                    defaults={
                        'amount': random.choice([500, 1000, 1500, 2000]),
                        'due_date': (timezone.now() + timedelta(days=30)).date(),
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'✓ Created Fee Structure: {fee_type} for {cls.name}')

        # Create Sample Timetables
        for cls in classes[:4]:
            for day_num, day in enumerate(['monday', 'tuesday', 'wednesday', 'thursday', 'friday']):
                for hour in range(9, 14):
                    subject = random.choice(cls.subjects.all())
                    teacher = random.choice(teachers)
                    timetable, created = Timetable.objects.get_or_create(
                        class_obj=cls,
                        subject=subject,
                        day=day,
                        start_time=f'{hour:02d}:00:00',
                        defaults={
                            'teacher': teacher,
                            'end_time': f'{hour+1:02d}:00:00',
                            'room_number': f'R{hour}{day_num+1}'
                        }
                    )
                    if created:
                        self.stdout.write(f'✓ Created Timetable entry')

        # Create Sample Messages
        for i in range(5):
            sender = random.choice(teachers).user
            recipient = random.choice(students).user
            message, created = Message.objects.get_or_create(
                sender=sender,
                recipient=recipient,
                defaults={
                    'subject': f'Important Notice {i+1}',
                    'content': f'This is an important message regarding your academic progress. Please review your recent exam results and discuss any concerns with your teacher.',
                    'is_read': False
                }
            )
            if created:
                self.stdout.write(f'✓ Created Message')

        # Create Sample Announcements
        announcements_data = [
            ('School Closure Notice', 'The school will be closed on holidays. Please plan accordingly.'),
            ('Exam Schedule Released', 'Final exam schedule for all classes is now available. Check your dashboard.'),
            ('Sports Day Announcement', 'Annual sports day will be held next month. All students are encouraged to participate.'),
        ]
        for title, content in announcements_data:
            announcement, created = Announcement.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'priority': random.choice(['low', 'medium', 'high']),
                    'created_by': random.choice(teachers).user,
                    'published_date': timezone.now().date(),
                    'expire_date': (timezone.now() + timedelta(days=30)).date()
                }
            )
            if created:
                self.stdout.write(f'✓ Created Announcement: {title}')

        self.stdout.write(self.style.SUCCESS('\n✓ Database populated successfully with example data!'))
        self.stdout.write(self.style.SUCCESS('\nSample Login Credentials:'))
        self.stdout.write(self.style.WARNING('Student: student1 / password123'))
        self.stdout.write(self.style.WARNING('Teacher: teacher1 / password123'))
        self.stdout.write(self.style.WARNING('Parent: parent1 / password123'))
