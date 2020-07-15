from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
# from django.contrib.auth import

from bases.views import home, HomesinPrivilegios

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bases/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='bases/login.html'),
         name='logout'),
    path('sin_privilegios/', HomesinPrivilegios.as_view(), name='sin_privilegios'),

    path('reset/rpk_srl', auth_views.PasswordResetView.as_view(template_name='bases/password_reset_form.html', email_template_name='bases/password_reset_email.html', success_url=reverse_lazy('bases:password_reset_done')),
         name='reset', ),

    path('reset/password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='bases/password_reset_done.html'),
         name='password_reset_done'),


     # #re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='bases/password_reset_confirm.html', success_url=reverse_lazy('bases:password_reset_complete')),
         name='password_reset_confirm'),

    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='bases/password_reset_complete.html' ),
         name='password_reset_complete'),
]
