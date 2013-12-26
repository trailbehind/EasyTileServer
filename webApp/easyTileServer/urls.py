from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib.auth.decorators import login_required

from layers import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'layeradmin', views.LayerAdmin)


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.IndexView.as_view()),

    url(r'^', include(router.urls)),

    url(r'^layers/$', views.TileJson.as_view({'get': 'list'})),
    url(r'^layers.(?P<format>[^/\.]+)$', views.TileJson.as_view({'get': 'list'})),
    url(r'^layers/(?P<layerName>[^/\.]+).(?P<format>[\w]+)$', views.TileJson.as_view({'get': 'retrieve'})),
    url(r'^layers/(?P<layerName>[^/]+)/$', views.TileJson.as_view({'get': 'retrieve'})),

    url(r'^preview/(?P<layer_name>[^/\.]+)/$', views.LayerPreviewView.as_view()),
    url(r'^upload/', login_required(views.UploadFileView.as_view(success_url="/layeradmin/"))),

    url(r'^tiles/(?P<layer_name>[^/]+)/(?P<z>[^/]+)/(?P<x>[^/]+)/(?P<y>[^/]+)\.(?P<extension>.+)$', 'layers.views.tiles', name='tiles_url'),
)
