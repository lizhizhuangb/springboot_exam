# -*- coding: utf-8 -*-
# @Time    : 2024/10/17 11:13
# @Author  : 烂泥
# @FileName: demo01.py
# @Version : v1.0
# @Description:
"""
https://tieba.baidu.com/managerapply/data/frs?kw=%E5%AD%99%E7%AC%91%E5%B7%9D&fid=21841105&is_mgr=0&mgr_num=1&t=1iacgc81q&ie=utf-8
https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D
"""
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class spider():
    def get_t(self):
        current_time = datetime.utcnow()
        timestamp_ms = str(current_time.timestamp() * 1000)
        return str(timestamp_ms)

    def __init__(self, id, page_num):
        self.baseurl = 'https://tieba.baidu.com/p/'
        self.id = id
        self.page_num = page_num
        self.ajax = 1
        self.time = self.get_t()
        self.count = 1
        self.url = self.baseurl + self.id + '?pn=' + self.page_num + '&ajax=1' + f'&t={self.time}'
        self.file = open(f'./{id}.md', 'w', encoding='utf-8')

    def spider_get_max_num(self):
        resp = requests.get(self.url)
        if resp.status_code == 200:
            page = BeautifulSoup(resp.text, 'html.parser')
            self.max_number = page.find('input', {'class': 'jump_input_bright'}).get('max-page')
        else:
            print('状态码有误：' + str(resp.status_code))

    def loop_all_page(self):
        for self.page_num in range(int(self.max_number)):
            self.time = self.get_t()
            self.url = self.baseurl + self.id + '?pn=' + str(self.page_num) + '&ajax=1' + f'&t={self.time}'
            self.get_target_page()
        self.file.close()

    def get_target_page(self):
        resp = requests.get(self.url)
        page = BeautifulSoup(resp.text, 'html.parser')
        comments = page.find_all('div', {'class': 'l_post l_post_bright j_l_post clearfix'})
        for comment_info in comments:
            print(comment_info)
            print('-----------------------------------------------------------------------------------------')
            try:
                user = comment_info.find('a', {'class': 'p_author_name'}).text
            except:
                user = comment_info.find('a', {'class': 'p_author_name'}).text
            comment = comment_info.find('div', {'class': 'd_post_content j_d_post_content'}).decode_contents().strip()
            if '<img' in comment:
                img_list = re.findall('<img.*?src="(.*?)".*?/>', comment)
                for img in img_list:
                    # print(img)
                    img_pos_start = comment.index('<img')  # 获取 <img> 标签的位置
                    img_pos_end = comment.index('/>') + 2  # 获取 <img> 标签的位置
                    # 在 <img> 标签前插入 Markdown 格式的图片
                    comment = comment[:img_pos_start] + f'![Image]({img})' + comment[img_pos_end:]
            self.file.write('#### ' + user + f'{self.count}楼\n')
            self.file.write(comment + '\n')


if __name__ == '__main__':
    spider = spider('9220823757', '1')
    spider.spider_get_max_num()
    spider.loop_all_page()
