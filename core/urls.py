from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    path('register/',views.register,),
    path('', views.get_task),
    path('<int:pk>/', views.get_task),
    path("<int:pk>/", views.get_task)

]
