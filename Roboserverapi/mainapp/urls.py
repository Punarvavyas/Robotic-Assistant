from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import RoboUserShowView

#app_name = ""
urlpatterns = [
    url(r'RoboUser/$',RoboUserShowView.as_view(),name='UserShow'),
]