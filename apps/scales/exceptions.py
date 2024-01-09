from rest_framework.exceptions import APIException


class CantAddScalesForOthersTests(APIException):
    default_detail = (
        "Вы не можете создавать шкалы для тестов которые не пренадлежат вам."
    )
    status_code = 403


class CantUpdateScalesForOthersTests(APIException):
    default_detail = (
        "Вы не можете обновлять шкалы для тестов которые не пренадлежат вам."
    )
    status_code = 403


class CantDeleteScalesForOthersTests(APIException):
    default_detail = "Вы не можете удалять шкалы для тестов которые не пренадлежат вам."
    status_code = 403


class CantViewScalesForOthersTest(APIException):
    default_detail = "Вы не можете просматривать шкалы для тестов других пользователей."
    status_code = 403
