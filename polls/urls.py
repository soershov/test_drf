from django.urls import path
from . import apiviews

urlpatterns = [
        path('', apiviews.polls_view, name='polls_view'),
        path('<int:poll_id>/', apiviews.poll_detail_view, name='poll_detail_view'),
	path('questions/', apiviews.questions_view, name='questions_view'),
        path('questions/<int:question_id>/', apiviews.question_detail_view, name='question_detail_view'),
        path('questions/<int:question_id>/choices/', apiviews.choices_view, name='choices_view'),
        path('questions/<int:question_id>/vote/', apiviews.vote_view, name='vote_view'),
        path('questions/<int:question_id>/result/', apiviews.question_result_view, name='question_result_view'),
]

