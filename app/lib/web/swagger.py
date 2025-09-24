from app.lib.web.models import ErrorResponse
from app.lib.web import exeptions

jwt_unauthorized_responses = {
    401: {
        "model": ErrorResponse,
        "description": "Unauthorized - ошибка авторизации JWT",
        "content": {
            "application/json": {
                "examples": {
                    "missing_token": {
                        "summary": "Token отсутствует",
                        "value": {
                            "detail": exeptions.JWT_MISSING_TOKEN.detail,
                        },
                    },
                    "expired": {
                        "summary": "Истёк срок действия",
                        "value": {
                            "detail": exeptions.JWT_TOKEN_EXPIRED.detail,
                        },
                    },
                    "bad_credentials": {
                        "summary": "Некорректные данные",
                        "value": {
                            "detail": exeptions.JWT_BAD_CREDENSIALS.detail,
                        },
                    },
                    "refresh_not_found": {
                        "summary": "Refresh-токен не найден в БД",
                        "value": {
                            "detail": exeptions.REFRESH_TOKEN_NOT_FOUND.detail,
                        },
                    },
                    "decode_error": {
                        "summary": "Ошибка при декодировании JWT",
                        "value": {
                            "detail": exeptions.JWT_DECODE_ERROR.detail,
                        },
                    },
                }
            }
        },
    }
}

auth_unauthorized_responses = {
    401: {
        "model": ErrorResponse,
        "description": "Unauthorized – ошибка авторизации",
        "content": {
            "application/json": {
                "examples": {
                    "bad_credentials": {
                        "summary": "Некорректные данные",
                        "value": {
                            "detail": exeptions.BAD_CREDENSIALS.detail,
                        },
                    },
                    "user_not_found": {
                        "summary": "Пользователь не найден",
                        "value": {
                            "detail": exeptions.USER_NOT_FOUND.detail,
                        },
                    },
                }
            }
        },
    }
}
