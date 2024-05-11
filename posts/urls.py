from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Страница с постами, отфильтрованными по группам
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # Добавление поста
    path('create/', views.create_post, name='post_create'),
    # редактирование поста
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    # добавление комментария
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
