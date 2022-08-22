from django.urls import path

from . import doc_views

urlpatterns = [
    path('', doc_views.index, name='index'),
    path('add_document', doc_views.add, name='add_document'),
    path('doc_upload', doc_views.doc_upload, name='doc_upload'),
    path('download', doc_views.download, name='download'),
    path('doc_delete', doc_views.doc_delete, name='doc_delete'),

]