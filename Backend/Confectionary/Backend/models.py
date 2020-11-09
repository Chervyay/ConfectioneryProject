from django.db import models
from django.conf import settings
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from django.core.validators import MaxValueValidator
from .validators import *
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils import timezone
import transliterate


def client_avatar_upload_path(instance, filename):
    return '/'.join(['pictures', 'users', instance.username, 'avatar', filename])


def recipe_avatar_upload_path(instance, filename):
    return '/'.join(['pictures', 'users', instance.creator.username, 'recipes',
                     transliterate.translit(instance.title, reversed=True) + ' ('
                     + str(instance.id) + ')', 'avatar', filename])


def cook_stage_picture_upload_path(instance, filename):
    return '/'.join(['pictures', 'users', instance.recipe.creator.username, 'recipes',
                     transliterate.translit(instance.recipe.title, reversed=True) + ' ('
                     + str(instance.recipe.id) + ')', 'cook stages', filename])


class ClientManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class Client(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    username = models.CharField(max_length=80, unique=True, validators=[CustomUsernameValidator()],
                                error_messages={
                                    'unique': _("Введённый логин занят другим пользователем."),
                                }, verbose_name='Логин')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    email = models.EmailField(unique=True,
                              error_messages={
                                    'unique': _("Пользователь с введённой почтой уже зарегистрирован в системе."),
                              }, null=True, verbose_name='Почта')
    first_name = models.CharField(max_length=80, validators=[CustomFirstNameValidator()], blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=80, validators=[CustomLastNameValidator()], blank=True,
                                 verbose_name='Фамилия')
    patronymic = models.CharField(max_length=80, validators=[CustomPatronymicValidator()], blank=True,
                                  verbose_name='Отчество')
    avatar = models.ImageField(upload_to=client_avatar_upload_path, max_length=100, blank=True, verbose_name='Аватарка')
    is_staff = models.BooleanField(default=False, verbose_name='Служебный аккаунт')
    status_vars = (
        ('A', 'Активен'),
        ('B', 'Заблокирован'),
    )
    status = models.CharField(max_length=3, choices=status_vars, default='A', verbose_name='Статус активности')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Последнее подключение')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Дата создания аккаунта')

    objects = ClientManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    default_avatar = '/media/pictures/default/client_default.jpg'

    def try_get_avatar(self):
        try:
            avatar_got = self.avatar.url
            if os.path.exists(settings.BASE_DIR + avatar_got):
                return avatar_got
            else:
                self.avatar = ''
                self.save()
                raise ValueError
        # в случае, если URL некорректный, или в системе не существует путь
        except ValueError:
            return self.default_avatar


class Recipe(models.Model):
    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='recipes',
                                verbose_name='Рецепт')
    title = models.CharField(max_length=100, default='', verbose_name='Наименование')

    portions = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], blank=True, null=True,
                                                verbose_name='Количество порций')
    cook_time = models.PositiveIntegerField(validators=[MaxValueValidator(1440)], blank=True, null=True,
                                            verbose_name='Время приготовления')
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(1000000)], blank=True, null=True,
                                         verbose_name='Вес')
    avatar = models.ImageField(upload_to=recipe_avatar_upload_path, max_length=100, blank=True, verbose_name='Аватарка')
    status_vars = (
        ('A', 'В широком доступе'),
        ('B', 'Заблокировано'),
    )
    status = models.CharField(max_length=3, choices=status_vars, default='A', verbose_name='Статус')
    date_init = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    default_avatar = '/media/pictures/default/recipe_default.png'

    def try_get_avatar(self):
        try:
            avatar_got = self.avatar.url
            if os.path.exists(settings.BASE_DIR + avatar_got):
                return avatar_got
            else:
                self.avatar = ''
                self.save()
                raise ValueError
        except ValueError:
            return self.default_avatar


class CookStage(models.Model):
    class Meta:
        verbose_name = _('Этап приготовления')
        verbose_name_plural = _('Этапы приготовления')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='cook_stages', verbose_name='Рецепт')
    description = models.TextField(default='', max_length=500, verbose_name='Описание')
    picture = models.ImageField(upload_to=cook_stage_picture_upload_path, max_length=100, blank=True,
                                verbose_name='Изображение этапа')

    default_picture = '/media/pictures/default/cook_default.png'

    def try_get_picture(self):
        try:
            picture_got = self.picture.url
            if os.path.exists(settings.BASE_DIR + picture_got):
                return picture_got
            else:
                self.picture = ''
                self.save()
                raise ValueError
        except ValueError:
            return self.default_picture


class Ingredient(models.Model):
    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Рецепт')
    name = models.CharField(default='', max_length=80, validators=[CustomIngredientValidator()],
                            verbose_name='Наименование')
    measure = models.CharField(default='', max_length=30, validators=[CustomMeasureValidator()], verbose_name='Мера')


class Tag(models.Model):
    class Meta:
        verbose_name = _('Прикреплённый тег')
        verbose_name_plural = _('Прикреплённые теги')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='tags', verbose_name='Рецепт')
    name = models.CharField(max_length=30, default='', validators=[CustomTagValidator()],
                            verbose_name='Наименование')


class RecipeGrade(models.Model):
    class Meta:
        verbose_name = _('Оценка рецепта')
        verbose_name_plural = _('Оценки рецептов')
        unique_together = ('evaluator', 'recipe')

    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipe_grades',
                                  verbose_name='Оценивающий')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_grades', verbose_name='Рецепт')
    grade = models.BooleanField(default=True, verbose_name='Оценка')
    status_vars = (
        ('A', 'Активна'),
        ('B', 'Заблокирована'),
    )
    status = models.CharField(max_length=3, choices=status_vars, default='A', verbose_name='Статус')


class Comment(models.Model):
    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='comments',
                                verbose_name='Создатель')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='Рецепт')
    body = models.TextField(default='', verbose_name='Содержание')
    status_vars = (
        ('A', 'В широком доступе'),
        ('B', 'Заблокировано'),
    )
    status = models.CharField(max_length=3, choices=status_vars, default='A', verbose_name='Статус')
    date_init = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class CommentGrade(models.Model):
    class Meta:
        verbose_name = _('Оценка комментария')
        verbose_name_plural = _('Оценки комментариев')
        unique_together = ('evaluator', 'comment')

    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_grades',
                                  verbose_name='Оценивающий')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_grades',
                                verbose_name='Комментарий')
    grade = models.BooleanField(default=True, verbose_name='Оценка')
    status_vars = (
        ('A', 'Активна'),
        ('B', 'Заблокирована'),
    )
    status = models.CharField(max_length=3, choices=status_vars, default='A', verbose_name='Статус')