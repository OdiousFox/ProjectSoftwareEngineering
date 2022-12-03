from django.urls import path
from . import views
urlpatterns = [
    path('',views.init,name='init'),
    path('api/',views.fetch_api,name='api')
]