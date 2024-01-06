from rest_framework.exceptions import APIException


class QuestionNotForThisTest(APIException):
    """ошибка вызывается когда пользователь пытается назначить существующий вопрос к тесту, для которого он был создан"""

    status_code = 400
    default_detail = "Этот вопрос уже связан с другим тестом!"


class CantAddQuestionsForOthersTest(APIException):
    """ошибка вызывается когда пользователь пытается создать вопрос для теста, который ему не пренадлежит"""

    status_code = 403
    default_detail = "Вы не можете добавлять вопросы для тестов других пользователей"


class CantUpdateQuestionsForOthersTest(APIException):
    """ошибка вызывается когда пользователь пытается изменить вопрос теста, который ему не пренадлежит"""

    status_code = 403
    default_detail = "Вы не можете изменять вопросы тестов других пользователей"


class CantDeleteQuestionsForOthersTest(APIException):
    """ошибка вызывается когда пользователь пытается удалить вопрос теста, который ему не пренадлежит"""

    status_code = 403
    default_detail = "Вы не можете удалять вопросы тестов других пользователей"


class QuestionWithNumberExists(APIException):
    status_code = 400
    default_detail = "Тест с таким номером уже существует"


class IncorrectQuestionNumber(APIException):
    status_code = 400
    default_detail = "Некорректный номер вопроса"
