from django.contrib import admin
from django.urls import path



from .views import Index,Cart,Login, CheckOut


from.import views

urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/',Cart.as_view() , name='cart'),
    path('check-out',CheckOut.as_view() , name='checkout'),
    path('recommend',views.recommend , name='recommend'),
]
