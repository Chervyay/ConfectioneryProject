from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
import re


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]{3,80}\Z'
    message = _('Введите корректный логин: от 3 до 80 символов; только буквы, цифры и символы: \"@ . + - _\".')


@deconstructible
class CustomFirstNameValidator(validators.RegexValidator):
    regex = r'[\w\-^\d_]{1,80}\Z'
    message = _('Введите корректное имя: от 1 до 80 символов; только буквы и символы \"-\".')
    flags = re.U


@deconstructible
class CustomLastNameValidator(validators.RegexValidator):
    regex = r'^[\w\-^\d_]{1,80}\Z'
    message = _('Введите корректную фамилию: от 1 до 80 символов только буквы и символы \"-\".')
    flags = re.U


@deconstructible
class CustomPatronymicValidator(validators.RegexValidator):
    regex = r'^[\w^\d_]{1,80}\Z'
    message = _('Введите корректное отчество: от 1 до 80 символов; только буквы.')
    flags = re.U


@deconstructible
class CustomTagValidator(validators.RegexValidator):
    regex = r'^[\w\s_"]{1,30}\Z'
    message = _('Введите корректный тег: от 1 до 30 символов; только буквы, цифры, пробелы и символы \"_\".')
    flags = re.U


@deconstructible
class CustomIngredientValidator(validators.RegexValidator):
    regex = r'^.{1,80}\Z'
    message = _('Введите корректное наименование ингредиента: от 1 до 80 символов; любые символы юникода.')
    flags = re.U


@deconstructible
class CustomMeasureValidator(validators.RegexValidator):
    regex = r'^.{1,80}\Z'
    message = _('Введите корректную меру ингредиента: от 1 до 30 символов; любые символы юникода.')
    flags = re.U