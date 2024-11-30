
  
![pipeline](https://gitlab.crja72.ru/django_2023/projects/business-manager_14/badges/main/pipeline.svg)    
  
# TaskPulse  
  This is documentation of "__TaskPulse__" project - web-based BPM-system, which was created as a final     
qualifying work for ["Specialisations of Yandex Lyceum"](https://yandex.ru/support2/lyceum/ru/common-concepts/specialization) educational project.    
    
Following description is divided to 3 parts:     
* [User Manual](#user-manual) - how to use, what it can    
* [Instruction for launching](#launching-instruction) the application in dev-mode    
* [Documentation](#developer-docs) for devs     
    
# User Manual    
 # Launching instruction 
 ## Установка виртуального окружения 
 ```sh 
 python -m venv venv  
``` 
## Активация виртуального окружения 
```sh 
venv\Scripts\activate 
``` 
## Установка зависимостей для работы с проектом 
```sh 
pip install -r requirements/dev.txt  
``` 

Для корректной работы проекта в продакшен-среде достаточно установки prod.txt    

```sh 
pip install -r requirements/prod.txt  
```    
 для тестирования проекта    
```
sh pip install -r requirements/test.txt  
``` 
## Настройка переменных виртуального окружения 
#### Создайте файл ".env" в корневой директории вашего проекта. Скопируйте в этот файл переменные из ".env.template", изменив данные в них на свои. Этих переменных хватит для корректного запуска проекта. ## Компиляция сообщений для перевода: 
```sh 
django-admin makemessages -l endjango-admin makemessages -l rudjango-admin compilemessages  
``` 
## Создание миграций и их применение: 
```sh 
python manage.py makemigrationspython manage.py migrate  
``` 
## Запуск проекта в dev-режиме 
```sh 
python manage.py runserver  
```    
 # Developer Docs 

Here you will find documentation for developers - for     
following improvement and/or easier usage of it's parts in    
other projects :)  
  
####GENERAL OVERVIEW  
This is documentation of "TaskPulse" project - web-based BPM-system, which was created as a project for "Specialisations of Yandex Lyceum" educational project.   
  
It is cleaved to four basic applications: homepage, users, stats, workplace and core (which contains some instruments, used in various apps of the project described).   
  
Lower you will see a short description of each, for further exploration scroll the documentation down to sections, related to the app you are interested in.  
  
[HOMEPAGE]()  
  
Handles views for the homepage: first site-cover and a few other views, not related to the main funcionallity specifically.   
  
[STATS]()  
  
Handles functionallity, related to extracting statistics about employee performance and information about company in general; information tracked about users (which may be used later for analysis by managers) includes speed of tasks completion and amount of tasks completed.  
  
[WORKPLACE]()  
  
main web-app logic: pages for giving, reviewing and marking tasks, "statistcs" page for managers and owners, company settings for owner, etc.  
  
[USERS]()  
  
Handles manipulation with user information in general - login/signin, user settings (related not to any company specifically, but to users themselves), inviting new users to company, etc.  
  
[CORE](#core)  
Provides some software functionality, which is used over the project in different applications, to be specific - useful mixins for class-based views, related to users' authorization and authentification. Comprehensive description is lower.  
  
  
  
### CORE  

core contains some mixins those are used along the project, in different apps. Mixins are classes, those are used for class-based view inheritance (and, thus, adding some specific qualities to them).   
Mixins provided are:  
  
* GiveCompanyUserToContext  
  
passes company_user variable to the context if the view; company_user is an object of CompanyUser table - see details in WORKPLACE MODELS reference.   
USED TO FROM "CompanyUserRequiredMixin"  
  
  
* BaseCompanyUserRequiredMixin  
  
Provides functionallity to check whether authorized user has required role to view some company's folds - via method "test_func", which takes list of allowed positions (all three by default) as an argument "roles".  
USED TO FROM "CompanyUserRequiredMixin"  
  
  
* CompanyUserRequiredMixin   
  
combination of GiveCompanyUserToContext and BaseCompanyUserRequiredMixin mixins.  
  
  
* CompanyManagerRequiredMixin/CompanyOwnerRequiredMixin   
  
"syntactic sugar", shells for "CompanyUserRequiredMixin" which require positions "manager and higher" and "owner" respectfully in order to access some special View.  
  
[Back to dev-docs](#developer-docs)  
  
[Back to the beginning](#taskpulse)