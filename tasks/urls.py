from django.conf.urls import url
import tasks.views as views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard")
]
