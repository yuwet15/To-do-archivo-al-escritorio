from django.urls import path

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('crear_csv', views.crear_csv, name='crear_csv'),
  path('callback', views.callback, name='callback')
]