from django.urls import path

from . import views
app_name = 'app'

urlpatterns = [
    # path('', views.HomeView.as_view(), name='index'),
    path('home/', views.home),
    path('logout', views.logout_user),
    path('signup_candidate', views.signup_candidate),
    path('signup_recruiter', views.signup_recruiter),
    path('recruiter_dashboard', views.dashboard_recruiter)
]