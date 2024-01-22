from typing import Any
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from apps.tests.models import Test
from apps.questions.models import Question
import secrets
from apps.options.models import (
    Option,
    OptionScore,
    TextOption,
    ImageOption,
    RangeOption,
)


User = get_user_model()


def create_question(test, idx):
    """создает вопрос"""
    if idx == 0:
        type = Question.QuestionTypes.SINGLE_OPTION
    else:
        type = Question.QuestionTypes.RANGE
    question = Question.objects.create(
        test=test, number=idx, text=f"Текст вопроса {idx}", type=type
    )
    question.save()
    return question


def create_option(question):
    """создает вариант ответа"""
    for idx in range(1):
        option = Option.objects.create(
            question=question,
            number=idx,
        )
        if question.type == Question.QuestionTypes.SINGLE_OPTION:
            s = TextOption.objects.create(
                option=option,
                text="Текст варианта ответа",
            )
            s.save()
        elif question.type == Question.QuestionTypes.RANGE:
            s = RangeOption.objects.create(option=option, min_range=0, max_range=5)
            s.save()
        os = OptionScore.objects.create(option=option, score=1)
        os.save()


def create_user():
    """создает пользователя"""
    user = User.objects.create_user(
        email="sample@psymetrica.ru", password=secrets.token_hex(16)
    )
    user.save()
    return user


def create_test(title, user):
    """создает тест"""
    test = Test.objects.create(
        title=title,
        author=user,
    )
    test.save()
    questions = []
    for idx in range(1):
        question = create_question(test, idx)
        questions.append(question)
    for question in questions:
        create_option(question)


class Command(BaseCommand):
    """Создает команду для manage.py - "prepopulate",
    которая заполнит бд начальными данными (необязательно это делать)"""

    help = "Заполняет БД шаблонными данными"

    def handle(self, *args, **options):
        self.stdout.write("Заполняем БД начальными данными...")
        user = create_user()
        create_test("Тест 1", user)
        create_test("Тест 2", user)
        self.stdout.write("Заполнение завершено")
