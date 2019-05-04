from django.contrib import admin
from django.conf.urls import url
#from api.views import home
#from api.views import ictal
#from api.views import interictal
#from api.views import stop
import api.views as views
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/',views.home, name = 'home'),
    url('ictal/',views.ictal, name = 'ictal'),
    url('inter/',views.interictal, name = 'inter'),
    url('stop/',views.stop, name = 'stop')
]
