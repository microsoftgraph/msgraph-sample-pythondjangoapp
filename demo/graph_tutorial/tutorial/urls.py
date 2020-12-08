# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from django.urls import path

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.home, name='signin'),
  path('signout', views.home, name='signout'),
  path('calendar', views.home, name='calendar'),
]
