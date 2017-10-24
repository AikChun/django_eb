from django.conf.urls import url
import tasks.views as views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^upload-file/$', views.upload_file, name="upload-file.html")
]
