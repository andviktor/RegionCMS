from django.urls import path
from . import views
from django.conf.urls import url

# main
urlpatterns = [
    path('', views.SiteListView.as_view(), name='sites'),
]

# build
urlpatterns += [
    path('site/<int:site_id>/build', views.build_site, name='site-build'),
]

# upload
urlpatterns += [
    path('site/<int:site_id>/upload', views.upload_site, name='site-upload'),
]

# site
urlpatterns += [
    path('site/<int:pk>', views.SiteDetailView.as_view(), name='site-detail'),
    path('site/create', views.SiteCreate.as_view(), name='site-create'),
    path('site/<int:pk>/edit', views.SiteUpdate.as_view(), name='site-edit'),
]

# region
urlpatterns += [
    path('site/<int:site_id>/regions', views.RegionListView.as_view(), name='region-list'),
    path('region/<int:pk>/edit', views.RegionUpdate.as_view(), name='region-edit'),
    path('site/<int:site_id>/addregion', views.RegionCreate.as_view(), name='region-create'),
    path('region/<int:pk>/delete', views.RegionDelete.as_view(), name='region-delete'),
]

# template
urlpatterns += [
    path('template/<int:pk>/edit', views.TemplateUpdate.as_view(), name='template-edit'),
    path('site/<int:site_id>/addtemplate', views.TemplateCreate.as_view(), name='template-create'),
    path('template/<int:pk>/delete', views.TemplateDelete.as_view(), name='template-delete'),
]

# chunk
urlpatterns += [
    path('chunk/<int:pk>/edit', views.ChunkUpdate.as_view(), name='chunk-edit'),
    path('site/<int:site_id>/addchunk', views.ChunkCreate.as_view(), name='chunk-create'),
    path('chunk/<int:pk>/delete', views.ChunkDelete.as_view(), name='chunk-delete'),
]

# placeholder
urlpatterns += [
    path('placeholder/<int:pk>/edit', views.PlaceholderUpdate.as_view(), name='placeholder-edit'),
    path('site/<int:page_id>/addplaceholder', views.PlaceholderCreate.as_view(), name='placeholder-create'),
    path('placeholder/<int:pk>/delete', views.PlaceholderDelete.as_view(), name='placeholder-delete'),
]

# page
urlpatterns += [
    path('page/<int:pk>/edit', views.PageUpdate.as_view(), name='page-edit'),
    path('site/<int:site_id>/addpage', views.PageCreate.as_view(), name='page-create'),
    path('page/<int:pk>/delete', views.PageDelete.as_view(), name='page-delete'),
]

# service
urlpatterns += [
    path('service/topvisor/<int:pk>/edit', views.TopvisorUpdate.as_view(), name='topvisor-edit'),
    path('site/<int:site_id>/createtopvisor', views.create_topvisor, name='create-topvisor'),
    path('service/topvisor/<int:topvisor_id>/export', views.export_topvisor, name='export-topvisor'),
    path('service/topvisor/<int:topvisor_id>/clear', views.clear_topvisor, name='clear-topvisor'),
]