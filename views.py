from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        choice_ids = request.POST.getlist('choice')
        submission = Submission.objects.create(enrollment=request.user) # Adjust based on enrollment relationship
        for choice_id in choice_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        
        return redirect('onlinecourse:exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    questions = Question.objects.filter(lesson__course=course)
    
    for question in questions:
        selected_choices = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)
        
        # Check if selected match correct choices exactly
        if set(selected_choices) == set(correct_choices):
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
