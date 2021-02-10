# Django-Sample

### 建立 Django Project
安裝 Django
```text
pipenv install django
```

建立 Django Project
```text
django-admin startproject django_sample
```

執行 Django
```text
python manage.py runserver
```

即可啟動 Django

**可以把django_sample/django_sample改成django_sample/main比較好辨識。**

### 建立 Django App
通常依照功能建立一個app，例如：建立一個Todo List的app
```text
python manage.py startapp todoList
```
執行之後會出現todoList的資料夾。接著要將建立的app加入main/setting內INSTALLED_APPS中：
```text
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todoList' // 新增這行
]
```
#### 建立 Views
到todoList/views.py內新增以下程式碼。
```python
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello World!")

```
#### 設定 URLconf
到main/urls.py內設定剛剛建立的view
```python
from django.conf.urls import url
from django.contrib import admin
from todoList.views import hello_world


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', hello_world),
]
```

#### 建立 Templates
現在要來用templates建立畫面，在main/templates/新增index.html。如果沒有templates的資料夾，就自行新增一個。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!-- 透過views.py將值傳入-->
    {{data}} 
    <em>{{ current_time }}</em>
</body>
</html>
```
接著到main/setting.py內更改templates的設定。
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
        # 'DIRS': [] 把這行改成上面那行
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
到todoList/views.py內新增以下程式碼。
```python
from django.shortcuts import render
from datetime import datetime


def hello_html(request):
    return render(request, 'index.html', {
        'data': 'hello html!!!', # 回傳給剛剛設定html內的{{data}}
        'current_time': str(datetime.now()), # 回傳給剛剛設定html內的{{current_time}}
    })
```
再回到到main/urls.py內設定
```python
from django.conf.urls import url
from django.contrib import admin
from todoList.views import hello_world, hello_html # 新增 hello_html


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', hello_world),    
    url(r'^hello_html/', hello_html), # 新增 url

]

```

#### 設定 Models
Django Model 在定義資料庫的結構（schema），並透過 Django 指令創建資料庫、資料表及欄位。
優點：轉換資料庫相當方便

到main/setting.py內設定資料庫，python預設是SQLite。
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',         # 資料庫引擎
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),   # 資料庫名稱
    }
}
```

到todoList/model.py內宣告一個class，並定義屬性。Django 會依據這個建立資料表，以及資料表裡的欄位設定：
```python
from django.db import models


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "todo_list"

```
接著來同步資料庫：
```
python manage.py makemigrations
---
Migrations for 'todoList':
  todoList/migrations/0001_initial.py
    - Create model TodoList
```
```
python manage.py migrate
---
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, todoList
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying todoList.0001_initial... OK

```
makemigrations ： 會幚你建立一個檔案，去記錄你更新了哪些東西。
migrate ： 根據 makemigrations 建立的檔案，去更新你的 DATABASE 。

建立完成後可以使用SQLiteBrowser觀看DB，會發現多了一個todo_list的table

#### Django ORM
使用python shell試試看
```
python manage.py shell
```
*註：如果直接打`python`進去的話，會抓不到django設定的環境變數。*

新增一筆資料：
```
>>> from todoList.models import TodoList 
>>> TodoList.objects.create(title='study django', description='create django project')
<TodoList: TodoList object (1)>
```
先將TodoList import進來，接著新增一筆資料，就可以到SQLiteBrowser查看是否有成功。剩餘的就不在這麼多做敘述，之後會講完整程式碼寫出來。


*註：如果要退出python shell的話輸入`exit()`即可。*

#### Django Admin
Django 內建有後台管理介面。我們可以透過 Django Admin 看到實際的資料，並跟資料庫進行互動。在建立時基本上就會產生好設定，若沒有的話，可以照以下步驟做設定。

在 main/setting.py 內的 INSTALLED_APPS 加入下方設定：
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    ...
)
```
在 main/urls.py 設定管理後台的 URL：
```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 略
]
```
基本上這樣設定就完成了。接下來就是建立 superuser。在 Terminal輸入：
```text
python manage.py createsuperuser

--- 以下自訂 ---
Username (leave blank to use 'YOUR_NAME'):
Email address: your_name@yourmail.com
Password:
Password (again):
Superuser created successfully.
```

連至 http://127.0.0.1:8000/admin，可以看到管理後台的登入頁面。

在 todoList/admin.py 註冊 model，讓後台可以看到 DB。

```python
from django.contrib import admin
from .models import TodoList

admin.site.register(TodoList)
```
現在回到管理後台，就可以看到 todoList 的 table。