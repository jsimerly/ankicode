from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.query import QuerySet
from graphql_api import get_new_question
from .models import *

# Create your views here.
class NextStudy(APIView):
    def get(self, request):
        most_recent_question = Question.objects.order_by('-date').first()
        ordered_categories = Category.objects.order_by('-current_score')[:2]

        if most_recent_question.category != ordered_categories.first():
            category = ordered_categories.first()
        else:
            category = ordered_categories.last()

        difficulty = 'easy'
        if category.current_score > 1000:
            difficulty == 'hard'
        elif category.current_score > 500:
            difficulty == 'medium'

        question_link = get_new_question(difficulty=difficulty)
        #will return name of question too
        return Response(
            {'question_link': question_link},
            status=status.HTTP_200_OK, 
        )
        
class CompleteQuestion(APIView):
    def post(self, request):
        name = request.data.get('name')
        link = request.data.get('link')
        difficulty = request.data.get('difficulty')
        answer_quality = request.data.get('answer_quality')
        category_str = request.data.get('category')

        category = Category.objects.get(name=category_str)
        question = Question.objects.create(
            name=name,
            link=link,
            category=category,
            difficulty=difficulty,
            quality_of_answer=answer_quality,
        )

        category.update_current_score()

        return Response(status=status.HTTP_200_OK)






        


        
        

        




        

