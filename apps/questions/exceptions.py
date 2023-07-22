from rest_framework.exceptions import APIException


class QuestionNotForThisTest(APIException):
    status_code = 400
    default_detail = "This question is already associated with another test!"


class CantAddQuestionsForOthersTest(APIException):
    status_code = 403
    default_detail = "You cant add questions to other user's tests"


class CantUpdateQuestionsForOthersTest(APIException):
    status_code = 403
    default_detail = "You cant update questions for other user's tests"


class CantDeleteQuestionsForOthersTest(APIException):
    status_code = 403
    default_detail = "You cant delete questions for other user's tests"


class QuestionWithNumberExists(APIException):
    status_code = 400
    default_detail = "Question with this number already exists"
