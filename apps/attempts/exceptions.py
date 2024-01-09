from rest_framework.exceptions import APIException


class CantAttemptDeletedTest(APIException):
    status_code = 403
    default_detail = "Вы не можете попытаться пройти удалённый тест"


class CantChangeFinishedAttempt(APIException):
    status_code = 403
    default_detail = "Вы не можете изменять завершенные попытки"


class CantUpdateAttempts(APIException):
    status_code = 403
    default_detail = "Вы не можете изменять попытки пользователей"


class CantAddAnswersForOthersAttempts(APIException):
    status_code = 403
    default_detail = "Вы не можете добавлять ответы попыткам других пользователей"


class CantViewAttemptForOthersTests(APIException):
    status_code = 403
    default_detail = "Вы не можете просматривать попытки других пользователей, если вы не создать теста."
