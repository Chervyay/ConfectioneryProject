from .models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from django.conf import settings


##### Сериализаторы данных пользователя #####

# (для карточки рецепта)
class ClientRecipeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username']


# (для страницы рецепта)
class ClientRecipePageSerializer(ClientRecipeCardSerializer):

    avatar = serializers.SerializerMethodField()

    class Meta(ClientRecipeCardSerializer.Meta):
        fields = ClientRecipeCardSerializer.Meta.fields + ['avatar']

    def get_avatar(self, client_obj):
        return settings.CURRENT_PREFIX + client_obj.try_get_avatar()


# (для страницы пользователя в личном кабинете)
class ClientSelfPageSerializer(ClientRecipePageSerializer):

    class Meta(ClientRecipePageSerializer.Meta):
        fields = ClientRecipePageSerializer.Meta.fields + ['email', 'first_name', 'last_name', 'patronymic',
                                                           'date_joined']


# (для публичной части страницы пользователя)
class ClientPublicPageSerializer(ClientSelfPageSerializer):

    status = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    class Meta(ClientSelfPageSerializer.Meta):
        fields = ClientSelfPageSerializer.Meta.fields + ['status', 'last_login']

    def get_status(self, client_obj):
        return client_obj.get_status_display()

    def get_last_login(self, client_obj):
        if client_obj.last_login:
            return client_obj.last_login.strftime('%Y-%m-%d %H:%M:%S')


# (для регистрации или редактирования данных пользователя)
class ClientFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'patronymic', 'avatar']
        extra_kwargs = {
            'email': {'required': False},
            'avatar': {'required': False}
        }

    def reset_avatar(self):
        self.instance.avatar.delete(save=True)
        self.instance.avatar = ''
        self.instance.save()

    def create(self, validated_data):
        password_got = validated_data.pop('password')
        new_client = Client.objects.create(**validated_data)
        new_client.set_password(password_got)
        client_group = Group.objects.get(name='client')
        new_client.save()
        client_group.user_set.add(new_client)
        return new_client

    # исключаем возможность сменить пароль через обычный запрос на редактирование
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)

        avatar_got = validated_data.get('avatar',  None)
        if avatar_got:
            # удаляем предыдущее изображение; метод не выбрасывает исключений
            instance.avatar.delete(save=True)
            instance.avatar = avatar_got

        instance.save()
        return instance


class ClientPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, password):
        validate_password(password)
        return password



##### Сериализаторы данных тега #####

# (для прикрепления тега к рецепту)
class TagFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


# (для страницы рецепта)
class TagSerializer(TagFormSerializer):
    class Meta(TagFormSerializer.Meta):
        model = Tag
        fields = TagFormSerializer.Meta.fields + ['id']



##### Сериализаторы данных комментария #####

# (для страницы рецепта)
class CommentSerializer(serializers.ModelSerializer):

    creator = ClientRecipePageSerializer()
    date_init = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'creator', 'body', 'date_init', 'rating']

    def get_date_init(self, comment_obj):
        return comment_obj.date_init.strftime('%Y-%m-%d %H:%M:%S')

    def get_rating(self, comment_obj):
        grades = CommentGrade.objects.filter(comment=comment_obj.id)
        rating_value = 0
        # Проходимся по всем объектам оценивания и подсчитываем общий рейтинг
        for grade in grades:
            if grade.status == 'B':
                continue
            elif grade.grade:
                rating_value += 1
            else:
                rating_value -= 1
        return rating_value


class CommentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']

    def create(self, validated_data):
        new_comment = Comment.objects.create(
            **validated_data,
            creator=self.context['creator'],
            recipe=Recipe.objects.get(id=self.context['recipe_id']))
        new_comment.save()
        return new_comment



##### Сериализаторы данных ингредиентов #####

# (для прикрепления ингредиента к рецепту)
class IngredientFormSerialier(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'measure']


