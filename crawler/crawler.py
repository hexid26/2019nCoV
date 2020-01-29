#!/usr/bin/env python
# coding:utf-8
"""crawler.py"""

import argparse
import os
import re
import logging
import datetime
import requests
import csv
import json
import time
from bs4 import BeautifulSoup

# def set_argparse():
#   """Set the args&argv for command line mode"""
#   parser = argparse.ArgumentParser()
#   parser.add_argument("file", type=str, default="", help="input data file")
#   return parser.parse_args()

url = "https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579581727&enterid=1579581727&from=timeline&isappinstalled=0"
cur_data = []
data_collection = []
cur_date = time.strftime("%Y-%m-%d", time.localtime())


def get_logger(logname):
  """Config the logger in the module
  Arguments:
      logname {str} -- logger name
  Returns:
      logging.Logger -- the logger object
  """
  logger = logging.getLogger(logname)
  formater = logging.Formatter(
      fmt='%(asctime)s - %(filename)s : %(levelname)-5s :: %(message)s',
      # filename='./log.log',
      # filemode='a',
      datefmt='%m/%d/%Y %H:%M:%S')
  stream_hanlde = logging.StreamHandler()
  stream_hanlde.setFormatter(formater)
  logger.addHandler(stream_hanlde)
  logger.setLevel(logging.DEBUG)
  return logger


__logger__ = get_logger('crawler.py')


def get_source(url):
  """get_source get source of url
  
  Arguments:
      url {str} -- url address
  
  Returns:
      str -- source of url
  """
  request_res = requests.get(url)
  request_res.encoding = "utf-8"
  return request_res.text


def gen_area_data(area_name, static_sentence):
  """gen_item_data genarate data of areas
  
  Arguments:
      area_name {str} -- name of the area
      static_sentence {str} -- text data of the area
  """
  global cur_data
  dic_item = {'确诊': 0, '疑似': 0, '治愈': 0, '死亡': 0}
  item_pattern = re.compile(r'确诊 ?(\d+) ?例', re.DOTALL | re.IGNORECASE)
  item_pattern_res = re.findall(item_pattern, static_sentence)
  if len(item_pattern_res) != 0:
    dic_item['确诊'] = int(item_pattern_res[0])
  item_pattern = re.compile(r'疑似 ?(\d+) ?例', re.DOTALL | re.IGNORECASE)
  item_pattern_res = re.findall(item_pattern, static_sentence)
  if len(item_pattern_res) != 0:
    dic_item['疑似'] = int(item_pattern_res[0])
  item_pattern = re.compile(r'治愈 ?(\d+) ?例', re.DOTALL | re.IGNORECASE)
  item_pattern_res = re.findall(item_pattern, static_sentence)
  if len(item_pattern_res) != 0:
    dic_item['治愈'] = int(item_pattern_res[0])
  item_pattern = re.compile(r'死亡 ?(\d+) ?例', re.DOTALL | re.IGNORECASE)
  item_pattern_res = re.findall(item_pattern, static_sentence)
  if len(item_pattern_res) != 0:
    dic_item['死亡'] = int(item_pattern_res[0])
  cur_data.append({'name': area_name, cur_date: dic_item})


