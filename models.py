from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=100, default='online course')
    description = models.CharField(max_length=500)
    pub_date = models.DateField(null=True)

    def __str__(self):
        return self.name

# Lesson Model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

# Question Model
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.TextField()
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True)
        selected_choices = all_answers.filter(id__in=selected_ids)
        if all_answers.count() == selected_choices.count() and all_answers.count() == len(selected_ids):
            return True
        return False

# Choice Model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

# Submission Model
class Submission(models.Model):
    enrollment = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # or Enrollment model depending on structure
    choices = models.ManyToManyField(Choice)