# (для страницы рецепта)
class IngredientSerializer(IngredientFormSerialier):
    class Meta(IngredientFormSerialier.Meta):
        fields = IngredientFormSerialier.Meta.fields + ['id']



##### Сериализаторы данных этапов приготовления #####

# (для страницы рецепта)
class CookStageSerializer(serializers.ModelSerializer):

    picture = serializers.SerializerMethodField()

    class Meta:
        model = CookStage
        fields = ['id', 'description', 'picture']

    def get_picture(self, cook_stage_obj):
        return settings.CURRENT_PREFIX + cook_stage_obj.try_get_picture()


# (для добавления к рецепту)
class CookStageFormSerializer(serializers.ModelSerializer):

    picture = serializers.SerializerMethodField(required=False)

    class Meta:
        model = CookStage
        fields = ['description', 'picture']

    def reset_picture(self):
        self.instance.picture.delete(save=True)
        self.instance.picture = ''
        self.instance.save()

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)

        picture_got = validated_data.get('picture', None)
        if picture_got:
            # удаляем предыдущее изображение; метод не выбрасывает исключений
            instance.picture.delete(save=True)
            instance.picture = picture_got

        instance.save()
        return instance



##### Сериализаторы данных рецепта #####

# (для карточки рецепта конкретного пользователя)
class RecipeCardForCreatorSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'avatar', 'rating']

    def get_avatar(self, recipe_obj):
        return settings.CURRENT_PREFIX + recipe_obj.try_get_avatar()

    def get_rating(self, recipe_obj):
        grades = RecipeGrade.objects.filter(recipe=recipe_obj.pk)
        rating_value = 0
        # Проходимся по всем объектам оценивания и подсчитываем общий рейтинг
        for grade in grades:
            if grade.status == 'B':
                continue
            elif grade.grade:
                rating_value += 1
            else:
                rating_value -= 1
        return rating_value


# (для карточки рецепта)
class RecipeCardSerializer(RecipeCardForCreatorSerializer):

    creator = ClientRecipeCardSerializer()

    class Meta(RecipeCardForCreatorSerializer.Meta):
        model = Recipe
        fields = RecipeCardForCreatorSerializer.Meta.fields + ['creator', 'cook_time', 'portions']


# (для страницы рецепта)
class RecipePageSerializer(RecipeCardSerializer):

    creator = ClientRecipePageSerializer()
    ingredients = IngredientSerializer(many=True)
    cook_stages = CookStageSerializer(many=True)
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta(RecipeCardSerializer.Meta):
        fields = RecipeCardSerializer.Meta.fields + ['weight', 'ingredients', 'cook_stages', 'date_init', 'tags',
                                                     'comments']


