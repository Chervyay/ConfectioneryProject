from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]{3,80}\Z'
    message = _('Введите корректный логин: от 3 до 80 символов; только буквы, цифры и символы: \"@ . + - _\".')
    flags = 0


@deconstructible
class CustomFirstNameValidator(validators.RegexValidator):
    regex = r'^[A-Za-z-]+\Z'
    message = _('Введите корректное имя: от 1 до 80 символов; только буквы и символы \"-\".')
    flags = 0


@deconstructible
class CustomLastNameValidator(validators.RegexValidator):
    regex = r'^[A-Za-z-]+\Z'
    message = _('Введите корректную фамилию: от 1 до 80 символов только буквы и символы \"-\".')
    flags = 0


@deconstructible
class CustomPatronymicValidator(validators.RegexValidator):
    regex = r'^[A-Za-z]+\Z'
    message = _('Введите корректное отчество: от 1 до 80 символов; только буквы.')
    flags = 0


@deconstructible
class CustomEmailValidator(validators.EmailValidator):
    message = _('Введите корректный e-mail.')


@deconstructible
class CustomTagValidator(validators.RegexValidator):
    regex = r'^[\w]+\Z'
    message = _('Введите корректный тег: от 1 до 30 символов; только буквы, цифры и символы \"_\".')
    flags = 0


@deconstructible
class CustomFileFormatValidator(validators.RegexValidator):
    regex = r'^[a-z]+\Z'
    message = _('Введите корректное расширение файла: от 1 до 10 символов; только строчные буквы\"_\".')
    flags = 0