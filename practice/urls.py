from django.urls import path, include
from practice import views


urlpatterns = [
    path('practice/', views.practice, name='practice'),
    path('practice/tree/', views.tree, name='tree'),
    path('practice/tree/treeView', views.treeView, name='treeView'),
    path('practice/warrior/', views.warrior, name='warrior'),
    path('practice/warrior/warriorView', views.warriorView, name='warriorView'),
    path('practice/goddess/', views.goddess, name='goddess'),
    path('practice/goddess/goddessView', views.goddessView, name='goddessView'),

]