# (для создания и редактирования рецепта)
class RecipeFormSerializer(serializers.ModelSerializer):

    ingredients = IngredientFormSerialier(many=True, required=False)
    cook_stages = CookStageFormSerializer(many=True, required=False)
    tags = TagFormSerializer(many=True, required=False)

    max_ingredients = 20
    max_cook_stages = 30
    max_tags = 5

    class Meta:
        model = Recipe
        fields = ['title', 'portions', 'cook_time', 'weight', 'avatar', 'ingredients',
                  'cook_stages', 'tags']
        extra_kwargs = {
            'portions': {'required': False},
            'cook_time': {'required': False},
            'weight': {'required': False},
            'avatar': {'required': False}
        }

    def reset_avatar(self):
        self.instance.avatar.delete(save=True)
        self.instance.avatar = ''
        self.instance.save()

    def create(self, validated_data):
        # выталкиваем все данные связанных таблиц
        ingredients_got = validated_data.pop('ingredients', None)
        cook_stages_got = validated_data.pop('cook_stages', None)
        tags_got = validated_data.pop('tags', None)

        new_recipe = Recipe.objects.create(**validated_data, creator=self.context['client'])

        # создаём все связанные объекты других таблиц
        if ingredients_got:
            for ingredient in ingredients_got:
                Ingredient.objects.create(**ingredient, recipe=new_recipe)
                self.max_ingredients -= 1
                if self.max_ingredients == 0:
                    break
        if cook_stages_got:
            for cook_stage in cook_stages_got:
                CookStage.objects.create(**cook_stage, recipe=new_recipe)
                self.max_cook_stages -= 1
                if self.max_cook_stages == 0:
                    break
        if tags_got:
            for tag in tags_got:
                Tag.objects.create(**tag, recipe=new_recipe)
                self.max_tags -= 1
                if self.max_tags == 0:
                    break

        return new_recipe

    def partial_update_nested_multiple(self, instance, model, data, max_quantity):
        # редактируем (при необходимости добавляем, удаляем) все связанные объекты других таблиц
        # проверяем, пришёл ли словарь объектов (не пришёл - ничего не меняем)
        if not (data is None):
            # если пришёл пустой словарь, то удаляем все объекты
            if not data:
                model.objects.filter(recipe=instance).delete()
            # вводим итераторы
            obj_iter = iter(model.objects.filter(recipe=instance))
            data_iter = iter(data)
            # используем ограничение на максимальное количество в качестве обратного счётчика
            while max_quantity:
                # пробуем получить следующий объект для редактирования
                try:
                    curr_obj = next(obj_iter)
                except StopIteration:
                    # не получаем - просто добавляем оставшиеся объекты с нужными данными
                    try:
                        while True:
                            model.objects.create(**next(data_iter), recipe=instance)
                            max_quantity -= 1
                    except StopIteration:
                        pass
                    break
                # пробуем получить данные следующего объекта для редактирования
                try:
                    curr_data = next(data_iter)
                except StopIteration:
                    # не получаем - просто удаляем оставшиеся объекты
                    curr_obj.delete()
                    try:
                        while True:
                            next(obj_iter).delete()
                    except StopIteration:
                        pass
                    break
                model.objects.filter(id=curr_obj.id).update(**curr_data)
                max_quantity -= 1

    def update(self, instance, validated_data):
        # выталкиваем все данные связанных таблиц
        ingredients_got = validated_data.pop('ingredients', None)
        cook_stages_got = validated_data.pop('cook_stages', None)
        tags_got = validated_data.pop('tags', None)

        self.partial_update_nested_multiple(instance, Ingredient, ingredients_got, self.max_ingredients)
        self.partial_update_nested_multiple(instance, CookStage, cook_stages_got, self.max_cook_stages)
        self.partial_update_nested_multiple(instance, Tag, tags_got, self.max_tags)

        instance.title = validated_data.get('title', instance.title)
        instance.portions = validated_data.get('portions', instance.portions)
        instance.cook_time = validated_data.get('cook_time', instance.cook_time)
        instance.weight = validated_data.get('weight', instance.weight)

        # удаляем предыдущее изображение
        avatar_got = validated_data.get('avatar', None)
        if avatar_got:
            # метод не выбрасывает исключений
            instance.avatar.delete(save=True)
            instance.avatar = avatar_got

        instance.save()
        return instance



##### Сериализаторы оценок #####

# (для создания или редактирования оценки рецепта)
class RecipeGradeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeGrade
        fields = ['grade']

    def create(self, validated_data):
        new_grade = RecipeGrade.objects.create(
            **validated_data,
            evaluator=self.context['evaluator'],
            recipe=Recipe.objects.get(id=self.context['recipe_id']))
        return new_grade

    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', instance.grade)
        instance.status = 'A'
        instance.save()
        return instance


# (для создания или редактирования оценки комментария)
class CommentGradeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentGrade
        fields = ['grade']

    def create(self, validated_data):
        new_grade = CommentGrade.objects.create(
            **validated_data,
            evaluator=self.context['evaluator'],
            comment=Comment.objects.get(id=self.context['comment_id']))
        return new_grade

    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', instance.grade)
        instance.status = 'A'
        instance.save()
        return instance