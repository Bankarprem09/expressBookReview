from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Get enrollment for the current user and course
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
        
        # Create submission linked to enrollment
        submission = Submission.objects.create(enrollment=enrollment)
        
        choice_ids = request.POST.getlist('choice')
        for choice_id in choice_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    questions = Question.objects.filter(lesson__course=course)
    
    # Get selected choice IDs for the submission context
    selected_ids = submission.choices.values_list('id', flat=True)
    
    for question in questions:
        selected_choices = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)
        
        if set(selected_choices) == set(correct_choices):
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score,
        'selected_ids': selected_ids,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
