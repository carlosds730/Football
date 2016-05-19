"""Football URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib.auth.views import login, logout, logout_then_login, password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete, password_change, password_change_done
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from stats import views
from smarturls import surl

# use this part to include the views that not use arguments
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^login/$',
        login, name='login'),
    url(r'^logout/$',
        logout, name='logout'),
    url(r'^logout-then-login/$',
        logout_then_login, name='logout_then_login'),
    url(r'^password-reset/$',
        password_reset, name='password_reset'),
    url(r'^password-reset/done/$',
        password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        password_reset_complete, name='password_reset_complete'),
    url(r'^password-change/$',
        password_change, name='password_change'),
    url(r'^password-change/done/$',
        password_change_done, name='password_change_done'),
    url(r'^register/$', views.register, name='register'),
    url(r'edit/', views.edit, name='edit'),
    url(r'^$', views.home, name='home')
]

# use surl to set the views that receive arguments
urlpatterns += [
    surl('/season/<int:season_num>/', views.season, name='season'),
    surl('/general/<word:order>/', views.general, name='general'),
]

# This part is only to set serve the static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Surl

# Examples:
# urlpatterns = patterns('',
#     surl('/book/<int:bookid>/', 'some.view'),
#     surl('/author/<slug:author_name>/', 'some.other.view'),
#     surl('/year/<int4:year>/', 'year.view'),
#     surl('/year/<int4:year>/<word:month>/', 'month.view'),
# )

# Default patterns:
# int: \d+
# int2: \d{2,2}
# int4: \d{4,4}
# word: \w+
# slug: [\w-]+
# digit: \d{1,1}
# username: [\w.@+-]+
