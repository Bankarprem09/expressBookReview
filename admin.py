from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    search_fields = ['name', 'description']

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'course')

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'lesson')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
