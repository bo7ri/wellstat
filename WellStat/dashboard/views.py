from django.shortcuts import render

# Create your views here.
# dashboard/views.py
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
import requests

from openai import OpenAI
from .forms import PatientRegistrationForm

import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
)


def fetch_covid_variant_data():
    url = "https://data.cdc.gov/resource/jr58-6ysp.json"
    response = requests.get(url)
    data = response.json()

    # Process and structure the data as needed for the chart
    # For instance, you might want to sort it by date and group by variant
    structured_data = {}
    for entry in data:
        variant = entry['variant']
        date = entry['published_date']
        share_hi = float(entry['share_hi'])

        if date not in structured_data:
            structured_data[date] = {}
        structured_data[date][variant] = share_hi

    return structured_data


def covid_trends_view(request):
    covid_data = fetch_covid_variant_data()
    # Prepare the data for the template (convert to lists, order by date, etc.)
    context = {
        'covid_data': covid_data
    }
    return render(request, 'dashboard/overview.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get() to avoid MultiValueDictKeyError
        password = request.POST.get('password')

        if not username or not password:
            # Handle missing username or password
            return render(request, 'dashboard/login.html', {'error': 'Please enter both username and password'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_overview')  # Redirect to your dashboard overview page
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'dashboard/login.html')


@login_required
def dashboard_overview(request):
    # You might want to pass some context to the dashboard template.
    # For example, user data, recent activity, etc.
    context = {
        'user': request.user,
        # Add more context data here
    }
    return render(request, 'dashboard/overview.html', context)


@login_required
def ai_bot_view(request):
    # Placeholder for the AI Chatbot view
    return render(request, 'dashboard/ai_bot.html')


@login_required
def risk_assessment_view(request):
    # Placeholder for the Risk Assessment view
    return render(request, 'dashboard/risk_assessment.html')


@login_required
def registration_view(request):
    # Placeholder for the Registration view
    return render(request, 'dashboard/registration.html')


@login_required
def settings_view(request):
    # Placeholder for the Settings view
    return render(request, 'dashboard/settings.html')


def logout_view(request):
    # Logout the user and redirect to the login page
    logout(request)
    return render(request, 'dashboard/login.html')


def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and knowledgeable medical assistant called WellGPT"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:  # Update this to catch specific exceptions if possible
        return str(e)


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = request.POST
        user_prompt = data.get('prompt')
        chat_response = get_openai_response(user_prompt)
        return JsonResponse({'response': chat_response})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def patient_register_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some_success_url')
    else:
        form = PatientRegistrationForm()

    # Make sure 'form' is correctly passed to the template context
    return render(request, 'dashboard/registration.html', {'form': form})


@csrf_exempt
@require_http_methods(["POST"])
def api_risk_assessment(request):
    try:
        data = json.loads(request.body)
        patient_info = data.get('patient_info')

        # Use GPT to generate a risk assessment based on the patient_info
        gpt_response = get_openai_responses(patient_info)

        # Process the response to structure it in a JSON format for a risk assessment
        risk_assessment = process_gpt_response(gpt_response)

        # Return the risk assessment in JSON format
        return JsonResponse({
            'status': 'success',
            'patient_info': patient_info,
            'risk_assessment': risk_assessment
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_openai_responses(prompt):
    # Use OpenAI API to get a response based on the patient information
    response = openai.Completion.create(
        {"role": "system", "content": "You are a helpful and knowledgeable medical assistant called WellGPT"},
        {"role": "user", "content": prompt}
    )
    return response.choices[0].text.strip()


def process_gpt_response(response):
    # Process the GPT response to extract risk factors and create a risk assessment
    # This is a placeholder function, implement according to your own logic
    return {
        'summary': response,
        'risk_score': 42  # Placeholder for an actual risk score calculation
    }


