from django.urls import path, include

urlpatterns = [
    path('', include('app.urls.common')),
    path('upravljanje/', include('app.urls.admin')),
    path('asistent/', include('app.urls.asistent')),
    path('student/', include('app.urls.student')),
]