from django.urls import path, include
from course import views


urlpatterns = [
    path('',views.frontpage,name="frontpage"),
    path('about/', views.about, name='about'),
    path('course/', views.course, name='course'),
    path('support/', views.support, name='support'),
    path('course/courseView', views.courseView, name='courseView'),
]