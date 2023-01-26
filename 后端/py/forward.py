import requests
from urllib.parse import urlencode
import time
import random
from pyquery import PyQuery as pq
import sys

# 设置代理等（新浪微博的数据是用ajax异步下拉加载的，network->xhr）
host = 'weibo.com'
base_url = 'https://%s/ajax/statuses/repostTimeline?' % host
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'

# 设置请求头
headers = {
    'Host': host,
    'keep': 'close',
    # 'Referer': 'https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E5%A6%82%E4%BD%95%E7%9C%8B%E5%BE%85%E5%8F%8D%E5%86%85%E5%8D%B7%E7%83%AD%E6%BD%AE%23&extparam=%23%E5%A6%82%E4%BD%95%E7%9C%8B%E5%BE%85%E5%8F%8D%E5%86%85%E5%8D%B7%E7%83%AD%E6%BD%AE%23&luicode=10000011&lfid=100103type%3D38%26q%3D%E5%86%85%E5%8D%B7%26t%3D0',
    'User-Agent': user_agent
}
from datetime import datetime
def time_formater(input_time_str):
    input_format = '%a %b %d %H:%M:%S %z %Y'
    output_format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(input_time_str, input_format).strftime(output_format)
# 按页数抓取数据
def get_single_page(wid):
    params = {
        'id':wid, # 、、教育内卷、职场内卷、如何看待内卷的社会状态、如何避免婚姻内卷、
    }
    url = base_url + urlencode(params)
    print(url)   
    error_times = 3
    while True:
        response = requests.get(url, headers=headers)  # ,proxies=abstract_ip.get_proxy()
        if response.status_code == 200:
            if len(response.json().get('data')) > 0:
                return response.json()
        time.sleep(3)
        error_times += 1
        # 连续出错次数超过 3
        if error_times > 3:
            return None
count = 0
def parse_page(json_data):
    global count
    items = json_data.get('data')
    for index, item in enumerate(items):
        if item.get('reposts_count')>10:
            data = {
                'wid': item.get('mid'),
                'source': item.get('user').get('screen_name'),
                'target': item.get('retweeted_status').get('user').get('screen_name'),
                'value': item.get('reposts_count'),  # 转发数
                'publish_time': time_formater(item.get('created_at')),
                'counts':count,
            }
            
            count += 1
            print(f'total count: {count}')
            yield data

def parse_page_twice(json_data,user):
    global count
    try:
        items = json_data.get('data')
    except:
        return None
    for index, item in enumerate(items):
        if item.get('reposts_count')>1:
            data = {
                'wid': item.get('mid'),
                'source': item.get('user').get('screen_name'),
                'target': user,
                'value': item.get('reposts_count'),  # 转发数
                'publish_time': time_formater(item.get('created_at')),
                'counts':count,
            }
            count += 1
            print(f'total count: {count}')
            yield data
            
def parse_page_third(json_data,user):
    global count
    items = json_data.get('data')
    for index, item in enumerate(items):
        if item.get('reposts_count')>0:
            data = {
                'wid': item.get('mid'),
                'source': item.get('user').get('screen_name'),
                'target': user,
                'value': item.get('reposts_count'),  # 转发数
                'publish_time': time_formater(item.get('created_at')),
                'counts':count,
            }          
            count += 1
            print(f'total count: {count}')
            yield data
import os, csv

if __name__ == '__main__':
    wid = sys.argv[1]
    
    result_file = f'{wid}.csv'
    if not os.path.exists(result_file):
        with open(result_file, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["source","target","value","publish_time"])
    all_data = []
    temp_data = []
    temp_wid = []
    temp_wid_twice = []
    temp_user_twice = []
    temp_user = []
    empty_times = 0
    json_data = get_single_page(wid)
    if json_data == None:
        print('json is none')
    for result in parse_page(json_data):  # 需要存入的字段
        temp_data.append(result)
        temp_wid.append(result['wid'])
        temp_user.append(result['source'])
    all_data=temp_data
    with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        for d in temp_data:
            writer.writerow(
                [d['wid'], d['source'], d['target'], d['value'], d['publish_time']])
    print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n') 
    time.sleep(random.randint(1, 4))  # 爬取时间间隔
    for i in range(len(temp_wid)):
        temp_data = []
        
        json_data = get_single_page(temp_wid[i])
        if json_data == None:
            print('json is none')
        for result in parse_page_twice(json_data,temp_user[i]):
            temp_data.append(result)
            temp_wid_twice.append(result['wid'])
            temp_user_twice.append(result['source'])
        all_data=all_data+temp_data
        with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for d in temp_data:
                writer.writerow(
                    [d['wid'], d['source'], d['target'], d['value'], d['publish_time']])
        print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
        time.sleep(random.randint(1, 4))
    for i in range(len(temp_wid_twice)):
        temp_data = []
        json_data = get_single_page(temp_wid_twice[i])
        if json_data == None:
            print('json is none')
        for result in parse_page_third(json_data,temp_user_twice[i]):
            temp_data.append(result)
        all_data=all_data+temp_data
        with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for d in temp_data:
                writer.writerow(
                    [d['wid'], d['source'], d['target'], d['value'], d['publish_time']])
        print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
        time.sleep(random.randint(1, 4))
