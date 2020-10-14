from django.db import models
from django.conf import settings
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from .validators import *
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


def client_avatar_upload_path(instance, filename):
    return '/'.join(['pictures', 'users', instance.username, 'avatar', filename])


def recipe_avatar_upload_path(instance, filename):
    return '/'.join(['pictures', 'users', instance.creator.username, 'recipes', instance.id,
                     'avatar', filename])


def recipe_picture_upload_path(instance, filename):
    return '/'.join(['pictures', 'users', instance.recipe.creator.username, 'recipes',
                     instance.recipe.id, 'pictures', filename])


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
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)

    objects = ClientManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    def try_get_avatar(self):
        try:
            got_avatar = self.avatar.url
        except ValueError:
            return '/'.join(['/media', 'pictures', 'default', 'client_default.jpg'])
        if os.path.exists(settings.BASE_DIR + got_avatar):
            return got_avatar
        return '/'.join(['/media', 'pictures', 'default', 'client_default.jpg'])


class Recipe(models.Model):
    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='recipes',
                                verbose_name='Рецепт')
    title = models.CharField(max_length=100, default='', verbose_name='Наименование')
    body = models.TextField(default='', verbose_name='Описание')
    avatar = models.ImageField(upload_to=recipe_avatar_upload_path, max_length=100, blank=True, verbose_name='Аватарка')
    status_vars = (
        ('A', 'В широком доступе'),
        ('B', 'Заблокировано'),
    )
    status = models.CharField(max_length=3, choices=status_vars, default='A', verbose_name='Статус')
    date_init = models.DateField(default=timezone.now, verbose_name='Дата создания')

    def try_get_avatar(self):
        try:
            got_avatar = self.avatar.url
        except ValueError:
            return '/'.join(['/media', 'pictures', 'default', 'recipe_default.jpg'])
        if os.path.exists(settings.BASE_DIR + got_avatar):
            return got_avatar
        return '/'.join(['/media', 'pictures', 'default', 'recipe_default.jpg'])


class FixedPicture(models.Model):
    class Meta:
        verbose_name = _('Прикреплённое изображение')
        verbose_name_plural = _('Прикреплённые изображения')
        unique_together = ('recipe', 'picture')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='fixed_pictures',
                               verbose_name='Рецепт')
    picture = models.ImageField(upload_to=recipe_picture_upload_path, max_length=100, verbose_name='Изображение')

    '''def try_get_picture(self):
        try:
            got_picture = self.picture.url
        except ValueError:
            pass
        if os.path.exists(settings.BASE_DIR + got_picture):
            return got_picture
        pass'''


class FixedTag(models.Model):
    class Meta:
        verbose_name = _('Прикреплённый тег')
        verbose_name_plural = _('Прикреплённые теги')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='fixed_tags', verbose_name='Рецепт')
    name = models.CharField(max_length=30, default='', validators=[CustomTagValidator()], unique=True,
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
    date_init = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')


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