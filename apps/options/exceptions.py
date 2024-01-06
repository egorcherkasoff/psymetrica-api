from rest_framework.exceptions import APIException


class OptionNotForThisQuestion(APIException):
    status_code = 400
    default_detail = "Этот вариант ответа уже связан с другим вопросом!"


class IncorrectOptionNumber(APIException):
    status_code = 400
    default_detail = "Некорректный номер варианта ответа"


class OptionWithNumberExists(APIException):
    status_code = 400
    default_detail = "Вариант ответа с таким номером уже существует"


class IncorrectOptionType(APIException):
    status_code = 400
    default_detail = "Некорректный тип варианта ответа"


class CantDeleteOptionsForOthersTest(APIException):
    status_code = 403
    default_detail = "Вы не можете удалять варианты ответов других пользователей"


class CantUpdateOptionsForOthersTest(APIException):
    status_code = 403
    default_detail = "Вы не можете изменять варианты ответов других пользователей"


class CantAddOptionsForOthersTest(APIException):
    status_code = 403
    default_detail = "Вы не можете добавлять варианты ответов других пользователей"
