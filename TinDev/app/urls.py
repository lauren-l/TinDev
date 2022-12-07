from django.urls import path
from . import views
from .views import UpdatePosts

app_name = 'app'

urlpatterns = [
    # path('', views.HomeView.as_view(), name='index'),
    path('home/', views.home),
    path('logout', views.logout_user),
    path('signup_candidate', views.signup_candidate),
    path('signup_recruiter', views.signup_recruiter),
    path('recruiter_dashboard', views.dashboard_recruiter),
    path('candidate_dashboard', views.dashboard_candidate),
    path('candidate_offers', views.candidate_offers),
    path('submit_application', views.submit_application),
    path('view_applicants', views.view_applicants),
    path('offer_response', views.offer_response),
    path('create_posts', views.create_posts),
    path('delete_posts/<int:pk>', views.delete_posts),
    path('update_posts/<int:pk>', views.update_posts, name='update_posts')
    # path('update_posts/<int:pk>', UpdatePosts.as_view(), name='update_posts')
]