from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrganizationListCreate.as_view()),
    path('<int:pk>/', views.OrganizationRetrieveUpdateDestroy.as_view())
]
