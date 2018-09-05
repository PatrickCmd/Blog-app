from django.conf.urls import url, include
from django.contrib.flatpages import views as flat_views
from django.contrib.sitemaps.views import sitemap

from .views import (post_list, post_detail, feedback,
                    post_by_category, post_by_tag, tracker_user,
                    stop_tracking, admin_page, login, logout)
from .sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap
}


urlpatterns = [
    url(r'^feedback/$', feedback, name='feedback'),
    url(r'^$', post_list, name='post_list'),
    url(r'^(?P<pk>\d+)/(?P<post_slug>[\w\d-]+)$', post_detail, name='post_detail'),
    url(r'^category/(?P<category_slug>[\w-]+)/$', post_by_category, name='post_by_category'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', post_by_tag, name='post_by_tag'),
    url(r'^stop-tracking/$', stop_tracking, name='stop_tracking'),
    url(r'^track_user/$', tracker_user, name='tracker_user'),
    url(r'^login/$', login, name='blog_login'),
    url(r'^logout/$', logout, name='blog_logout'),
    url(r'^admin_page/$', admin_page, name='admin_page'),
    
    url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^eula/$', flat_views.flatpage, {'url': '/eula/'}, name='eula'),
    # url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^sitemap\.xml/$', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),
]
