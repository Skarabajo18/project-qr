from django.contrib import admin
from django.urls import path, include
from myapp.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('logout/', logout_view, name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),

]
