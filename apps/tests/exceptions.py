from rest_framework.exceptions import APIException


class CantAssignTestsForYourself(APIException):
    """ошибка вызывается когда вы пытаетесь назначить тест самому себе"""

    status_code = 403
    default_detail = "Вы не можете назначить тест самому себе."
