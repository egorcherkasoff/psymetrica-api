from rest_framework.exceptions import APIException


# custom exceptions
class CantAssignTests(APIException):
    status_code = 403
    default_detail = "You cant assign tests to other users."


class CantAssignTestsForYourself(APIException):
    status_code = 403
    default_detail = "You cant assign tests to yourself."


class NotYourTest(APIException):
    status_code = 403
    default_detail = "You cannot assign tests created by other users."
