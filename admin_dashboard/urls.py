from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_create_user/', views.user_create, name='admin_create_user'),
    path('<int:user_id>', views.user_details, name='admin_user_details'),
    path('<int:user_id>/update/', views.UserModelUpdateView.as_view(), name='admin_user_update'),
    path('<int:user_id>/delete/', views.UserModelDeleteView.as_view(), name='admin_user_delete'),
]