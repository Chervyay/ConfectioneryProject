from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes, parser_classes

from rest_framework import generics, status
from djoser import utils
from djoser.conf import settings as djoser_settings
from djoser.views import TokenCreateView

from .serializers import *
# import random


class CustomTokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = djoser_settings.SERIALIZERS.token_create
    permission_classes = djoser_settings.PERMISSIONS.token_create
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def _action(self, serializer):
        if Client.objects.get_by_natural_key(serializer.user.username).status == 'A':
            token = utils.login_user(self.request, serializer.user)
            token_serializer_class = djoser_settings.SERIALIZERS.token
            return Response(data=token_serializer_class(token).data, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Пользователь заблокирован."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_all(request):
    try:
        recipes = Recipe.objects.filter(status='A')
    except Recipe.DoesNotExist:
        return Response(data={"message": "Список рецептов пуст."}, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)

'''
@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_random(request, quantity):
    max_quantity = Recipe.objects.filter(status='A').count()
    if quantity < 0:
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)
    elif quantity > max_quantity:
        recipes = Recipe.objects.all()
    else:
        # Массив случайных id
        random_id = [0] * quantity
        for i in range(len(random_id)):
            while True:
                random_id[i] = random.randint(1, Recipe.objects.last().pk)
                if Recipe.objects.filter(status='A', id=random_id[i]).exists():
                    exist_flg = False
                    for j in range(len(random_id)):
                        if random_id[j] == random_id[i] and not i == j:
                            exist_flg = True
                            break
                    if exist_flg:
                        continue
                    else:
                        break
                else:
                    continue
        recipes = Recipe.objects.filter(id__in=random_id)
    if recipes.exists():
        serializer = RecipeShowSerializer(recipes, many=True)
        return Response({'recipes': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)'''


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_title(request, search_title):
    try:
        recipes = Recipe.objects.filter(status='A', title__icontains=search_title)
    except Recipe.DoesNotExist:
        return Response(data={"message": "Не найдено ни одного рецепта с введённым наименованием."},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_tag(request, search_tag):
    try:
        recipes = Recipe.objects.filter(status='A', fixed_tags__in=(
            Tag.objects.filter(name__icontains=search_tag)
        ))
    except Recipe.DoesNotExist:
        return Response(data={"message": "Не найдено ни одного рецепта с введённым тегом."},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_author(request, search_author):
    try:
        recipes = Recipe.objects.filter(status='A', creator__in=(
            Client.objects.filter(username__icontains=search_author)
        ))
    except Recipe.DoesNotExist:
        return Response(data={"message": "Не найдено ни одного рецепта с введённым логином автора."},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_recipes(request):
    try:
        recipes = Recipe.objects.filter(status='A', creator=request.user)
    except Recipe.DoesNotExist:
        return Response(data={"message": "Список рецептов пуст."}, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardForCreatorSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_info(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk, status='A')
    except Recipe.DoesNotExist:
        return Response(data={"message": "Рецепт не существует или заблокирован."}, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipePageSerializer(recipe)
    return Response(data={'recipe': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def client_info(request, pk):
    try:
        client = Client.objects.get(id=pk)
    except Client.DoesNotExist:
        return Response(data={"message": "Пользователь не существует."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClientPublicPageSerializer(client)
    return Response(data={'client': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_self_info(request):
    try:
        client = Client.objects.get(id=request.user.id)
    except Client.DoesNotExist:
        return Response(data={"message": "Пользователь не существует или заблокироан."},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = ClientSelfPageSerializer(client)
    return Response(data={'client': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([AllowAny])
def client_reg(request):
    new_client = ClientFormSerializer(data=request.data, partial=True)
    if new_client.is_valid():
        new_client.save()
        return Response(data={"message": "Регистрация прошла успешно."}, status=status.HTTP_201_CREATED)
    return Response(data=new_client.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def client_edit(request):
    try:
        old_client = Client.objects.get(id=request.user.id)
    except Client.DoesNotExist:
        return Response(data={"message": "Пользователь не существует или заблокирован."},
                        status=status.HTTP_404_NOT_FOUND)
    '''if request.data.get('avatar', None) == 'reset':
        request.data['avatar'] = '''''
    new_client = ClientFormSerializer(instance=old_client, data=request.data, partial=True)
    if new_client.is_valid():
        new_client.save()
        return Response(data={"message": "Данные профиля успешно отредактированы."},
                        status=status.HTTP_202_ACCEPTED)
    return Response(data=new_client.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def client_pass_change(request):
    client = request.user
    passwords = ClientPasswordChangeSerializer(data=request.data)
    if passwords.is_valid():
        if client.check_password(passwords.data.get('old_password')):
            client.set_password(passwords.data.get('new_password'))
            client.save()
        return Response(data={"message": "Пароль успешно изменён."}, status=status.HTTP_202_ACCEPTED)
    return Response(data=passwords.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def recipe_add(request):
    new_recipe = RecipeFormSerializer(data=request.data, context={"client": request.user}, partial=True)
    if new_recipe.is_valid():
        new_recipe.save()
        return Response(data={"message": "Рецепт успешно добавлен."}, status=status.HTTP_201_CREATED)
    return Response(data=new_recipe.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def recipe_edit(request, pk):
    try:
        old_recipe = Recipe.objects.get(id=pk, creator=request.user, status='A')
    except Recipe.DoesNotExist:
        return Response(data={"message": "Рецепт не существует, заблокирован или не принадлежит текущему пользователю."},
                        status=status.HTTP_404_NOT_FOUND)
    new_recipe = RecipeFormSerializer(instance=old_recipe, data=request.data, partial=True)
    if new_recipe.is_valid():
        new_recipe.save()
        return Response(data={"message": "Данные рецепта успешно отредактированы."}, status=status.HTTP_202_ACCEPTED)
    return Response(data=new_recipe.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def recipe_remove(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk, creator=request.user, status='A')
    except Recipe.DoesNotExist:
        return Response(data={"message": "Рецепт не существует или заблокирован."}, status=status.HTTP_404_NOT_FOUND)
    recipe.delete()
    return Response(data={"message": "Рецепт успешно удалён."}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def comment_add(request, recipe_pk):
    new_comment = CommentFormSerializer(data=request.data, context={"creator": request.user, "recipe_id": recipe_pk})
    if new_comment.is_valid(raise_exception=False):
        new_comment.save()
        return Response(data={"message": "Комментарий успешно добавлен."}, status=status.HTTP_201_CREATED)
    return Response(data=new_comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_remove(request, pk):
    try:
        comment = Comment.objects.get(id=pk, creator=request.user, status='A')
    except Comment.DoesNotExist:
        return Response(data={"message": "Комментарий не существует или заблокирован."},
                        status=status.HTTP_404_NOT_FOUND)
    comment.delete()
    return Response(data={"message": "Комментарий успешно удалён."}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def recipe_grade_add(request, recipe_pk):
    if Recipe.objects.filter(id=recipe_pk, status='A').exists():
        try:
            old_grade = RecipeGrade.objects.get(
                recipe=Recipe.objects.get(id=recipe_pk),
                evaluator=request.user)
            new_grade = RecipeGradeFormSerializer(instance=old_grade, data=request.data)
        except RecipeGrade.DoesNotExist:
            new_grade = RecipeGradeFormSerializer(data=request.data,
                                                  context={"evaluator": request.user,
                                                           "recipe_id": recipe_pk})
        if new_grade.is_valid():
            new_grade.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=new_grade.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"message": "Рецепт не существует или заблокирован."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_grade_check(request, recipe_pk):
    try:
        grade = RecipeGrade.objects.get(status='A', evaluator=request.user,
                                        recipe__in=Recipe.objects.filter(
                                            id=recipe_pk, status='A'))
    except RecipeGrade.DoesNotExist:
        return Response(data={"grade": "Ещё не оценено."},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(data={"grade": grade.grade},
                    status=status.HTTP_200_OK)


'''@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def recipe_grade_inverse(request, recipe_pk):
    try:
        grade = RecipeGrade.objects.get(evaluator=request.user,
                                        recipe__in=Recipe.objects.filter(
                                            id=recipe_pk, status='A'))
    except RecipeGrade.DoesNotExist:
        return Response(data={"message": "Оценка не существует или не может быть изменена."},
                        status=status.HTTP_404_NOT_FOUND)
    grade.status = 'A'
    grade.grade = not grade.grade
    grade.save()
    return Response(status=status.HTTP_204_NO_CONTENT)'''


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def recipe_grade_cancel(request, recipe_pk):
    try:
        grade = RecipeGrade.objects.get(evaluator=request.user,
                                        recipe__in=Recipe.objects.filter(
                                            id=recipe_pk, status='A'))
    except RecipeGrade.DoesNotExist:
        return Response(data={"message": "Оценка не существует или не может быть отменена."},
                        status=status.HTTP_404_NOT_FOUND)
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
                evaluator=request.user)
            new_grade = CommentGradeFormSerializer(instance=old_grade, data=request.data)
        except CommentGrade.DoesNotExist:
            new_grade = CommentGradeFormSerializer(data=request.data,
                                                   context={"evaluator": request.user,
                                                            "comment_id": comment_pk})
        if new_grade.is_valid():
            new_grade.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=new_grade.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"message": "Комментарий не существует или заблокирован."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_grade_check(request, comment_pk):
    try:
        grade = CommentGrade.objects.get(evaluator=request.user,
                                         comment__in=Comment.objects.filter(
                                             id=comment_pk, status='A'))
    except CommentGrade.DoesNotExist:
        return Response(data={"grade": "Ещё не оценено."},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(data={"grade": grade.grade},
                    status=status.HTTP_200_OK)


'''@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_grade_inverse(request, comment_pk):
    try:
        grade = CommentGrade.objects.get(evaluator=request.user,
                                         comment__in=Comment.objects.filter(id=comment_pk, status='A'))
    except CommentGrade.DoesNotExist:
        return Response(data={"message": "Оценка не найдена или не может быть изменена."},
                        status=status.HTTP_404_NOT_FOUND)
    grade.status = 'A'
    grade.grade = not grade.grade
    grade.save()
    return Response(status=status.HTTP_204_NO_CONTENT)'''


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_grade_cancel(request, comment_pk):
    try:
        grade = CommentGrade.objects.get(evaluator=request.user,
                                         comment__in=Comment.objects.filter(id=comment_pk, status='A'))
    except CommentGrade.DoesNotExist:
        return Response(data={"message": "Оценка не существует или не может быть отменена."},
                        status=status.HTTP_404_NOT_FOUND)
    # не удаляем, а только блокируем
    grade.status = 'B'
    grade.save()
    return Response(status=status.HTTP_204_NO_CONTENT)