from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)

class Course(models.Model):
    no = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    credit = models.DecimalField(max_digits=1, decimal_places=1)
    year = models.CharField(max_length=30)
    semester = models.CharField(max_length=4)
    department = models.CharField(max_length=40)
    active = models.BooleanField(default=False)
class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name



# Define Teacher Model
class Teacher(models.Model):
    # Define the fileds
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    # current_courses = models.OneTo(Course, through='')
    # past_course = models.OneToOneField(Course,)
class Student(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name         = models.CharField(max_length=100, default="")
    session_begin      =models.CharField(max_length=4,validators=[RegexValidator(r'^\d{1,10}$')],default="")
    session_end = models.CharField(max_length=2,validators=[RegexValidator(r'^\d{1,10}$')],default="")
    year = models.CharField(max_length=30,default="")
    semester = models.CharField(max_length=4,default="")
    department = models.CharField(max_length=40, default="")
    reg_no       = models.CharField(max_length=10,validators=[RegexValidator(r'^\d{1,10}$')],default="")
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    # def get_unanswered_questions(self, quiz):
    #     answered_questions = self.quiz_answers \
    #         .filter(answer__question__quiz=quiz) \
    #         .values_list('answer__question__pk', flat=True)
    #     questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
    #     return questions

    def __str__(self):
        return self.user.username

class Survey(models.Model):
    # Related names had to be added
    answered_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    asked_by = models.ForeignKey(Teacher,on_delete= models.CASCADE)
    


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text

    
# Define Staff Model
class Staff(models.Model):
    # Define the fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 100)
    department = models.CharField(max_length = 30)

class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
