# Тестовое задание для IT Power
## Развёртывание проекта локально или на сервере:
Склонируйте проект на пк/сервер.
Запустите Docker.
Находясь в папке с файлом  ```docker-compose.yml``` запустите команду  ```docker-compose up -d --build```.
После успешной сборки введите команду  ```docker container ls```, найдите контейнер с бэкендом, скопируйте его ID и вставьте в следующую команду  ```docker exec -ti *ID* sh```.
Находясь внутри контейнера с бэкендом создайте миграции и примените их.
 ```python manage.py makemigrations users```
 ```python manage.py makemigrations todolists```
 ```python manage.py migrate```
Создайте Суперпользователя командой:
 ```python manage.py createsuperuser```
И введите поля  ```email``` и  ```password```
Вы Великолепны!
## Взаимодействие с API:
### Регистрация:
На эндпоинт /api/v1/users/ с помощью POST запроса отправьте 4 поля:
#### email (str)
#### password (str)
#### first_name (str)
#### last_name (str)
Вы зарегистрированы!
### Получение Токена:
На эндпоинт /api/v1/obtain_token/ с помощью POST запроса отправьте 2 поля СУЩЕСТВУЮЩЕГО АККАУНТА:
#### email (str)
#### password (str)
### Использование токена:
Для примера я буду использовать программу Postman.
В заголовках запроса укажите ключ (key) "Authorization"
В поле значение (value) заголовка с ключом "Authorization" введите "Token "Ваш токен"". Токен может быть получен на предыдущем шаге.
### Просмотр Тэгов:
На эндпоинт /api/v1/tags/ отправьте GET запрос, в ответ придут все созданные тэги.
### Создание Дела (Case):
На эндпоинт /api/v1/cases/ с помощью POST запроса отправьте 4 поля:
#### title (str)
#### descriptions (str)
#### deadline (Дата в формате YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z])
#### tag (Необходимо отправить ID тэга, который можно получить выше.)
### Создание Списка дел (ToDoList):
На эндпоинт /api/v1/todolists/ с помощью POST запроса отправьте 2 поля:
#### title (str)
#### cases (ListField - необходимо отправить список, содаржащий ID созданных вами Дел)
### Чтобы завершить Дело (Case) вам необходимо:
Перейти на эндпоинт /api/v1/cases/"ID"/solve/, где ID это ID дела, которое вы хотите завершить.
Отправить на этот эндпоинт POST запрос.
### Фильтрация Дел по Тэгам и Названию:
#### Фильтрация по Тэгам:
На эндпоинт /api/v1/cases?tag="тэг" отправьте запрос, вставив после знака "=" существующий тэг.
#### Фильтрация по Названию:
На эндпоинт /api/v1/cases?title="название" отправьте запрос, вставив после знака "=" строку, чтобы найти совпадение по Делам пользователя.
## Вы Великолепны!
