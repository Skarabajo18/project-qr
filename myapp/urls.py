from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('signup/', views.signup, name='signup'),
    # ----- Ckeditor -----
    path('', views.postList, name='postList'),
    path('post/<str:pk>/', views.post, name="post"),
    path('edit/<str:pk>', views.editPost, name='editUrl'),
    path('form-post/', views.insertPost, name='form-post'),
    path('search/', views.search, name='search'),

]
