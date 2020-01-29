#!/usr/bin/env python
# coding:utf-8
"""merge_json.py"""

import logging
import time
import os
import json, csv


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
  stream_hdlr = logging.StreamHandler()
  stream_hdlr.setFormatter(formater)
  logger.addHandler(stream_hdlr)
  logger.setLevel(logging.DEBUG)
  return logger


json_path = "json/"
__logger__ = get_logger('merge_json.py')
cur_date = time.strftime("%Y-%m-%d", time.localtime())
state_json_list = []
date_list = []
processed_json_data = 0  # ! 处理后的整体数据


def print_state_data(state_data):
  for province in state_data:
    print(province["name"])
    print(province["state"])
    print(province["cities"])


def read_json_files():
  global state_json_list
  global json_path
  global date_list
  json_file_list = sorted(os.listdir(json_path), reverse=True)
  date_list = list(map(lambda x: x[0:10], json_file_list))
  for file_name in json_file_list:
    json_data = ""
    with open(json_path + file_name, 'r') as json_file:
      json_data = json.load(json_file)
    state_json_list.append(json_data)
  # __logger__.debug(state_json_list)


def init_processed_json_data():
  global processed_json_data
  global state_json_list
  state_json = state_json_list[0]
  processed_json_data = state_json
  # __logger__.debug(processed_json_data)
  for province in processed_json_data:
    province["confirmedCount"] = [province["confirmedCount"]]
    province["suspectedCount"] = [province["suspectedCount"]]
    province["curedCount"] = [province["curedCount"]]
    province["deadCount"] = [province["deadCount"]]
    for city in province["cities"]:
      city["confirmedCount"] = [city["confirmedCount"]]
      city["suspectedCount"] = [city["suspectedCount"]]
      city["curedCount"] = [city["curedCount"]]
      city["deadCount"] = [city["deadCount"]]
  # __logger__.debug(json.dumps(processed_json_data[0], ensure_ascii=False))


def merge_cities(processed_json_cities, add_cities, day_index):
  missing_city_list = list(map(lambda x: x["cityName"], processed_json_cities))
  for city in add_cities:
    city_list = list(filter(lambda x: x["cityName"] in city["cityName"], processed_json_cities))
    if len(city_list) == 0:
      # ! 在现有数据之上新增 城市 数据
      city["confirmedCount"] = [city["confirmedCount"]] + [0] * day_index
      city["suspectedCount"] = [city["suspectedCount"]] + [0] * day_index
      city["curedCount"] = [city["curedCount"]] + [0] * day_index
      city["deadCount"] = [city["deadCount"]] + [0] * day_index
      processed_json_cities.append(city)
    else:
      # ! 刷新现有 城市 数据
      processed_json_data_cur_city = city_list[0]
      processed_json_data_cur_city["confirmedCount"].insert(0, city["confirmedCount"])
      processed_json_data_cur_city["suspectedCount"].insert(0, city["suspectedCount"])
      processed_json_data_cur_city["curedCount"].insert(0, city["curedCount"])
      processed_json_data_cur_city["deadCount"].insert(0, city["deadCount"])
      if processed_json_data_cur_city["cityName"] not in missing_city_list:
        # ! 锡林郭勒盟 会导致这里出问题
        pass
      else:
        missing_city_list.remove(processed_json_data_cur_city["cityName"])
  for city_name in missing_city_list:
    # ! 补全缺失的现有 城市 数据
    miss_city = list(filter(lambda x: x["cityName"] == city_name, processed_json_cities))[0]
    miss_city["confirmedCount"].insert(0, 0)
    miss_city["suspectedCount"].insert(0, 0)
    miss_city["curedCount"].insert(0, 0)
    miss_city["deadCount"].insert(0, 0)


def sort_json():
  global processed_json_data
  sort_flag_index = len(processed_json_data[0]["confirmedCount"]) - 1
  processed_json_data.sort(
      key=lambda k: (k.get("confirmedCount", 0)[sort_flag_index]), reverse=True)
  for province in processed_json_data:
    province["cities"].sort(
        key=lambda k: (k.get("confirmedCount", 0)[sort_flag_index]), reverse=True)


