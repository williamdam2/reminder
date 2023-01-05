from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/',include('authentication.urls')),
    path('reminder/',include('reminder.urls')),
    path('',RedirectView.as_view(url='reminder'))
    ]
