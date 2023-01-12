from django.urls import path
from .views import UserLoginView, UserLogoutView, register_view, UsersListView, verification_user_view, \
    ProfilePageView, UserEditFormView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='new-list-url'), name='logout'),
    path('register/', register_view, name='register'),
    path('', UsersListView.as_view(), name='users-list'),
    path('verificate_user/<int:pk>/', verification_user_view, name='verification-user'),
    path('profile/<int:pk>/', ProfilePageView.as_view(), name='profile-page'),
    path('profile/edit/<int:user_id>/', UserEditFormView.as_view(), name='profile-edit'),
]
