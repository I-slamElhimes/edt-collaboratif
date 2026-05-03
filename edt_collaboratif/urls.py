from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  

urlpatterns = [
    path('admin/',         admin.site.urls),
    path('dashboard/',     views.dashboard, name='dashboard'), 
    path('',               include('accounts.urls',      namespace='accounts')),
    path('events/',        include('events.urls',         namespace='events')),
    path('groups/',        include('groups.urls',         namespace='groups')),
    path('notifications/', include('notifications.urls',  namespace='notifications')),
    path('api/',           include('api.urls')),
    path('chatbot/',       include('chatbot.urls',        namespace='chatbot')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)