def gen_cur_data(source):
  """gen_cur_data generate current data from DXY
  
  Arguments:
      source {str} -- DXY website source
  """
  global cur_data
  soup = BeautifulSoup(source, features="html.parser")
  # ! 2020-01-29 全国整体数据
  for script_item in soup.body.find_all('script'):
    if 'id' in script_item.attrs:
      if script_item.get('id') == "getStatisticsService":
        json_pattern = re.compile(r'getStatisticsService = (.*?)}catch',
                                  re.DOTALL | re.IGNORECASE | re.MULTILINE)
        res = re.findall(json_pattern, script_item.text)
        nation_json_data = json.loads(res[0])
        gen_area_data(
            '全国', "确诊 " + str(nation_json_data["confirmedCount"]) + " 例，" + "疑似 " +
            str(nation_json_data["suspectedCount"]) + " 例，" + "治愈" +
            str(nation_json_data["curedCount"]) + " 例，" + "死亡 " +
            str(nation_json_data["deadCount"]) + " 例，")
        break
  # ! 2020-01-24 全国整体数据
  # for p_item in soup.find_all('p'):
  #   if 'class' in p_item.attrs:
  #     if p_item.get('class')[0] == "confirmedNumber___3WrF5":
  #       gen_area_data('全国', p_item.get_text())
  # ! 2020-01-24 区域数据
  for script_item in soup.body.find_all('script'):
    if 'id' in script_item.attrs:
      if script_item.get('id') == "getAreaStat":
        json_pattern = re.compile(r'getAreaStat = (.*?)}catch',
                                  re.DOTALL | re.IGNORECASE | re.MULTILINE)
        res = re.findall(json_pattern, script_item.text)
        site_json_data = json.loads(res[0])
        json_file = open("/root/2019nCoV/json/" + cur_date + ".json", 'w', encoding='utf-8')
        json.dump(site_json_data, json_file, ensure_ascii=False)
        json_file.close()
        for province in site_json_data:
          gen_area_data(
              province['provinceShortName'], "确诊 " + str(province['confirmedCount']) + " 例，" +
              "疑似 " + str(province['suspectedCount']) + " 例，"
              "治愈 " + str(province['curedCount']) + " 例，"
              "死亡 " + str(province['deadCount']) + " 例，")
  # # ! 2020-01-23
  # # * 全国整体数据
  # for p_item in soup.find_all('p'):
  #   if 'class' in p_item.attrs:
  #     if p_item.get('class')[0] == "confirmedNumber___3WrF5":
  #       gen_item_data('全国', p_item.get_text())
  # # * 区域数据
  # soup = BeautifulSoup(source, features="lxml")
  # for div_item in soup.find_all('div'):
  #   if 'class' in div_item.attrs:
  #     if div_item.get('class')[0] == "descBox___3dfIo":
  #       for p_item in div_item.find_all('p'):
  #         # __logger__.debug(p_item.get_text())
  #         area_name_pattern = re.compile(r'^(.*?) ', re.DOTALL | re.IGNORECASE)
  #         area_name_res = re.findall(area_name_pattern, p_item.get_text())
  #         gen_item_data(area_name_res[0], p_item.get_text())
  # # ! 2020-01-22
  # # * 全国整体数据
  # country_pattern = re.compile(r'"countRemark":"(.*?)"', re.DOTALL | re.IGNORECASE | re.MULTILINE)
  # country_res = re.findall(country_pattern, source)
  # gen_item_data('全国', country_res[0])
  # # * 红色区域数据
  # red_pattern = re.compile(r'<span><i class="red___3VJ3X"></i>(.*?)</span>',
  #                          re.DOTALL | re.IGNORECASE)
  # red_res = re.findall(red_pattern, source)
  # for red_item in red_res:
  #   area_name_pattern = re.compile(r'^(.*?) ', re.DOTALL | re.IGNORECASE)
  #   area_name_res = re.findall(area_name_pattern, red_item)
  #   gen_item_data(area_name_res[0], red_item)
  # # * 橙色区域数据
  # red_pattern = re.compile(r'<span><i class="orange___1FP2_"></i>(.*?)</span>',
  #                          re.DOTALL | re.IGNORECASE)
  # red_res = re.findall(red_pattern, source)
  # for red_item in red_res:
  #   area_name_pattern = re.compile(r'^(.*?) ', re.DOTALL | re.IGNORECASE)
  #   area_name_res = re.findall(area_name_pattern, red_item)
  #   gen_item_data(area_name_res[0], red_item)
  # ! 排序
  cur_data.sort(key=lambda k: (k.get('name', 0)))
  cur_data.sort(key=lambda k: ((k.get(cur_date, 0)).get('疑似', 0)), reverse=True)
  cur_data.sort(key=lambda k: ((k.get(cur_date, 0)).get('确诊', 0)), reverse=True)


