# -*-coding:utf-8-*-
# 解析QQ团的代码
# 

import re
import logging
from spider_base import *


class StateInitial(StateBase):
    def start_div(self, attrs):
        c=get_attr(attrs, 'class')
        if c == 'tuan_list_number':
            self.change_state(self.context.state_h3_title)

class StateH3Title(StateBase):
    def start_h3(self, attrs):
        self.change_state(self.context.state_url)

class StateUrl(StateBase):
    def start_a(self, attrs):
        show_href=get_attr(attrs,'href')
        url_prefix='http://tuan.qq.com'
        ch='/'
        if show_href[0] == '/':
            ch=''
        url = url_prefix + ch + show_href
        self.context.add_url(url)
        self.change_state(self.context.state_span_price)

class StateSpanPrice(StateBase):
    def start_span(self, attrs):
        c=get_attr(attrs, 'class')
        if c == 'num_price':
            self.change_state(self.context.state_price)

class StatePrice(StateBase):
    def handle_data(self, data):
        price=parse_first_float(data.strip())
        self.context.add_price(price)
        self.change_state(self.context.state_ul_value)

class StateUlValue(StateBase):
    def start_ul(self, attrs):
        c=get_attr(attrs, 'class')
        if c=='price_all':
            self.change_state(self.context.state_li_value)

class StateLiValue(StateBase):
    def enter(self):
        self.times=0
    def exit(self):
        self.times=0
    def start_li(self, attrs):
        self.times = self.times + 1
    def handle_data(self, data):
        if self.times == 2:
            self.change_state(self.context.state_value)
    # def start_del(self, attrs):
    #     self.change_state(self.context.state_value)

class StateValue(StateBase):
    def handle_data(self, data):
        value=parse_first_float(data.strip())
        self.context.add_value(value)
        self.change_state(self.context.state_span_bought)

class StateSpanBought(StateBase):
    def start_span(self, attrs):
        if get_attr(attrs, 'id') == 'sellCountter':
            self.change_state(self.context.state_bought)

class StateBought(StateBase):
    def handle_data(self, data):
        bought=parse_first_float(data.strip())
        self.context.add_bought(bought)
        self.change_state(self.context.state_lefttime)

class StateLefttime(StateBase):
    def enter(self):
        self.unit=''
        self.hour=0
        self.minute=0
        self.second=0

    def exit(self):
        self.unit=''
        self.hour=0
        self.minute=0
        self.second=0

    def start_span(self, attrs):
        self.unit=''
        c=get_attr(attrs,'class')
        if c == 'hour_num':
            self.unit='hour'
        elif c == 'minute_num':
            self.unit='minute'
        elif c == 'second_num':
            self.unit='second'
        else:
            self.unit=''
        
    def handle_data(self, data):
        unit = self.unit
        self.unit = ''
        value=int(parse_first_integer(data))
        if unit=='hour':
            self.hour=value
        elif unit=='minute':
            self.minute=value
        elif unit=='second':
            self.second=value
            lefttime=self.hour*60*60+self.minute*60+self.second
            self.context.add_time_end_by_timeleft(str(lefttime))
            self.change_state(self.context.state_div_image)
        else:
            self.context.logger.debug('skip,unit='+ unit +', value:'+data)

class StateDivImage(StateBase):
    def start_div(self, attrs):
        c=get_attr(attrs, 'class')
        if c in ['list_photo_details', 'first_photo_details']:
            self.change_state(self.context.state_image)

class StateImage(StateBase):
    def start_img(self, attrs):
        img=get_attr(attrs, 'init_src')
        title=get_attr(attrs, 'alt')
        self.context.add_image(img)
        self.context.add_title(title)
        self.change_state(self.context.state_initial)

class SpiderQQTuan(SpiderBase):
    logger = logging.getLogger('spider.SpiderQQTuan')
    def __init__(self):
        SpiderBase.__init__(self)
        self.state_initial=StateInitial(self)
        self.state_h3_title=StateH3Title(self)
        self.state_url=StateUrl(self)
        self.state_span_price=StateSpanPrice(self)
        self.state_price=StatePrice(self)
        self.state_ul_value=StateUlValue(self)
        self.state_li_value=StateLiValue(self)
        self.state_value=StateValue(self)
        self.state_span_bought=StateSpanBought(self)
        self.state_bought=StateBought(self)
        self.state_lefttime=StateLefttime(self)
        self.state_div_image=StateDivImage(self)
        self.state_image=StateImage(self)
        self.state=self.state_initial

def test_spider():
    import urllib
    urls = [
        'http://tuan.qq.com/shenzhen',
#        'http://tuan.qq.com/shanghai',
#        'http://tuan.qq.com/beijing',
#        'http://tuan.qq.com/chongqing',
#        'http://tuan.qq.com/guangzhou',
#        'http://tuan.qq.com/chengdu',
#        'http://tuan.qq.com/fuzhou',
        ]
    for url in urls:
        spider = SpiderQQTuan()
        if fetch_and_parse(spider, url):
            print spider
        else:
            print "fetch fail! url = " + url


def main():
    #logging.basicConfig(filename='', level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.ERROR)
    test_spider()

if __name__ == '__main__':
    main()

