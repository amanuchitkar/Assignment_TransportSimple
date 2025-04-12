from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Answer
from .forms import UserRegisterForm, QuestionForm, AnswerForm

def home(request):
    questions = Question.objects.all()
    return render(request, 'qanda/home.html', {'questions': questions})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'qanda/register.html', {'form': form})

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qanda/question_form.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    
    # Answer form handling
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        answer_form = AnswerForm()
    
    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
    }
    return render(request, 'qanda/question_detail.html', context)

@login_required
def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.likes.filter(id=request.user.id).exists():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return HttpResponseRedirect(reverse('question_detail', args=[answer.question.id]))
