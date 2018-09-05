from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from .views import (post_add, post_update, post_list, post_delete, home,
                    category_list, category_add, category_update,
                    category_delete,tag_list, tag_add, tag_update,
                    tag_delete, register, login, activate_account,
                    account_info)

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^post/add/$', post_add, name='post_add'),
    url(r'^post/delete/(?P<pk>[\d]+)/$',post_delete, name='post_delete'),
    url(r'^post/update/(?P<pk>[\d]+)/$', post_update, name='post_update'),
    url(r'^category/$', category_list, name='category_list'),
    url(r'^category/add/$', category_add, name='category_add'),
    url(r'^category/update/(?P<pk>[\d]+)/$', category_update,
        name='category_update'),
    url(r'^category/delete/(?P<pk>[\d]+)/$', category_delete,
        name='category_delete'),
    url(r'^tag/$', tag_list, name='tag_list'),
    url(r'^tag/add/$', tag_add, name='tag_add'),
    url(r'^tag/update/(?P<pk>[\d]+)/$', tag_update, name='tag_update'),
    url(r'^tag/delete/(?P<pk>[\d]+)/$', tag_delete, name='tag_delete'),
    url(r'^accounts/login/$', login,
        {'template_name': 'cadmin/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,
        {'template_name': 'cadmin/logout.html'}, name='logout'),
    url(r'^account-info/$', account_info, name='account_info'),
    url(r'^password-change/$', auth_views.password_change,
        {'template_name': 'cadmin/password_change.html',
        'post_change_redirect': 'cadmin:password_change_done'},
        name='password_change'),
    url(r'^password-change-done/$', auth_views.password_change_done,
        {'template_name': 'cadmin/password_change_done.html'},
        name='password_change_done'
    ),
    url(r'^activate/account/$', activate_account, name='activate'),
    url(r'^register/$', register, name='register'),
]
