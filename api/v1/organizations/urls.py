from django.urls import include, path
from . import  views

urlpatterns = [
    path('', views.OrganizationAPI.as_view()),
    path('<int:pk>', views.OrganizationRetrieveUpdateDestroy.as_view())
]
