# yatube_project
Социальная сеть блогеров

Учебный проект

### Настройка проекта

Для настройки проекта выполните следующие шаги:

1. Клонируйте репозиторий:
git clone
2. Перейдите в директорию проекта
3. Скопируйте `.env.example` в новый файл `.env` и заполните необходимые значения переменных окружения:
cp .env.example .env ([Как заполнить переменные окружения?](#Description_env) )
4. Установите зависимости: 
```pip install -r requirements.txt```
5. Выполните миграции:
```python manage.py migrate```
6. Запустите проект:
```python manage.py runserver```


#### <a id="Description_env">Описание переменных окружения</a>
SECRET_KEY - для его получения необходимо запустить следующий код Python: 
```python
from django.core.management.utils import get_random_secret_key  
print(get_random_secret_key())
```

## Что может проект

http://localhost:8000/swagger/

