from rest_framework.exceptions import APIException

class UnprocessableEntity(APIException):
    status_code = 406
    default_code = 406
    default_detail = 'unprocessable entity'

