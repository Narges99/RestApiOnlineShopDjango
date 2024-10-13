from django.urls import path
from .views import UserListView, UserCreateView, LoginUser, LogoutUser, UserRetrieveUpdateView, UserDeleteView

urlpatterns = [

    path('list/', UserListView.as_view(), name='user-list'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', LoginUser.as_view(), name='user-login'),
    path('logout/', LogoutUser.as_view(), name='user-logout'),
    path('update/', UserRetrieveUpdateView.as_view(), name='user-update'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),

]
