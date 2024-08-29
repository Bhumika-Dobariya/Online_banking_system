from django.urls import path
from .views import get_all_user,create_user,update_user,delete_user_by_id,delete_user_by_token,get_user_by_id, verify_otp_and_login,user_register,get_user_by_token,get_all_user,update_user_by_token,forget_password,reset_password_by_token,user_login
urlpatterns = [
    path('get_all_user/', get_all_user, name='get_all_user'),
    path('create_user/', create_user, name='create_user'),
    path('update_user/<uuid:id>/', update_user, name='update_user'),
    path('delete_user/<uuid:id>/', delete_user_by_id, name='delete_user'),
    path('get_user_by_id/<uuid:id>/', get_user_by_id, name='get_user_by_id'),
    path('user_register/', user_register, name='user_register'),
    path('get_user_by_token/', get_user_by_token, name='get_user_by_token'),
    path('get_all_users/', get_all_user, name='get_all_users'),
    path('update_user_by_token/<uuid:id>/', update_user_by_token, name='update_user_by_token'),
    path('delete_user_by_token/<uuid:id>/', delete_user_by_token, name='delete_user_by_token'),
    path('forget_password/', forget_password, name='forget_password'),
    path('reset_password/', reset_password_by_token, name='reset_password_by_token'),
    path('user_login/', user_login, name='user_login'),
    path('verify_otp_and_login/', verify_otp_and_login, name='verify_otp_and_login')

]


