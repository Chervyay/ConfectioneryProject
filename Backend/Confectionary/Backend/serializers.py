from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import *
# from django.conf import settings
import os

##### Сериализаторы данных пользователя #####

# (для карточки рецепта)
class ClientRecipeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'username')


# (для страницы рецепта)
class ClientRecipePageSerializer(ClientRecipeCardSerializer):

    avatar = serializers.SerializerMethodField()

    class Meta(ClientRecipeCardSerializer.Meta):
        fields = ClientRecipeCardSerializer.Meta.fields + ('avatar',)

    def get_avatar(self, client_obj):
        return settings.CURRENT_PREFIX + client_obj.try_get_avatar()


# (для публичной части страницы пользователя)
class ClientPublicPageSerializer(ClientRecipePageSerializer):

    status = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    class Meta(ClientRecipePageSerializer.Meta):
        fields = ClientRecipePageSerializer.Meta.fields + ('first_name', 'last_name', 'patronymic', 'status',
                                                           'date_joined', 'last_login')

    def get_status(self, client_obj):
        if client_obj.is_active:
            return "Активен"
        else:
            return "Заблокирован"

    def get_last_login(self, client_obj):
        last_login = client_obj.last_login
        if last_login:
            return last_login.strftime('%Y-%m-%d %H:%M:%S')


# (для страницы пользователя)
class ClientSelfPageSerializer(ClientRecipePageSerializer):
    class Meta(ClientRecipePageSerializer.Meta):
        fields = ClientRecipePageSerializer.Meta.fields + ('first_name', 'last_name', 'patronymic', 'email')


# (для регистрации или редактирования данных пользователя)
class ClientFormSerializer(serializers.ModelSerializer):

    avatar = serializers.ImageField(max_length=100, required=False)

    class Meta:
        model = Client
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'patronymic', 'avatar')

    def save(self):
        try:
            avatar_got = self.validated_data['avatar']
        except KeyError:
            avatar_got = None
        try:
            email_got = self.validated_data['email']
        except KeyError:
            email_got = None
        new_client = Client(
            username=self.validated_data['username'],
            email=email_got,
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            patronymic=self.validated_data['patronymic'],
            avatar=avatar_got
        )
        password = self.validated_data['password']
        new_client.set_password(password)
        client_group = Group.objects.get(name='client')
        new_client.save()
        client_group.user_set.add(new_client)



##### Сериализаторы данных тега #####

# (для прикрепления тега к рецепту)
class TagFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedTag
        fields = ('name',)


# (для страницы рецепта)
class TagSerializer(TagFormSerializer):
    class Meta(TagFormSerializer.Meta):
        model = FixedTag
        fields = TagFormSerializer.Meta.fields + ('id',)



##### Сериализаторы данных комментария #####

# (для страницы рецепта)
class CommentSerializer(serializers.ModelSerializer):
    creator = ClientRecipePageSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'creator', 'body', 'date_init', 'rating')

    def get_rating(self, comment_obj):
        grades = CommentGrade.objects.filter(comment=comment_obj.id)
        rating_value = 0
        # Проходимся по всем объектам оценивания и подсчитываем общий рейтинг
        for grade in grades:
            if grade.grade:
                rating_value += 1
            else:
                rating_value -= 1
        return rating_value


class CommentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)

    def save(self, request_client, request_recipe):
        new_comment = CommentGrade(
            creator=request_client,
            recipe=request_recipe,
            body=self.validated_data['body']
        )
        new_comment.save()



##### Сериализаторы данных прикреплённого изображения #####

# (для страницы рецепта)
class FixedPictureSerializer(serializers.ModelSerializer):

    picture = serializers.SerializerMethodField()

    class Meta:
        model = FixedPicture
        fields = ('id', 'picture',)

    def get_picture(self, picture_obj):
        return settings.CURRENT_PREFIX + picture_obj.picture.url


# (для добавления изображения к рецепту)
class FixedPictureFormSerializer(serializers.ModelSerializer):

    picture = serializers.ImageField(max_length=100)

    class Meta:
        model = FixedPicture
        fields = ('picture',)



##### Сериализаторы данных рецепта #####

# (для карточки рецепта конкретного пользователя)
class RecipeCardForCreatorSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'avatar', 'rating')

    def get_avatar(self, recipe_obj):
        return settings.CURRENT_PREFIX + recipe_obj.try_get_avatar()

    def get_rating(self, recipe_obj):
        grades = RecipeGrade.objects.filter(recipe=recipe_obj.pk)
        rating_value = 0
        # Проходимся по всем объектам оценивания и подсчитываем общий рейтинг
        for grade in grades:
            if grade.grade:
                rating_value += 1
            else:
                rating_value -= 1
        return rating_value


# (для карточки рецепта)
class RecipeCardSerializer(RecipeCardForCreatorSerializer):

    creator = ClientRecipeCardSerializer()

    class Meta(RecipeCardForCreatorSerializer.Meta):
        model = Recipe
        fields = RecipeCardForCreatorSerializer.Meta.fields + ('creator',)


# (для страницы рецепта)
class RecipePageSerializer(RecipeCardSerializer):

    creator = ClientRecipePageSerializer()
    fixed_pictures = FixedPictureSerializer(many=True)
    fixed_tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta(RecipeCardSerializer.Meta):
        fields = RecipeCardSerializer.Meta.fields + ('body', 'date_init', 'fixed_pictures', 'fixed_tags', 'comments')


# (для создания рецепта)
class RecipeFormSerializer(serializers.ModelSerializer):

    avatar = serializers.ImageField(max_length=100, required=False)
    fixed_pictures = FixedPictureFormSerializer(many=True, required=False)
    fixed_tags = TagFormSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('title', 'body', 'avatar', 'fixed_pictures', 'fixed_tags')

    def save(self, request_client):
        try:
            avatar_got = self.validated_data['avatar']
        except KeyError:
            avatar_got = None
        try:
            pictures_got = self.validated_data['fixed_pictures']
        except KeyError:
            pictures_got = None
        try:
            tags_got = self.validated_data['fixed_tags']
        except KeyError:
            tags_got = None
        new_recipe = Recipe(
            creator=request_client,
            title=self.validated_data['title'],
            body=self.validated_data['body'],
            avatar=avatar_got,
        )
        new_recipe.fixed_pictures.set(pictures_got)
        new_recipe.fixed_tags.set(tags_got)
        new_recipe.save()



##### Сериализаторы оценок #####

# (для создания оценки рецепта)
class RecipeGradeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeGrade
        fields = ('grade',)

    def save(self, request_client, request_recipe):
        new_grade = RecipeGrade(
            evaluator=request_client,
            recipe=request_recipe,
            grade=self.validated_data['grade']
        )
        new_grade.save()


# (для создания оценки комментария)
class CommentGradeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentGrade
        fields = ('grade',)

    def save(self, request_client, request_comment):
        new_grade = CommentGrade(
            evaluator=request_client,
            comment=request_comment,
            grade=self.validated_data['grade']
        )
        new_grade.save()