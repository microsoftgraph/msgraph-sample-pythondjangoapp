<!-- markdownlint-disable MD002 MD041 -->

In this exercise you will use [Django](https://www.djangoproject.com/) to build a web app. If you don't already have Django installed, you can install it from your command-line interface (CLI) with the following command.

```Shell
pip install Django=2.2.2
```

Open your CLI, navigate to a directory where you have rights to create files, and run the following command to create a new Django app.

```Shell
django-admin startproject graph_tutorial
```

Django creates a new directory called `graph_tutorial` and scaffolds a Django web app. Navigate to this new directory and enter the following command to start a local web server.

```Shell
python manage.py runserver
```

Open your browser and navigate to `http://localhost:8000`. If everything is working, you will see a Django welcome page. If you don't see that, check the [Django getting started guide](https://www.djangoproject.com/start/).

Now that you've verified the project, add an app to the project. Run the following command in your CLI.

```Shell
python manage.py startapp tutorial
```

This creates a new app in the `./tutorial` directory. Open the `./graph_tutorial/settings.py` and add the new `tutorial` app to the `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tutorial',
]
```

In your CLI, run the following command to initialize the database for the project.

```Shell
python manage.py migrate
```

Add a [URLconf](https://docs.djangoproject.com/en/2.1/topics/http/urls/) for the `tutorial` app. Create a new file in the `./tutorial` directory named `urls.py` and add the following code.

```python
from django.urls import path

from . import views

urlpatterns = [
  # /tutorial
  path('', views.home, name='home'),
]
```

Now update the project URLconf to import this one. Open the `./graph_tutorial/urls.py` file and replace the contents with the following.

```python
from django.contrib import admin
from django.urls import path, include
from tutorial import views

urlpatterns = [
    path('tutorial/', include('tutorial.urls')),
    path('admin/', admin.site.urls),
]
```

Finally add a temporary view to the `tutorials` app to verify that URL routing is working. Open the `./tutorial/views.py` file and add the following code.

```python
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
  # Temporary!
  return HttpResponse("Welcome to the tutorial.")
```

Save all of your changes and restart the server. Browse to `http://localhost:8000/tutorial`. You should see `Welcome to the tutorial.`

Before moving on, install some additional libraries that you will use later:

- [Requests-OAuthlib: OAuth for Humans](https://requests-oauthlib.readthedocs.io/en/latest/) for handling sign-in and OAuth token flows, and for making calls to Microsoft Graph.
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) for loading configuration from a YAML file.
- [python-dateutil](https://pypi.org/project/python-dateutil/) for parsing ISO 8601 date strings returned from Microsoft Graph.

Run the following command in your CLI.

```Shell
pip install requests_oauthlib==1.2.0
pip install pyyaml==5.1
pip install python-dateutil==2.8.0
```

## Design the app

Start by creating a templates directory and defining a global layout for the app. Create a new directory in the `./tutorial` directory named `templates`. In the `templates` directory, create a new directory named `tutorial`. Finally, create a new file in this directory named `layout.html`. The relative path from the root of your project should be `./tutorial/templates/tutorial/layout.html`. Add the following code in that file.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Python Graph Tutorial</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"
      integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.1.0/css/all.css"
      integrity="sha384-lKuwvrZot6UHsBSfcMvOkWwlCMgc0TaWr+30HWe3a4ltaBwTZhyTEggF5tJv8tbt" crossorigin="anonymous">
    {% load static %}
    <link rel="stylesheet" href="{% static "tutorial/app.css" %}">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"
      integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"
      integrity="sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T" crossorigin="anonymous"></script>
  </head>

  <body>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <div class="container">
        <a href="{% url 'home' %}" class="navbar-brand">Python Graph Tutorial</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
          aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a href="{% url 'home' %}" class="nav-link{% if request.resolver_match.view_name == 'home' %} active{% endif %}">Home</a>
            </li>
            {% if user.is_authenticated %}
              <li class="nav-item" data-turbolinks="false">
                <a class="nav-link{% if request.resolver_match.view_name == 'calendar' %} active{% endif %}" href="#">Calendar</a>
              </li>
            {% endif %}
          </ul>
          <ul class="navbar-nav justify-content-end">
            <li class="nav-item">
              <a class="nav-link" href="https://developer.microsoft.com/graph/docs/concepts/overview" target="_blank">
                <i class="fas fa-external-link-alt mr-1"></i>Docs
              </a>
            </li>
            {% if user.is_authenticated %}
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">
                  {% if user.avatar %}
                    <img src="{{ user.avatar }}" class="rounded-circle align-self-center mr-2" style="width: 32px;">
                  {% else %}
                    <i class="far fa-user-circle fa-lg rounded-circle align-self-center mr-2" style="width: 32px;"></i>
                  {% endif %}
                </a>
                <div class="dropdown-menu dropdown-menu-right">
                  <h5 class="dropdown-item-text mb-0">{{ user.name }}</h5>
                  <p class="dropdown-item-text text-muted mb-0">{{ user.email }}</p>
                  <div class="dropdown-divider"></div>
                  <a href="#" class="dropdown-item">Sign Out</a>
                </div>
              </li>
            {% else %}
              <li class="nav-item">
                <a href="#" class="nav-link">Sign In</a>
              </li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>
    <main role="main" class="container">
      {% if errors %}
        {% for error in errors %}
          <div class="alert alert-danger" role="alert">
            <p class="mb-3">{{ error.message }}</p>
            {% if error.debug %}
              <pre class="alert-pre border bg-light p-2"><code>{{ error.debug }}</code></pre>
            {% endif %}
          </div>
        {% endfor %}
      {% endif %}
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

This code adds [Bootstrap](http://getbootstrap.com/) for simple styling, and [Font Awesome](https://fontawesome.com/) for some simple icons. It also defines a global layout with a nav bar.

Now create a new directory in the `./tutorial` directory named `static`. In the `static` directory, create a new directory named `tutorial`. Finally, create a new file in this directory named `app.css`. The relative path from the root of your project should be `./tutorial/static/tutorial/app.css`. Add the following code in that file.

```css
body {
  padding-top: 4.5rem;
}

.alert-pre {
  word-wrap: break-word;
  word-break: break-all;
  white-space: pre-wrap;
}
```

Next, create a template for the home page that uses the layout. Create a new file in the `./tutorial/templates/tutorial` directory named `home.html` and add the following code.

```html
{% extends "tutorial/layout.html" %}
{% block content %}
<div class="jumbotron">
  <h1>Python Graph Tutorial</h1>
  <p class="lead">This sample app shows how to use the Microsoft Graph API to access Outlook and OneDrive data from Python</p>
  {% if user.is_authenticated %}
    <h4>Welcome {{ user.name }}!</h4>
    <p>Use the navigation bar at the top of the page to get started.</p>
  {% else %}
    <a href="#" class="btn btn-primary btn-large">Click here to sign in</a>
  {% endif %}
</div>
{% endblock %}
```

Update the `home` view to use this template. Open the `./tutorial/views.py` file and add the following new function.

```python
def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context
```

Then replace the existing `home` view with the following.

```python
def home(request):
  context = initialize_context(request)

  return render(request, 'tutorial/home.html', context)
```

Save all of your changes and restart the server. Now, the app should look very different.

![A screenshot of the redesigned home page](./images/create-app-01.png)
