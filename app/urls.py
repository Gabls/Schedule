from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('users', views.readUsers, name="users"),
    path('users/updateUser', views.updateUser, name="updateUser"),
    path('users/deleteUser', views.deleteUser, name="deleteUser"),

    path('exitEvent', views.exitEvent, name="exitEvent"),
    path('updateEvent', views.updateEvent, name="updateEvent"),
    path('deleteEvent', views.deleteEvent, name="deleteEvent"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
