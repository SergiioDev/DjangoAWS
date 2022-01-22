from django.urls import path
from . import views
urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>', views.UserRetrieveUpdateDestroy.as_view()),
    path('register', views.UserRegister.as_view())
]
