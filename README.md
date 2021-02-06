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

#### Models
Django Model 在定義資料庫的結構（schema），並透過 Django 指令創建資料庫、資料表及欄位。