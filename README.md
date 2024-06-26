# // 1561 PROJECTS //
Cервис для поиска единомышленников для совместного выполнения проектов разного уровня сложности.


## Проблема
Довольно часто в жизни людей возникает проблема нехватки опыта, знаний и навыков работы с чем-либо. При работе над каким-либо проектом это становится настоящим препятствием: для продолжения работы автору необходимо либо изучить вопрос самостоятельно, либо найти человека, который уже разобрался и готов помогать.

## Решение
Сервис, который в разы упрощает поиск специалистов для работы над проектами авторам проектов, а заинтересованным людям позволяет найти интересный проект, предложить свою помощь и работать над ним вместе с его автором. 
<br>
Сервис представляет собой сайт, на котором пользователи могут создавать и обмениваться проектами, а также искать людей в команду.

> Данный сайт получил своё название по номеру школы, в которой он представлен

## Функционал
#### Основной функционал сайта:
1. Вход и регистрация пользователей.
2. Редактирование профиля с дополнительными полями.
3. Создание проектов, исследований или идей, возможность добавить к ним вакансии, а при создании - воспользоваться ИИ функциями.
4. Взаимодействие с проектами: оценки, добавление в избранное.
5. Поиск пользователей и проектов с удобными фильтрами.
6. Автоматическая сортировка по самым оцениваемым в поиске проектов и по количеству проектов в поиске пользователей.
7. Система тегов для пользователей и проектов.
8. Просмотр проектов, редактирование и удаление.
9. Множество других мелких функций.


## Установка и запуск

1. **Убедитесь, что у вас установлен Python версии 3.6 и выше.** Сайт разрабатывался и тестировался на версии Python 3.10.
2. **Убедитесь, что у вас установлен и настроен PostgreSQL на вашем компьютере или сервере, а также создан пользователь.**
3. **Клонирование репозитория.** Измените _<путь/до/папки>_ на путь к папке, в которую необходимо клонировать проект.
    
    ```bash
    git clone https://github.com/stepannovoselov/project-exchange-website.git <путь/до/папки>
    ```
4. **Переход в директорию проекта.** Измените _<путь/до/папки/проекта>_ на путь к папке, в которую был сохранён проект.
    
    ```bash
    cd <путь/до/папки/проекта>
   ```
5. **Установка зависимостей.**
    
    ```bash
    pip install -r requirements.txt
    ```
6. **Создание файла .env.** Создайте файл ```.env``` в корневой директории проекта и заполните указанной ниже информацией.

    ```
    POSTGRES_USERNAME='<postgres username>'
    POSTGRES_PASSWORD='<postgres password>'
    POSTGRES_HOST='<postgres host>'
    POSTGRES_PORT='<postgres port>'
    POSTGRES_DATABASE='<postgres database name>'
    
    FLASK_APP_SECRET_KEY='<app secret key>'
    FLASK_DEBUG_MODE=False
    FLASK_PORT=5000
    FLASK_HOST='localhost'
   
    DEFAULT_SESSION_TIME_SECONDS=3600
    LONG_SESSION_TIME_SECONDS=7200
    
    SALT_FOR_USERS_COLOR_GENERATOR='get'
    SALT_FOR_PROJECTS_COLOR_GENERATOR='pull'
   
    LOG_FILE_PATH='logs.log'
    ```
    
    * Замените `<postgres username>`, `<postgres password>`, `<postgres host>`, `<postgres port>`, `<postgres database name>` на соответствующие значения вашей базы данных PostgreSQL.
    * Замените `localhost` на адрес вашего сервера или оставьте это значение без изменений, чтобы сайт был запущен локально.
    * Замените `<app secret key>` на любую последовательность символов в качестве ключа шифра для данных пользователя в браузере.
    * Вы можете изменить значение переменной `FLASK_PORT` с `5000` (по умолчанию) для изменения порта, на котором будет работать сайт.


7. **Инициализация базы данных.**
   
   ```bash
   flask db init
   ```

8. **Обновление базы данных.**
   ```bash
   flask db migrate
   ```
   ```bash
   flask db upgrade
   ```

9. **Дополнительная настройка.** Вы можете пропустить этот пункт, чтобы сохранить значения по умолчанию.
   * **Настройка времени сессии пользователя.**
     * Откройте ранее созданный вами файл `.env`.
     * Найдите в файле значения `DEFAULT_SESSION_TIME_SECONDS` и `LONG_SESSION_TIME_SECONDS`.
     * `DEFAULT_SESSION_TIME_SECONDS` - время обычной сессии; `LONG_SESSION_TIME_SECONDS` - время сессии, если пользователь нажал «Запомнить меня».
     * Измените значения по умолчанию в секундах на ваши значения, указанные также в секундах.
       
   * **Настройка ключей (salt) генерации цвета из строк.**
     * Откройте ранее созданный вами файл `.env`.
     * Найдите в файле значения `SALT_FOR_USERS_COLOR_GENERATOR` и `SALT_FOR_PROJECTS_COLOR_GENERATOR`.
     * `SALT_FOR_USERS_COLOR_GENERATOR` - ключ для генерации цвета для пользователей; `SALT_FOR_PROJECTS_COLOR_GENERATOR` - ключ для генерации цвета для проектов.
     * Измените значения по умолчанию на ваши.
     * Изменяя ключи вы меняете входные данные для алгоритма генерирования цвета. За счёт этого вы получаете разные цвета элементов на странице при разных значениях ключей.
   
   * **Настройка файла с информацией для отладки**
     * Откройте ранее созданный вами файл `.env`
     * Найдите в файле значение `LOG_FILE_PATH`
     * Измените значение по умолчанию на путь к файлу с логами с расширением `.log` или оставьте значение пустым, чтобы информация для отладки не записывалась в файл.


10. **Запуск.** Теперь проект готов к запуску. Чтобы запустить сайт, запустите файл `app.py` или выполните следующую команду.

       ```bash
       python app.py
       ```

11. **Просмотр результата.**
   
       После запуска файла `app.py` сайт будет запущен по адресу `http://localhost:5000`.
       <br><br>
       Учтите, что, если на этапе `5` вы изменили переменную `FLASK_PORT`, то вместо `5000` вам необходимо указать выбранный вами порт в адресе: `http://localhost:<ваш порт>`

