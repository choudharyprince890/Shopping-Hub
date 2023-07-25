from django.contrib import admin
from django.urls import path


from.import views
# from views import FindProduct

urlpatterns = [
    path('',views.designclothes,name='designclothes'),
]