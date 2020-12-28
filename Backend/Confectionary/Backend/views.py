import shutil

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes, parser_classes

from rest_framework import generics, status
from djoser import utils
from djoser.conf import settings as djoser_settings

from .serializers import *

messages = {
    'USER_DOES_NOT_EXISTS': 'Пользователь не существует.',
    'USER_BLOCKED': 'Пользователь заблокирован.',
    'USER_REGISTERED': 'Регистрация прошла успешно.',
    'USER_EDITED': 'Профиль успешно отредактирован.',
    'PASSWORD_RESET': 'Пароль успешно изменён.',
    'RECIPE_ADDED': 'Рецепт успешно добавлен.',
    'RECIPE_EDITED': 'Рецепт успешно отредактирован.',
    'RECIPE_REMOVED': 'Рецепт успешно удалён.',
    'RECIPES_NONE': 'Рецепты не найдены.',
    'RECIPES_NONE_TITLE': 'Не найдено ни одного рецепта с введённым наименованием.',
    'RECIPES_NONE_TAG': 'Не найдено ни одного рецепта с введённым тегом.',
    'RECIPES_NONE_AUTHOR': 'Не найдено ни одного рецепта с введённым логином автора.',
    'RECIPES_NONE_ACCESSIBLE': 'Рецепт не существует или заблокирован.',
    'RECIPES_NONE_ACCESSIBLE_OR_OWN': 'Рецепт не существует, заблокирован или не принадлежит текущему пользователю.',
    'COMMENT_ADDED': 'Комментарий успешно добавлен.',
    'COMMENT_REMOVED': 'Комментарий успешно удалён.',
    'COMMENT_NOT_ACCESSIBLE': 'Комментарий не существует или заблокирован.',
    'NO_GRADE_YET': 'Оценка ещё не добавлена.',
    'GRADE_NOT_ACCESSIBLE': 'Оценка не существует или заблокирована для изменения.',
    'FIELD_MISMATCH': 'Ни одно поле формы не соответствует принимаемому формату.',
}


class CustomTokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = djoser_settings.SERIALIZERS.token_create
    permission_classes = djoser_settings.PERMISSIONS.token_create
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def _action(self, serializer):
        if Client.objects.get_by_natural_key(serializer.user.username).status == 'A':
            token = utils.login_user(self.request, serializer.user)
            token_serializer_class = djoser_settings.SERIALIZERS.token
            return Response(
                data=token_serializer_class(token).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message': messages['USER_BLOCKED']},
                status=status.HTTP_401_UNAUTHORIZED
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_all(request):
    try:
        recipes = Recipe.objects.filter(status='A')
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_title(request, search_title):
    try:
        recipes = Recipe.objects.filter(status='A', title__icontains=search_title)
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE_TITLE']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_tag(request, search_tag):
    try:
        recipes = Recipe.objects.filter(
            status='A',
            fixed_tags__in=(
                Tag.objects.filter(name__icontains=search_tag)
            )
        )
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE_TAG']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_author(request, search_author):
    try:
        recipes = Recipe.objects.filter(
            status='A',
            creator__in=(
                Client.objects.filter(username__icontains=search_author)
            )
        )
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE_AUTHOR']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_recipes(request):
    try:
        recipes = Recipe.objects.filter(status='A', creator=request.user)
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecipeCardForCreatorSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_info(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk, status='A')
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE_ACCESSIBLE']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecipePageSerializer(recipe)
    return Response(data={'recipe': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def client_info(request, pk):
    try:
        client = Client.objects.get(id=pk)
    except Client.DoesNotExist:
        return Response(
            data={'message': messages['USER_DOES_NOT_EXISTS']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = ClientPublicPageSerializer(client)
    return Response(data={'client': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_self_info(request):
    try:
        client = Client.objects.get(id=request.user.id)
    except Client.DoesNotExist:
        return Response(
            data={'message': messages['USER_DOES_NOT_EXISTS']},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = ClientSelfPageSerializer(client)
    return Response(data={'client': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([AllowAny])
def client_reg(request):
    new_client = ClientFormSerializer(data=request.data, partial=True)
    if new_client.is_valid():
        if new_client.validated_data:
            new_client.save()
            return Response(
                data={'message': messages['USER_REGISTERED']},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': messages['FIELD_MISMATCH']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(data=new_client.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def client_edit(request):
    try:
        old_client = Client.objects.get(id=request.user.id)
    except Client.DoesNotExist:
        return Response(
            data={'message': messages['USER_DOES_NOT_EXISTS']},
            status=status.HTTP_404_NOT_FOUND
        )

    # флаг сброса аватарки
    avatar_reset = False

    # если в поле 'avatar' кодовое слово 'reset'
    if request.data.get('avatar', None) == 'reset':
        edited_data = request.data.copy()
        edited_data.pop('avatar')
        new_client = ClientFormSerializer(instance=old_client, data=edited_data, partial=True)
        avatar_reset = True
    else:
        new_client = ClientFormSerializer(instance=old_client, data=request.data, partial=True)

    if new_client.is_valid():
        if new_client.validated_data:
            if avatar_reset:
                new_client.reset_avatar()
            new_client.save()
            return Response(
                data={'message': messages['USER_EDITED']},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data={'message': messages['FIELD_MISMATCH']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(data=new_client.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def client_pass_change(request):
    client = request.user
    passwords = ClientPasswordChangeSerializer(data=request.data)
    if passwords.is_valid():
        if passwords.validated_data:
            if client.check_password(passwords.data.get('old_password')):
                client.set_password(passwords.data.get('new_password'))
                client.save()
            return Response(
                data={'message': messages['PASSWORD_RESET']},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data={'message': messages['FIELD_MISMATCH']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(data=passwords.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def recipe_add(request):
    new_recipe = RecipeFormSerializer(data=request.data, context={'client': request.user}, partial=True)
    if new_recipe.is_valid():
        if new_recipe.validated_data:
            new_recipe.save()
            return Response(
                data={'message': messages['RECIPE_ADDED']},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': messages['FIELD_MISMATCH']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(data=new_recipe.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def recipe_edit(request, pk):
    try:
        old_recipe = Recipe.objects.get(id=pk, creator=request.user, status='A')
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE_ACCESSIBLE_OR_OWN']},
            status=status.HTTP_404_NOT_FOUND
        )

    # флаги сброса аватарки и картинок стадий приготовления
    avatar_reset = False
    pictures_reset = None

    # работаем с изменяемой копией request.data
    # (_mutable=True тоже работает, но не рекомендовано в документации)
    edited_data = request.data.copy()

    cook_stages_got = edited_data.get('cook_stages', None)
    if cook_stages_got:
        pictures_reset = [False] * len(cook_stages_got)
        index = 0
        for cook_stage in cook_stages_got:
            # если в поле 'picture' кодовое слово 'reset'
            if cook_stage.get('picture', None) == 'reset':
                del cook_stage['picture']
                pictures_reset[index] = True
            index += 1

    # если в поле 'avatar' кодовое слово 'reset'
    if edited_data.get('avatar', None) == 'reset':
        del edited_data['avatar']
        avatar_reset = True

    new_recipe = RecipeFormSerializer(instance=old_recipe, data=edited_data, partial=True)

    if new_recipe.is_valid():
        if new_recipe.validated_data:
            # физически зачищаем все сброшенные картинки
            if pictures_reset:
                index = 0
                for cook_stage in new_recipe.cook_stages:
                    if pictures_reset[index]:
                        cook_stage.reset_picture()
                    index += 1
            if avatar_reset:
                new_recipe.reset_avatar()

            new_recipe.save()
            return Response(
                data={'message': messages['RECIPE_EDITED']},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data={'message': messages['FIELD_MISMATCH']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(data=new_recipe.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def recipe_remove(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk, creator=request.user, status='A')
    except Recipe.DoesNotExist:
        return Response(
            data={'message': messages['RECIPES_NONE_ACCESSIBLE']},
            status=status.HTTP_404_NOT_FOUND
        )

    # зачищаем соответствующие данные рецепта в ФС
    # подготавливаем системный путь возможно созданного каталога файлов
    rm_path = settings.BASE_DIR + settings.MEDIA_URL + recipe_avatar_upload_path(recipe, '')
    rm_dir = 'recipes/%i' % recipe.id
    # пробуем удалить каталог со всеми связанными изображениями
    shutil.rmtree(path=rm_path[0: (rm_path.find(rm_dir) + len(rm_dir))], ignore_errors=True)

    recipe.delete()
    return Response(
        data={'message': messages['RECIPE_REMOVED']},
        status=status.HTTP_202_ACCEPTED
    )


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def comment_add(request, recipe_pk):
    new_comment = CommentFormSerializer(
        data=request.data,
        context={'creator': request.user, 'recipe_id': recipe_pk}
    )
    if new_comment.is_valid(raise_exception=False):
        if new_comment.validated_data:
            new_comment.save()
            return Response(
                data={'message': messages['COMMENT_ADDED']},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': messages['FIELD_MISMATCH']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(data=new_comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_remove(request, pk):
    try:
        comment = Comment.objects.get(id=pk, creator=request.user, status='A')
    except Comment.DoesNotExist:
        return Response(
            data={'message': messages['COMMENT_NOT_ACCESSIBLE']},
            status=status.HTTP_404_NOT_FOUND
        )
    comment.delete()
    return Response(
        data={'message': messages['COMMENT_REMOVED']},
        status=status.HTTP_202_ACCEPTED
    )


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def recipe_grade_add(request, recipe_pk):
    if Recipe.objects.filter(id=recipe_pk, status='A').exists():
        try:
            old_grade = RecipeGrade.objects.get(
                recipe=Recipe.objects.get(id=recipe_pk),
                evaluator=request.user
            )
            new_grade = RecipeGradeFormSerializer(instance=old_grade, data=request.data)
        except RecipeGrade.DoesNotExist:
            new_grade = RecipeGradeFormSerializer(
                data=request.data,
                context={'evaluator': request.user, 'recipe_id': recipe_pk})
        if new_grade.is_valid():
            if new_grade.validated_data:
                new_grade.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                data={'message': messages['FIELD_MISMATCH']},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=new_grade.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        data={'message': messages['RECIPES_NONE_ACCESSIBLE']},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_grade_check(request, recipe_pk):
    try:
        grade = RecipeGrade.objects.get(
            status='A',
            evaluator=request.user,
            recipe__in=Recipe.objects.filter(id=recipe_pk, status='A')
        )
    except RecipeGrade.DoesNotExist:
        return Response(
            data={'grade': messages['NO_GRADE_YET']},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(
        data={'grade': grade.grade},
        status=status.HTTP_200_OK
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def recipe_grade_cancel(request, recipe_pk):
    try:
        grade = RecipeGrade.objects.get(
            evaluator=request.user,
            recipe__in=Recipe.objects.filter(id=recipe_pk, status='A')
        )
    except RecipeGrade.DoesNotExist:
        return Response(
            data={'message': messages['GRADE_NOT_ACCESSIBLE']},
            status=status.HTTP_404_NOT_FOUND
        )
    # не удаляем, а только блокируем
    grade.status = 'B'
    grade.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def comment_grade_add(request, comment_pk):
    if Comment.objects.filter(id=comment_pk, status='A').exists():
        try:
            old_grade = CommentGrade.objects.get(
                comment=Comment.objects.get(id=comment_pk),
                evaluator=request.user
            )
            new_grade = CommentGradeFormSerializer(instance=old_grade, data=request.data)
        except CommentGrade.DoesNotExist:
            new_grade = CommentGradeFormSerializer(
                data=request.data,
                context={'evaluator': request.user, 'comment_id': comment_pk}
            )
        if new_grade.is_valid():
            if new_grade.validated_data:
                new_grade.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                data={'message': messages['FIELD_MISMATCH']},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=new_grade.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        data={'message': messages['COMMENT_NOT_ACCESSIBLE']},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_grade_check(request, comment_pk):
    try:
        grade = CommentGrade.objects.get(
            evaluator=request.user,
            comment__in=Comment.objects.filter(id=comment_pk, status='A')
        )
    except CommentGrade.DoesNotExist:
        return Response(
            data={'grade': messages['NO_GRADE_YET']},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(data={'grade': grade.grade}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_grade_cancel(request, comment_pk):
    try:
        grade = CommentGrade.objects.get(
            evaluator=request.user,
            comment__in=Comment.objects.filter(id=comment_pk, status='A')
        )
    except CommentGrade.DoesNotExist:
        return Response(
            data={'message': messages['GRADE_NOT_ACCESSIBLE']},
            status=status.HTTP_404_NOT_FOUND
        )
    # не удаляем, а только блокируем
    grade.status = 'B'
    grade.save()
    return Response(status=status.HTTP_204_NO_CONTENT)