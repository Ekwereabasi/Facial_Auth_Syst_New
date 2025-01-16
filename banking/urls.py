
from django.urls import path
from . import views 
from .views import register, dashboard, facial_login_test, MyLoginView, facial_login, UserListCreate, AccountDetail, TransactionListCreate, profile_view

urlpatterns = [
    path('', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('facial_login/', facial_login, name='facial_login'),
    path('facial-login-test/', facial_login_test, name='facial_login_test'),
    path('api/users/', UserListCreate.as_view(), name='user-list-create'),
    path('api/accounts/<int:pk>/', AccountDetail.as_view(), name='account-detail'),
    path('accounts/profile/', profile_view, name='profile'),
    path('api/transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),

]