def read_csv_file(file_path):
  global data_collection
  with open(file_path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    rows = [row for row in reader]
    for area_index in range(0, int((len(rows) - 1) / 4)):
      area_item = {}
      for col_index in range(2, len(rows[0])):
        dict_item = {
            '确诊': int(rows[1 + 4 * area_index + 0][col_index]),
            '疑似': int(rows[1 + 4 * area_index + 1][col_index]),
            '治愈': int(rows[1 + 4 * area_index + 2][col_index]),
            '死亡': int(rows[1 + 4 * area_index + 3][col_index])
        }
        area_item['name'] = rows[1 + 4 * area_index][0]
        area_item[rows[0][col_index]] = dict_item
      data_collection.append(area_item)
  return


def save_csv(file_path, data):
  date_list = []
  for item in data[0].keys():
    if item != "name":
      date_list.append(item)
  with open(file_path, 'w') as f:
    csv_write = csv.writer(f)
    csv_head = ["区域", "状态"]
    for item in date_list:
      csv_head.append(item)
    # __logger__.debug(csv_head)
    csv_write.writerow(csv_head)
    for dict_item in data:
      data_row_1 = [dict_item['name'], '确诊']
      for date_index in date_list:
        data_row_1.append(dict_item[date_index]['确诊'])
      data_row_2 = [dict_item['name'], '疑似']
      for date_index in date_list:
        data_row_2.append(dict_item[date_index]['疑似'])
      data_row_3 = [dict_item['name'], '治愈']
      for date_index in date_list:
        data_row_3.append(dict_item[date_index]['治愈'])
      data_row_4 = [dict_item['name'], '死亡']
      for date_index in date_list:
        data_row_4.append(dict_item[date_index]['死亡'])
      csv_write.writerow(data_row_1)
      csv_write.writerow(data_row_2)
      csv_write.writerow(data_row_3)
      csv_write.writerow(data_row_4)


def update_data_collection():
  global cur_data
  global data_collection
  global cur_date
  # * 确定日期列表
  date_list = []
  for item in data_collection[0].keys():
    if item != "name":
      date_list.append(item)
  # * 开始更新
  for cur_area_item in cur_data:
    flag_new = True
    for area_item in data_collection:
      # * 是否为新增城市（已有城市）
      if cur_area_item['name'] == area_item['name']:
        flag_new = False
        area_item[cur_date] = cur_area_item[cur_date]
        break
    # * 是否为新增城市（新增城市）
    if flag_new == True:
      print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - 新增：" + cur_area_item['name'])
      new_area_item = {'name': cur_area_item['name']}
      for date_item in date_list:
        new_area_item[date_item] = {'确诊': 0, '疑似': 0, '治愈': 0, '死亡': 0}
      new_area_item[cur_date] = cur_area_item[cur_date]
      data_collection.append(new_area_item)
  for missing_area_item in data_collection:
    if cur_date not in missing_area_item.keys():
      missing_area_item[cur_date] = {'确诊': 0, '疑似': 0, '治愈': 0, '死亡': 0}
  data_collection.sort(key=lambda k: (k.get('name', 0)))
  data_collection.sort(key=lambda k: ((k.get(cur_date, 0)).get('疑似', 0)), reverse=True)
  data_collection.sort(key=lambda k: ((k.get(cur_date, 0)).get('确诊', 0)), reverse=True)
  return


def main():
  """Main function"""
  global url
  global cur_data
  global data_collection
  file_path = "history.csv"
  url_source = get_source(url)
  gen_cur_data(url_source)
  if os.path.exists(file_path):
    read_csv_file(file_path)
  else:
    save_csv(file_path, cur_data)
    exit()
  update_data_collection()
  # __logger__.debug(data_collection)
  save_csv(file_path, data_collection)


if __name__ == '__main__':
  # ! Uncomment the next line to read args from cmd-line
  # ARGS = set_argparse()
  main()
