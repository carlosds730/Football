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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from stats import views
from smarturls import surl

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^$', views.home, name='home')
]

urlpatterns += [
    surl('/season/<int:season_num>/', views.season, name='season'),
    surl('/general/<word:order>/', views.general, name='general'),
]

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
