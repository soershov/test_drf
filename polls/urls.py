from django.urls import path
from . import apiviews

urlpatterns = [
	path('questions/', apiviews.questions_view, name='questions_view'),
]

