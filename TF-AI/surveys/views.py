from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Question, Answer
from .forms import AnswerForm


def survey_list(request):
    surveys = Survey.objects.filter(is_active=True)
    return render(request, "surveys/list.html", {"surveys": surveys})


def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = request.POST.get("question_id")
            answer.save()
            return redirect("survey_detail", pk=survey.pk)
    else:
        form = AnswerForm()
    return render(request, "surveys/detail.html", {"survey": survey, "form": form})


def save_survey_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answer = Answer(question=question, text=request.POST.get("answer"))
    answer.save()
    return redirect("survey_list")
