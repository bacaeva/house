
from django.urls import path, include

from .views import RegisterView, ActivateView, LogoutView, LoginView, ChangePasswordView

# ChangePasswordView, ForgotPassword, \
    # ForgotPasswordComplete

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('forgot_password/', ForgotPassword.as_view()),
    # path('forgot_password_complete/', ForgotPasswordComplete.as_view()),

]