def merge_state_json_list():
  global processed_json_data
  global state_json_list
  init_processed_json_data()
  # days_sum = len(date_list)
  for state_json_index in range(1, len(date_list)):
    exsited_province_list = list(map(lambda x: x["provinceShortName"], processed_json_data))
    add_province_list = list(
        map(lambda x: x["provinceShortName"], state_json_list[state_json_index]))
    update_province_list = list(set(add_province_list) & set(exsited_province_list))
    new_province_list = list(set(add_province_list) - set(exsited_province_list))
    missing_province_list = list(set(exsited_province_list) - set(add_province_list))
    # __logger__.debug("更新 %s" % update_province_list)
    # __logger__.debug("新增 %s" % new_province_list)
    # __logger__.debug("缺失 %s" % missing_province_list)
    # ! 刷新现有 省市 数据
    for province_name in update_province_list:
      processed_json_data_cur_province = list(
          filter(lambda x: x["provinceShortName"] == province_name, processed_json_data))[0]
      province = list(
          filter(lambda x: x["provinceShortName"] == province_name,
                 state_json_list[state_json_index]))[0]
      processed_json_data_cur_province["confirmedCount"].insert(0, province["confirmedCount"])
      processed_json_data_cur_province["suspectedCount"].insert(0, province["suspectedCount"])
      processed_json_data_cur_province["curedCount"].insert(0, province["curedCount"])
      processed_json_data_cur_province["deadCount"].insert(0, province["deadCount"])
      merge_cities(processed_json_data_cur_province["cities"], province["cities"], state_json_index)
    # ! 在现有数据之上新增 省市 数据
    for province_name in new_province_list:
      new_province = list(
          filter(lambda x: x["provinceShortName"] == province_name,
                 state_json_list[state_json_index]))[0]
      new_province["confirmedCount"] = [new_province["confirmedCount"]] + [0] * state_json_index
      new_province["suspectedCount"] = [new_province["suspectedCount"]] + [0] * state_json_index
      new_province["curedCount"] = [new_province["curedCount"]] + [0] * state_json_index
      new_province["deadCount"] = [new_province["deadCount"]] + [0] * state_json_index
      for city in new_province["cities"]:
        city["confirmedCount"] = [city["confirmedCount"]] + [0] * state_json_index
        city["suspectedCount"] = [city["suspectedCount"]] + [0] * state_json_index
        city["curedCount"] = [city["curedCount"]] + [0] * state_json_index
        city["deadCount"] = [city["deadCount"]] + [0] * state_json_index
      processed_json_data.append(new_province)
    # ! 补全缺失的现有 省市 数据
    for province_name in missing_province_list:
      miss_province = list(
          filter(lambda x: x["provinceShortName"] == province_name, processed_json_data))[0]
      miss_province["confirmedCount"].insert(0, 0)
      miss_province["suspectedCount"].insert(0, 0)
      miss_province["curedCount"].insert(0, 0)
      miss_province["deadCount"].insert(0, 0)
      for city in miss_province["cities"]:
        city["confirmedCount"].insert(0, 0)
        city["suspectedCount"].insert(0, 0)
        city["curedCount"].insert(0, 0)
        city["deadCount"].insert(0, 0)
  sort_json()
  processed_json_data.insert(0, date_list)


def save_json(file_path):
  global processed_json_data
  with open(file_path, "w") as json_file:
    json.dump(processed_json_data, json_file, ensure_ascii=False)
  json_file.close()


def save_csv():
  global processed_json_data
  global date_list
  cnt_state = ["确诊", "疑似", "治愈", "死亡"]
  cnt_name = ["confirmedCount", "suspectedCount", "curedCount", "deadCount"]
  with open("history-areas.csv", "w") as csv_file:
    csv_write = csv.writer(csv_file)
    csv_head = ["省份", "区域", "状态"] + date_list
    csv_write.writerow(csv_head)
    for province in processed_json_data[1:]:
      province_name = province["provinceShortName"]
      for index in range(0, len(cnt_state)):
        row = [province_name, province_name, cnt_state[index]] + province[cnt_name[index]]
        csv_write.writerow(row)
      for city in province["cities"]:
        for index in range(0, len(cnt_state)):
          row = [province_name, city["cityName"], cnt_state[index]] + city[cnt_name[index]]
          csv_write.writerow(row)
  return


def read_csv_file(file_path):
  global processed_json_data
  with open(file_path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    all_china = {}
    rows = [row for row in reader]
    all_china["date"] = rows[0][2:]
    all_china["confirmedCount"] = [int(x) for x in rows[1][2:]]
    all_china["suspectedCount"] = [int(x) for x in rows[2][2:]]
    all_china["curedCount"] = [int(x) for x in rows[3][2:]]
    all_china["deadCount"] = [int(x) for x in rows[4][2:]]
    processed_json_data.insert(0, all_china)
  return


def main():
  """Main function"""
  file_path = "history-areas.json"
  read_json_files()
  merge_state_json_list()
  save_csv()
  read_csv_file("history.csv")
  save_json(file_path)


if __name__ == '__main__':
  # ! Uncomment the next line to read args from cmd-line
  main()
