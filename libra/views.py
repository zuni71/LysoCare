from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.db import models
from datetime import timedelta
import datetime
from django.core.exceptions import ValidationError

from .models import Question, Choice, Data, Answer, User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import plotly.express as px
import plotly.offline as opy
from django.db.models import Count

from .forms import MultipleChoiceQuestionForm


@login_required(login_url='/login/')
def homepage(request):
    
    return render(request, "libra/homepage.html")

def login(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            auth_login(request, user)

            next_url = request.POST.get('next') or request.GET.get('next') or 'homepage'
            return redirect(next_url)
    
    # Render the login page template (GET request)
    next_param = request.GET.get('next', '')
    return render(request, 'libra/login.html', {'next': next_param})

# Define a view function for the registration page
        

def register(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

         # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
    
    # Render the registration page template (GET request)
    return render(request, 'libra/register.html')

"""
@login_required(login_url='/login/')
def questionnaire(request):
    messages.info(request, "User authenticated!")
    questions = Question.objects.all()
    if request.method == 'POST':
        form = MultipleChoiceQuestionForm(questions, request.POST)
        if form.is_valid():
            from django.urls import reverse
            data_obj = Data.objects.create(
                user=request.user
                )
            return HttpResponseRedirect(reverse('questionnaire_details', kwargs={'data_id': data_obj.id}))

            for question in questions:
                
                answer_id = form.cleaned_data.get(question.id)

                Answer.objects.create(
                    data=data_obj,
                    question=question,
                    choice_id=answer_id,
                    
                )
        
    
    else:
        form = MultipleChoiceQuestionForm(questions)
    return render(request, "libra/questionnaire.html", {"form": form})
"""
@login_required(login_url='/login/')
def questionnaire_details(request, data_id):
    data = get_object_or_404(Data, id=data_id)
    
    question = Question.objects.get(id=data.question.id)
    answer = Answer.objects.filter(question=question) \
                    .values('choice__choice_text') \
                    .annotate(count=Count('choice')) \
                    .order_by('choice__choice_text')
    answer_counts = list(answer)
    import pandas as pd
    choices = [item['choice__choice_text'] for item in answer_counts]
    counts = [item['count'] for item in answer_counts]

    df = pd.DataFrame({
        'choice': choices,
        'count': counts
        })
    fig = px.bar(df, x='choice', y='count', title=f'Responses to: Has an ECG shown any new heart abnormalities or arrhythmias?')
    fig.update_layout(xaxis_title='Scale', yaxis_title='Frequency')

    plot_div = opy.plot(fig, output_type='div', include_plotlyjs=True)
    answers = Answer.objects.filter(data=data).select_related('question', 'choice')
    answers_data = []
    for answer in answers:
        answers_data.append({
            'question': answer.question.question_text,
            'choice': answer.choice.choice_text})
        context = {
            "data": data,
            "answers": answers_data,
            'plot_div': plot_div}
    return render(request, "libra/questionnaire_details.html", context)
def questionnaire_details_latest(request):
    latest_data = Data.objects.order_by('-id').first()  # Or whatever sorting logic you need
    if latest_data:
        return redirect('questionnaire_details', data_id=latest_data.id)
    else:
        # Handle case where no data exists
        return redirect("no_details_page")

def no_details_page(request):
    return render(request, "libra/no_details_page.html")
def questionnaire(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        form = MultipleChoiceQuestionForm(questions, request.POST)
        if form.is_valid():
            try:
                data_obj = form.save()
                for question in questions:
                    answer_id = form.cleaned_data.get(f"question_{question.id}")
                    if answer_id is None:  # Validate each answer exists
                        form.add_error(None, f"Missing answer for question: {question}")
                        raise ValueError("All questions must be answered")
                    Answer.objects.create(
                        data=data_obj,
                        question=question,
                        choice_id=answer_id,
                        
                    )

                return redirect('questionnaire_details', data_id=data_obj.id)
            except ValidationError as e:
                form.add_error(None, str(e))
    
    else:
        form = MultipleChoiceQuestionForm(questions)
    return render(request, "libra/questionnaire.html", {"form": form})


