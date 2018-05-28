from django.conf.urls import url

from . import apps
from . import views

urlpatterns = [
    url(r'^$', views.greeting, name='greeting'),
    url(r'(?P<line_index>[0-9]+)/$', apps.get_line_by_index),
]