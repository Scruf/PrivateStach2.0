from django.conf.urls import url,include
from . import views



urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.registration, name='register'),
    url(r'^login/$', views.login_v, name='login'),
    url(r'^profile/$', views.profile, name= 'profile'),
    url(r'^upload/$',views.model_form_upload, name= 'upload'),
    url(r'^products/$',views.products, name= 'products'),
    url(r'^logout/$',views.logout, name= 'logout'),
    #url(r'^file_upload/$',views.file_upload,name='file_upload'),

]
