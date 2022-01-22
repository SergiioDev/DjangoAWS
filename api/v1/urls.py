from django.urls import include, path

urlpatterns = [
    path('users/', include('api.v1.users.urls')),
    path('organizations/', include('api.v1.organizations.urls')),
]
