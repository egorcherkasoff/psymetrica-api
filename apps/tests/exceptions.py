from rest_framework.exceptions import APIException


# custom exceptions
class CantAssignTests(APIException):
    """ошибка вызывается когда вы пытаетесь назначить тест другому пользователю не состоя в опред. группах"""

    status_code = 403
    default_detail = "Вы не можете назначать тесты другим пользователям"


class CantAssignTestsForYourself(APIException):
    """ошибка вызывается когда вы пытаетесь назначить тест самому себе"""

    status_code = 403
    default_detail = "Вы не можете назначить тест самому себе."


class NotYourTest(APIException):
    """ошибка вызывается когда вы пытаетесь назначить тест другому пользователю не имея доступ к его изменению"""

    status_code = 403
    default_detail = "Вы не можете назначить тест, который вам не пренадлежит."
