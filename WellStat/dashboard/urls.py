# dashboard/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import chatbot_response, patient_register_view, login_view
from .views import risk_assessment_view


from .views import (
    dashboard_overview,
    ai_bot_view,
    risk_assessment_view,
    registration_view,
    settings_view,
    logout_view,
)

urlpatterns = [
    path('', views.login_view, name='login'),
    path('chatbot-response/', chatbot_response, name='chatbot_response'),
    path('dashboard/', dashboard_overview, name='dashboard_overview'),
    path('ai-bot/', ai_bot_view, name='ai_bot'),
    path('risk-assessment/', risk_assessment_view, name='risk_assessment'),
    path('register/', registration_view, name='registration'),
    path('settings/', settings_view, name='settings'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', patient_register_view, name='registration'),
    path('api/risk-assessment/', views.api_risk_assessment, name='api_risk_assessment'),
    path('login/', login_view, name='login_view'),
]

    # ... other patterns ...

