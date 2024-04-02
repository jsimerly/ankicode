from __future__ import annotations
from django.db import models
from django.core.validators import URLValidator
import numpy as np
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    n_questions = models.PositiveIntegerField()
    n_attempts = models.PositiveIntegerField()

    def get_current_score(self) -> float:
        all_questions = self.question_set.all()
        if len(all_questions) == 0:
            return 0
        
        N = np.log(len(all_questions))
        K = 2 / (N + 1)
        ema = all_questions[0]

        for question in all_questions:
            ema = question.score + ema( * (1-K))
        return ema

class Question(models.Model):
    DIFFICULTY_OPTIONS = (
        ('E', "Easy"),
        ('M', "Medium"),
        ('H', "Hard")
    )
    QUALITY_OPTIONS = (
        (0, 'Blackout'),
        (1, 'Attempted, little progress.'),
        (2, 'Attempted, close but needed more.'),
        (3, 'Correct, but with a lot of difficulty.'),
        (4, 'Correct, but with some syntax errors.'),
        (5, 'Correct, with no difficulities.')
    )

    name = models.CharField(max_length=256, blank=False, null=False)
    link = models.TextField(validators=[URLValidator()])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_OPTIONS)
    quality_of_answer = models.PositiveIntegerField(choices=QUALITY_OPTIONS)
    score = models.FloatField()

    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if any([
            'force_insert' in kwargs,
            'force_update' in kwargs,
            self._state.adding,
            self.score is None,
            self.pk is None
        ]):
            difficulty_map = {
                'E' : 100,
                'M': 300,
                'H': 1000,
            }

            self.score = difficulty_map[self.difficulty] * self.quality_of_answer
            super(Question, self).save(*args, **kwargs)



