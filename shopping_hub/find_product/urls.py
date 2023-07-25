from django.contrib import admin
from django.urls import path


from.import views
# from views import FindProduct

urlpatterns = [
    path('',views.find_product,name='find_product'),
    # path('',FindProduct.as_view() , name='find_product'),
]