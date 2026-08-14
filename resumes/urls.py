from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('<uuid:resume_id>/build/', views.resume_builder, name='resume_builder'),
    path('<uuid:resume_id>/delete/', views.resume_delete, name='resume_delete'),
    path('<uuid:resume_id>/download/', views.resume_download, name='resume_download'),
    path('<uuid:resume_id>/<str:section>/add/', views.add_resume_item, name='add_resume_item'),
    path('<uuid:resume_id>/<str:section>/<int:item_id>/update/', views.update_resume_item, name='update_resume_item'),
    path('<uuid:resume_id>/<str:section>/<int:item_id>/delete/', views.delete_resume_item, name='delete_resume_item'),
]
