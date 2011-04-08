# -*-coding:utf-8-*-

import datetime
from django.shortcuts import render_to_response

import models
from ip469.ip import ip_convert
from ip469.ip import models as ip_models

import logging
import settings
logging.basicConfig(filename=settings.LOG_ROOT + 'tuan-views.log',
                    level=logging.DEBUG)


DEFAULT_COUNT_PER_PAGE = 30
PAGE_BAD = 0
PAGE_1ST = 1
DEFAULT_PAGE = PAGE_1ST
CATEGORY_ALL = 0
DEFAULT_CATEGORY = CATEGORY_ALL
MAX_TITLE_LEN = 775

def get_client_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']

def tuan_city_category_page(request, city, category, page):
    """
    """
    try:
        category = int(category)
    except ValueError:
        category = DEFAULT_CATEGORY
        
    try:
        page = int(page)
    except ValueError:
        page = DEFAULT_CATEGORY
    if page < PAGE_1ST: page = PAGE_1ST
    count = DEFAULT_COUNT_PER_PAGE
    deals = None
    if category == 0:
        deals = models.Deal.objects.filter(city=city)
    else:
        deals = models.Deal.objects.filter(city=city, category=category)
    deals = deals.filter(time_end__gte=datetime.datetime.now()).order_by('-rank')
    total = deals.count()
    if total != 0:
        deals = deals[ (page - 1) * count : (page - 1) * count + count]
    max_page = (total / count) + ( (total % count > 0) and 1 or 0 )
    next_page = (page < max_page) and page + 1 or PAGE_BAD
    prev_page = (page > PAGE_1ST) and (page - 1) or PAGE_BAD
    for deal in deals:
        if len(deal.title) <= MAX_TITLE_LEN:
            deal.title_short = deal.title
        else:
            deal.title_short = deal.title[:MAX_TITLE_LEN] + '……'
        site = models.Site.objects.filter(site=deal.site)
        if site.count() == 1:
            deal.site_name = site[0].name
            site_city = models.SiteCity.objects.filter(site=deal.site,city=deal.city)
            if site_city.count() == 1:
                deal.site_url = site_city[0].url
            else:
                deal.site_url = site[0].url
        else:
            deal.site_name = ''
    # 获取城市名称
    city_name = city
    city_query = models.City.objects.filter(city=city)
    if city_query.count() == 1:
        city_name = city_query[0].name
    # 获取团购网站列表
    site = models.Site.objects.all()
    # 获取城市列表
    city_list = models.City.objects.all()
    return render_to_response('tuan.html', locals())

def tuan_city_category(request, city, category):
    return tuan_city_category_page(request, city, category, DEFAULT_PAGE)

def tuan_city_page(request, city, page):
    return tuan_city_category_page(request, city, DEFAULT_CATEGORY, page)

def tuan_city(request, city):
    return tuan_city_page(request, city, DEFAULT_PAGE)

def tuan_page(request, page):
    logger = logging.getLogger('tuan_page')
    ip_string = get_client_ip(request)
    ip = ip_convert.ipv4_from_string(ip_string)
    city_name = ip_models.Ipv4Info.objects.get_city_by_ip(ip)
    logger.debug('city_name is ' + city_name)
    city = 'beijing'           # default value
    if city_name != '':
        city_name_uni=city_name.decode('utf8')
        if len(city_name_uni) >= 2:
            city_name_2prefix = city_name_uni[0:2].encode('utf8')
            query = models.City.objects.filter(
                name__istartswith = city_name_2prefix)
            if query.count() > 0:
                city = query[0].city
                logger.debug('found city ' + city + ' by ip ' + ip_string)
    logger.debug('city is ' + city)
    return tuan_city_page(request, city, page)

def tuan(request):
   return tuan_page(request, DEFAULT_PAGE)


