from django.urls import include, path

urlpatterns = [
    path('user/', include('api.v1.user.urls')),
    path('organization/', include('api.v1.organization.urls')),
]
