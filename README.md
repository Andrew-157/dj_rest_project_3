# DJANGO REST FRAMEWORK API for publishing recipes

### Introduction
This API allows users to share their culinary recipes of particular category(like soups, desserts, etc.) with others. Users can rate recipes and leave their reviews on each recipe.

### Features 
* Users can register and login into their accounts.
* Each user can have a profile image(however, this is not obligatory).
* Authenticated users can publish, update and delete recipes.
* Authenticated users can publish up to 3 images for each of their recipes(as well as delete them).
* Authenticated users can publish, update and delete ratings for recipes.
* Authenticated users can publish, update and delete reviews for recipes.
* Admin users create categories. Users than choose category in which they want to publish their recipe.
* Users(authenticated as well as non-authenticated users) can view all categories available, all recipes, all ratings, all reviews and all authenticated users(except admins) with their recipes


### Project structure
Project consists of two apps:
- recipes
- users

`recipes` app manages all operations for reading, publishing, updating and deleting recipes, ratings and reviews. Also this app allows to see all authenticated users(except admin) with their recipes.

`users` app contains CustomUser model and serializers for this model:serializer for creating new user and and their representation(these serializers are only used in endpoints for authentication). Any other manipulations with authentication are handled by `djoser` package.

### Installation

Clone repository, using command:
```
    git clone https://github.com/Andrew-157/dj_rest_project_3
```

Then, use command:
```
    cd dj_rest_project_3
```

**Everything shown below assumes you are working from directory `dj_rest_project_3`**

Required packages:
```
    django==4.2.4
    djangorestframework==3.14.0
    mysqlclient==2.2.0
    django-environ==0.10.0
    pillow==10.0.0
    drf-nested-routers==0.93.4
    django-cleanup==8.0.0
    django-filter==23.2
    djoser==2.2.0
    djangorestframework-simplejwt==5.2.2
    django-debug-toolbar==4.1.0
    autopep8==2.0.2
```

If you are using `pipenv` for managing virtual environments, in command line run:
```
    pipenv install
```
And then to activate environment run:
```
    pipenv shell
```

You can also use file `requirements.txt` with pip.
Inside your activated virtual environment, run:
```
    pip install -r requirements.txt
```
For `Windows`
```
    pip3 install -r requirements.txt
```
For `Unix`-based systems

### Run project

**The following steps show how to run project locally(i.e., with DEBUG=True)**

Generate `SECRET KEY` for your project, using the following code:
```python
    import secrets

    secret_key = secrets.token_hex(34)

    print(secret_key)
```

In directory `api` create file `.env`(**check that this file is in `.gitignore`**) and the following line:
```
    SECRET_KEY=<your_secret_key>
```

Then you need to create MySQL database(using MySQL Workbench or any other tool), using `SQL` statement:
```SQL
    CREATE DATABASE <your_database_name>;
```

Next, go to `.env` and, using your database credentials, add the following lines:
```
    DB_NAME=<your_database_name>
    DB_USER=<your_database_user>
    DB_PASSWORD=<your_database_password>
    DB_HOST=<your_database_host>
    DB_PORT=<your_database_port>
```

After that, in command line run:
```
    python manage.py migrate
    python manage.py runserver
```
For `Windows`
```
    python3 manage.py migrate
    python3 manage.py runserver
```
For `Unix`-based systems