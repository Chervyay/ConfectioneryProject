from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from djoser.views import TokenDestroyView

urlpatterns = [
    path('login/', CustomTokenCreateView.as_view()),
    path('logout/', TokenDestroyView.as_view()),

    path('recipe_add/', recipe_add),
    path('recipes_by_title/<str:search_title>/', recipes_by_title),
    path('recipes_by_tag/<str:search_tag>/', recipes_by_tag),
    path('recipes_by_author/<str:search_author>/', recipes_by_author),
    path('recipes_all/', recipes_all),
    path('recipe_info/<str:pk>/', recipe_info),
    path('recipe_edit/<str:pk>/', recipe_edit),
    path('recipe_remove/<str:pk>/', recipe_remove),

    path('client_register/', client_reg),
    path('client_info/<str:pk>/', client_info),
    path('client_info/', client_self_info),
    path('client_recipes/', client_recipes),
    path('client_edit/', client_edit),
    path('client_password_change/', client_pass_change),

    path('comment_add/<str:recipe_pk>/', comment_add),
    path('comment_remove/<str:pk>/', comment_remove),

    path('recipe_grade_add/<str:recipe_pk>/', recipe_grade_add),
    path('recipe_grade_check/<str:recipe_pk>/', recipe_grade_check),
    path('recipe_grade_cancel/<str:recipe_pk>/', recipe_grade_cancel),

    path('comment_grade_add/<str:comment_pk>/', comment_grade_add),
    path('comment_grade_check/<str:comment_pk>/', comment_grade_check),
    path('comment_grade_cancel/<str:comment_pk>/', comment_grade_cancel)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('recipe_grade_inverse/<str:recipe_pk>/', recipe_grade_inverse),
# path('comment_grade_inverse/<str:comment_pk>/', comment_grade_inverse),

# path('Recipes/random/<str:quantity>/', recipes_random),