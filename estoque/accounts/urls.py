from django.urls import path
from .views import login_view, logout_view, profile_view, change_password

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password, name='change_password'),
]
