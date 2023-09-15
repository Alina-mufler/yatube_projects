from django.http import HttpResponse
from django.shortcuts import render

# Главная страница
def index(request):
    return HttpResponse('Привет, ты попал на главную страницу блога.\n'
                        'Надеюсь, тебе тут понравится!')


# Страница с постами, отфильтрованными по группам
def group_posts(request, pk):
    return HttpResponse(f'На данной странице ты можешь прочить посты группы {pk} ')

