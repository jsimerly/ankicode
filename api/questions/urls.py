from django.urls import path
from .views import *

urlpatterns = [
    path('new-question/', NextStudy.as_view(), name='new_study'),
    path('answer-question', CompleteQuestion.as_view(), name='complete_q'), 
]