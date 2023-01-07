# **API Yamdb**
Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
## Импорт данных
В проекте есть management команда, для импорта данных в базу из csv файлов.
Для справки необходимо в консоли использовать следующую команду:

    py manage.py importdata --help

## Документация
Документация доступна по ссылкам ниже после запуска проекта.
| Redoc |Swagger  |
|--|--|
| http://127.0.0.1:8000/redoc/ | http://127.0.0.1:8000/swagger/ |

[Также достпна полная документация в Redoc.yaml](https://github.com/pencool/api_yamdb/blob/master/api_yamdb/static/redoc.yaml)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/pencool/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов к API

### Регистрация:
Зарегистрироваться и получить email с кодом подтверждения для получения токена.
После отправки запроса на указанную почту придет письмо с кодом подтверждения и дальнейшими инструкциями для регистрации и получения токена.
- http://127.0.0.1:8000/api/v1/auth/signup/ - **ENDPOINT**


 #### **Запрос**:
 ```
{
"email": "user@example.com",
"username": "string"
}
```
 #### Ответ:
 ```
{
"email": "string",
"username": "string"
}
```
### Получение JWT-токена:
Для получения токена необходимо отправить запрос с именем пользователя и кодом подтверждения из письма отправленного на почту, в ответ будет выдан токен для авторизации.
- http://127.0.0.1:8000/api/v1/auth/token/ - **ENDPOINT**


 #### **Запрос**:
 ```
{
"username": "string",
"confirmation_code": "string"
}
```
 #### Ответ:
 ```
{
"token": "string"
}
```
### Получение списка всех произведений:
Получить список всех объектов. Права доступа: **Доступно без токена**.
- http://127.0.0.1:8000/api/v1/titles/ - **ENDPOINT**


 #### **Запрос**:
 ```

raw-data не требуется

```
 #### Ответ:
 ```
{
"count": 0,
"next": "string", 
"previous": "string",
"results": [
    -   {      
       "id": 0,    
       "name": "string",    
       "year": 0,  
       "rating": 0,   
       "description": "string",     
       "genre": [],     
       "category": {}      
        }     
    ]
}
```
