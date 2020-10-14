from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
# import random


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_all(request):
    try:
        recipes = Recipe.objects.filter(status='A')
    except Recipe.DoesNotExist:
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
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
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipes_by_tag(request, search_tag):
    try:
        recipes = Recipe.objects.filter(status='A', fixed_tags__in=(
            FixedTag.objects.filter(name__icontains=search_tag)
        ))
    except Recipe.DoesNotExist:
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
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
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def client_recipes(request, pk):
    try:
        recipes = Recipe.objects.filter(status='A', creator__in=(Client.objects.filter(id=pk)))
    except Recipe.DoesNotExist:
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeCardForCreatorSerializer(recipes, many=True)
    return Response(data={'recipes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_info(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk)
    except Recipe.DoesNotExist:
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipePageSerializer(recipe)
    return Response(data={'recipe': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def client_info(request, pk):
    try:
        client = Client.objects.get(id=pk)
    except Client.DoesNotExist:
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)
    serializer = ClientPublicPageSerializer(client)
    return Response(data={'client': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def client_reg(request):
    new_client = ClientFormSerializer(data=request.data)
    if new_client.is_valid(raise_exception=False):
        new_client.save()
        return Response(data=new_client.data, status=status.HTTP_201_CREATED)
    return Response(data=new_client.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def recipe_add(request):
    new_recipe = RecipeFormSerializer(data=request.data)
    if new_recipe.is_valid(raise_exception=False):
        new_recipe.save(request.user)
        return Response(data=new_recipe.data, status=status.HTTP_201_CREATED)
    return Response(data=new_recipe.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def comment_add(request, recipe_pk):
    new_comment = CommentFormSerializer(data=request.data)
    if new_comment.is_valid(raise_exception=False):
        new_comment.save(request.user, recipe_pk)
        return Response(data=new_comment.data, status=status.HTTP_201_CREATED)
    return Response(data=new_comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def recipe_grade_add(request, recipe_pk):
    new_grade = RecipeGradeFormSerializer(data=request.data)
    if Recipe.objects.get(id=recipe_pk).exists() and new_grade.is_valid(raise_exception=False):
        new_grade.save(request.user, recipe_pk)
        return Response(data=new_grade.data, status=status.HTTP_201_CREATED)
    return Response(data=new_grade.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def comment_grade_add(request, comment_pk):
    new_grade = CommentGradeFormSerializer(data=request.data)
    if Comment.objects.get(id=comment_pk).exists() and new_grade.is_valid(raise_exception=False):
        new_grade.save(request.user, comment_pk)
        return Response(data=new_grade.data, status=status.HTTP_201_CREATED)
    return Response(data=new_grade.errors, status=status.HTTP_400_BAD_REQUEST)