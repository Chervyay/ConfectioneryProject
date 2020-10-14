from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('recipes_by_title/<str:search_title>/', recipes_by_title),
    path('recipes_by_tag/<str:search_tag>/', recipes_by_tag),
    path('recipes_by_author/<str:search_author>/', recipes_by_author),
    path('recipes_all/', recipes_all),
    path('recipe_add/', recipe_add),
    path('recipe_info/<str:pk>/', recipe_info),

    path('client_recipes/<str:pk>/', client_recipes),
    path('client_register/', client_reg),
    path('client_info/<str:pk>/', client_info),

    path('comment_add/<str:recipe_pk>/', comment_add),

    path('recipe_grade_add/<str:recipe_pk>/', recipe_grade_add),
    path('comment_grade_add/<str:comment_pk>/', comment_grade_add),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('Recipes/random/<str:quantity>/', recipes_random),