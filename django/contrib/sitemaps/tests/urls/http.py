from datetime import date, datetime
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps import Sitemap, GenericSitemap, FlatPageSitemap, views
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page

from django.contrib.sitemaps.tests.base import I18nTestModel, TestModel


class SimpleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    location = '/location/'
    lastmod = datetime.now()

    def items(self):
        return [object()]


class SimpleI18nSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    i18n = True

    def items(self):
        return I18nTestModel.objects.all()


class EmptySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    location = '/location/'

    def items(self):
        return []


class FixedLastmodSitemap(SimpleSitemap):
    lastmod = datetime(2013, 3, 13, 10, 0, 0)


class FixedLastmodMixedSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    location = '/location/'
    loop = 0

    def items(self):
        o1 = TestModel()
        o1.lastmod = datetime(2013, 3, 13, 10, 0, 0)
        o2 = TestModel()
        return [o1, o2]


class DateSiteMap(SimpleSitemap):
    lastmod = date(2013, 3, 13)


class TimezoneSiteMap(SimpleSitemap):
    lastmod = datetime(2013, 3, 13, 10, 0, 0, tzinfo=timezone.get_fixed_timezone(-300))


def testmodelview(request, id):
    return HttpResponse()


simple_sitemaps = {
    'simple': SimpleSitemap,
}

simple_i18nsitemaps = {
    'simple': SimpleI18nSitemap,
}

empty_sitemaps = {
    'empty': EmptySitemap,
}

fixed_lastmod_sitemaps = {
    'fixed-lastmod': FixedLastmodSitemap,
}

fixed_lastmod__mixed_sitemaps = {
    'fixed-lastmod-mixed': FixedLastmodMixedSitemap,
}

generic_sitemaps = {
    'generic': GenericSitemap({'queryset': TestModel.objects.all()}),
}

flatpage_sitemaps = {
    'flatpages': FlatPageSitemap,
}


urlpatterns = [
    url(r'^simple/index\.xml$', views.index, {'sitemaps': simple_sitemaps}),
    url(r'^simple/custom-index\.xml$', views.index,
        {'sitemaps': simple_sitemaps, 'template_name': 'custom_sitemap_index.xml'}),
    url(r'^simple/sitemap-(?P<section>.+)\.xml$', views.sitemap,
        {'sitemaps': simple_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^simple/sitemap\.xml$', views.sitemap,
        {'sitemaps': simple_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^simple/i18n\.xml$', views.sitemap,
        {'sitemaps': simple_i18nsitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^simple/custom-sitemap\.xml$', views.sitemap,
        {'sitemaps': simple_sitemaps, 'template_name': 'custom_sitemap.xml'},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^empty/sitemap\.xml$', views.sitemap,
        {'sitemaps': empty_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^lastmod/sitemap\.xml$', views.sitemap,
        {'sitemaps': fixed_lastmod_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^lastmod-mixed/sitemap\.xml$', views.sitemap,
        {'sitemaps': fixed_lastmod__mixed_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^lastmod/date-sitemap.xml$', views.sitemap,
        {'sitemaps': {'date-sitemap': DateSiteMap}},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^lastmod/tz-sitemap.xml$', views.sitemap,
        {'sitemaps': {'tz-sitemap': TimezoneSiteMap}},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^generic/sitemap\.xml$', views.sitemap,
        {'sitemaps': generic_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^flatpages/sitemap\.xml$', views.sitemap,
        {'sitemaps': flatpage_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^cached/index\.xml$', cache_page(1)(views.index),
        {'sitemaps': simple_sitemaps, 'sitemap_url_name': 'cached_sitemap'}),
    url(r'^cached/sitemap-(?P<section>.+)\.xml', cache_page(1)(views.sitemap),
        {'sitemaps': simple_sitemaps}, name='cached_sitemap')
]

urlpatterns += i18n_patterns(
    url(r'^i18n/testmodel/(?P<id>\d+)/$', testmodelview, name='i18n_testmodel'),
)
