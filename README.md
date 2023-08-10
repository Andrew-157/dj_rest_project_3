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
    django
    djangorestframework
    mysqlclient
    django-environ
    pillow
    drf-nested-routers
    django-cleanup
    django-filter
    djoser
    djangorestframework-simplejwt
    django-debug-toolbar
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
[#1589F0](https://placehold.co/15x15/1589F0/1589F0.png) For Windows
```
    pip3 install -r requirements.txt
```
[#1589F0](https://placehold.co/15x15/1589F0/1589F0.png) For Unix-based systems