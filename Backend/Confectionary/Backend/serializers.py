from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import *
# from django.conf import settings
import os
import base64

##### Сериализаторы данных пользователя #####

# (для карточки рецепта)
class ClientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'username')


# (для страницы рецепта)
class ClientSurfaceSerializer(ClientSimpleSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta(ClientSimpleSerializer.Meta):
        fields = ClientSimpleSerializer.Meta.fields + ('avatar',)

    def get_avatar(self, client_obj):
        # settings.BASE_DIR + ...
        return client_obj.avatar.path + '.' + client_obj.avatar.format


# (для публичной части страницы пользователя)
class ClientShowSerializer(ClientSurfaceSerializer):
    status = serializers.SerializerMethodField()

    class Meta(ClientSurfaceSerializer.Meta):
        fields = ClientSurfaceSerializer.Meta.fields + ('first_name', 'last_name', 'patronymic', 'status',
                                                        'date_joined', 'last_login')

    def get_status(self, client_obj):
        if client_obj.is_active:
            return "Активен"
        else:
            return "Заблокирован"


# (для страницы пользователя)
class ClientSerializer(ClientSurfaceSerializer):
    class Meta(ClientSurfaceSerializer.Meta):
        fields = ClientSurfaceSerializer.Meta.fields + ('first_name', 'last_name', 'patronymic', 'email')


# (для регистрации пользователя)
class ClientDeserializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('username', 'email', 'avatar', 'first_name', 'last_name', 'patronymic')

    def get_avatar(self, client_obj):
        # Изображение приходит в кодировке base64
        avatar_decoded = base64.b64decode(client_obj.avatar.picture)
        avatar_format = client_obj.avatar.format
        avatar_path = settings.CLIENT_AVATARS_DIR + '/' + str(
            len(os.listdir(settings.CLIENT_AVATARS_DIR)) + 1) + '.' + avatar_format
        picture_file = open(avatar_path, 'w')
        picture_file.write(avatar_decoded)
        picture_file.close()
        avatar = ClientAvatar(client_id=client_obj, path=avatar_path, format=avatar_format)
        return avatar

    def save(self):
        new_client = Client(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            patronymic=self.validated_data['patronymic'],
            avatar=self.avatar,
        )
        password = self.validated_data['password']
        new_client.set_password(password)
        client_group = Group.objects.get(name='client')
        new_client.save()
        client_group.user_set.add(new_client)



##### Сериализаторы данных тега #####

# (для страницы рецепта)
class TagSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedTag
        fields = ('id', 'name')



##### Сериализаторы данных комментария #####

# (для страницы рецепта)
class CommentSerializer(serializers.ModelSerializer):
    creator = ClientSurfaceSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'creator', 'body', 'date_init', 'rating')

    def get_rating(self, comment_obj):
        grades = CommentGrade.objects.filter(comment=comment_obj.pk)
        rating_value = 0
        # Проходимся по всем объектам оценивания и подсчитываем общий рейтинг
        for grade in grades:
            if grade.grade:
                rating_value += 1
            else:
                rating_value -= 1
        return rating_value


class CommentDeserializer(serializers.ModelSerializer):
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
        return picture_obj.path + '.' + picture_obj.format


# (для добавления изображения к рецепту)
class FixedPictureDeserializer(serializers.ModelSerializer):

    path = serializers.SerializerMethodField()

    class Meta:
        model = FixedPicture
        fields = ('path', 'format')

    def get_path(self, picture_obj):
        # Изображение приходит в кодировке base64
        picture_decoded = base64.b64decode(picture_obj.picture)
        picture_path = settings.RECIPE_PICTURES_DIR + '/' + str(len(os.listdir(settings.RECIPE_PICTURES_DIR)) + 1)
        picture_file = open(picture_path, 'w')
        picture_file.write(picture_decoded)
        picture_file.close()
        return picture_path



##### Сериализаторы данных рецепта #####

# (для карточки рецепта конкретного пользователя)
class RecipeForCreatorSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'avatar', 'rating')

    def get_avatar(self, recipe_obj):
        return recipe_obj.avatar.path + '.' + recipe_obj.avatar.format

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
class RecipeShowSerializer(RecipeForCreatorSerializer):

    creator = ClientSimpleSerializer()

    class Meta(RecipeForCreatorSerializer.Meta):
        model = Recipe
        fields = RecipeForCreatorSerializer.Meta.fields + ('creator',)


# (для страницы рецепта)
class RecipeSerializer(RecipeShowSerializer):

    creator = ClientSurfaceSerializer()
    fixed_pictures = FixedPictureSerializer(many=True)
    fixed_tags = TagSimpleSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta(RecipeShowSerializer.Meta):
        fields = RecipeShowSerializer.Meta.fields + ('body', 'date_init', 'fixed_pictures', 'fixed_tags', 'comments')


# (для создания рецепта)
class RecipeDeserializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    fixed_pictures = FixedPictureDeserializer(many=True)

    class Meta:
        model = Recipe
        fields = ('title', 'body', 'avatar', 'fixed_pictures')

    def get_avatar(self, recipe_obj):
        # Изображение приходит в кодировке base64
        avatar_decoded = base64.b64decode(recipe_obj.avatar)
        avatar_path = settings.RECIPE_AVATARS_DIR + '/' + str(len(os.listdir(settings.RECIPE_AVATARS_DIR)) + 1)
        picture_file = open(avatar_path, 'w')
        picture_file.write(avatar_decoded)
        picture_file.close()
        return avatar_path

    def save(self, request_client):
        new_recipe = Recipe(
            creator=request_client,
            title=self.validated_data['title'],
            body=self.validated_data['body'],
            avatar=self.validated_data['avatar'],
            fixed_pictures=self.validated_data['fixed_pictures'],
        )
        new_recipe.save()



##### Сериализаторы оценок #####

# (для создания оценки рецепта)
class RecipeGradeDeserializer(serializers.ModelSerializer):
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
class CommentGradeDeserializer(serializers.ModelSerializer):
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