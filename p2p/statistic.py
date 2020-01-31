#!/usr/bin/env python
# coding:utf-8
"""read_json"""

import argparse
import logging
import json
import requests
import re
import xlrd
import xlwt

# def set_argparse():
#   """Set the args&argv for command line mode"""
#   parser = argparse.ArgumentParser()
#   parser.add_argument("file", type=str, default="", help="input data file")
#   return parser.parse_args()

nosugar_url = "https://2019ncov.nosugartech.com/data.json"
hbgj_gtgj_url = "https://jp.rsscc.com/gateway/dynamic/tool?client=vuetrainweb&source=vuetrainweb&platform=web&cver=7.0&dver=0&iver=5.32&format=json&uid=H5GTkvdmTxjKAfz7pRuxtjWc_C&imei=H5GTkvdmTxjKAfz7pRuxtjWc_C&uuid=H5GTkvdmTxjKAfz7pRuxtjWc_C&p=vuetrainweb%2Cunknown%2Cvuetrainweb%2C7.0%2Cweb&appinfo=vuetrainweb%2Cunknown%2Cvuetrainweb%2C7.0%2Cweb&systemtime=1580414561468&pid=315015&sid=3DF937FB"
sogou_url = "https://hhyfeed.sogoucdn.com/js/common/epidemic-search/main_2020013104.js"

global_item_list = []
global_table_head = [
    "id", "t_date", "t_start", "t_end", "t_type", "t_no", "t_memo", "t_no_sub", "t_pos_start",
    "t_pos_end", "source", "who", "verified", "t_created"
]
global_place_type = ["飞机", "火车", "地铁", "客车大巴", "公交车", "出租车", "轮船", "其它公共场所"]


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


def sort_json(key_name, json_object):
  json_object.sort(key=lambda k: (k.get(key_name, 0)))


def get_nosugar_data(url):
  """get_nosugar_data get source of url
  
  Arguments:
      url {str} -- url address
  """
  global global_place_type
  request_res = requests.get(url)
  request_res.encoding = "utf-8"
  temp_json = json.loads(request_res.text)
  temp_json = temp_json["data"]
  sort_json("t_date", temp_json)
  for item in temp_json:
    item["t_type"] = global_place_type[int(item["t_type"]) - 1]
    item["verified"] = "1"
    item["id"] = "无糖"
    item["t_created"] = item.pop("created_at")[0:10]
    item.pop("updated_at")
  return temp_json


def get_hbgj_gtgj_data(url):
  """get_nosugar_data get source of url
  
  Arguments:
      url {str} -- url address
  """
  global global_place_type
  request_res = requests.get(url)
  request_res.encoding = "utf-8"
  temp_json = json.loads(request_res.text)
  temp_json = temp_json["res"]["bd"]["data"]["list"]
  t_type_dict = {
      "subway": "地铁",
      "flight": "飞机",
      "coach": "客车大巴",
      "ship": "轮船",
      "bus": "公交车",
      "other": "其它公共场所",
      "taxi": "出租车",
      "train": "火车"
  }
  for item in temp_json:
    item["id"] = item.pop("id")
    item["t_date"] = item.pop("tripDate")
    item["t_start"] = item.pop("tripDeptime")
    item["t_end"] = item.pop("tripArrtime")
    item["t_no"] = item.pop("tripNo")
    item["t_memo"] = item.pop("tripMemo")
    item["t_no_sub"] = item.pop("carriage") + item.pop("seatNo")
    item["t_pos_start"] = item.pop("tripDepname")
    item["t_pos_end"] = item.pop("tripArrname")
    item["source"] = item.pop("link")
    item["who"] = item.pop("publisher")
    item["verified"] = str(item.pop("verified"))
    item.pop("tripDepcode")
    item.pop("tripArrcode")
    item.pop("nameIndex")
    item["t_created"] = item.pop("createtime")[0:10]
    item.pop("updatetime")
    item["t_type"] = t_type_dict[item.pop("tripType")]
    item["id"] = "航班管家"
  return temp_json


def get_sogou_data(url):
  """get_nosugar_data get source of url
  
  Arguments:
      url {str} -- url address
  """
  global global_place_type
  request_res = requests.get(url)
  request_res.encoding = "utf-8"
  temp_json = json.loads(request_res.text)
  t_type_dict = {"客车": "客车大巴", "公交": "公交车", "航班": "飞机", "火车": "火车", "汽车": "客车大巴", "大巴": "客车大巴"}
  for item in temp_json:
    item["id"] = ""
    item["t_date"] = item.pop("trafficTime")
    item["t_start"] = ""
    item["t_end"] = ""
    item["t_type"] = t_type_dict[item.pop("trafficType")]
    item["t_no"] = item.pop("trafficNum")
    item["t_no_sub"] = item.pop("detail") + item.pop("descr")
    item["t_pos_start"] = ""
    item["t_pos_end"] = ""
    item["source"] = item.pop("evidenceDocUrl")
    item["who"] = item.pop("evidenceDocId")
    item["verified"] = str(1)
    item["t_memo"] = item.pop("trainPath")
    item["id"] = "搜狗"
    item["t_created"] = item.pop("updateTime")[0:10]
  return temp_json


def get_temp_data(url):
  """get_nosugar_data get source of url
  
  Arguments:
      url {str} -- url address
  """
  global global_place_type
  request_res = requests.get(url)
  request_res.encoding = "utf-8"
  temp_json = json.loads(request_res.text)
  for item in temp_json:
    item["id"] = item.pop("")
    item["t_date"] = item.pop("")
    item["t_start"] = item.pop("")
    item["t_end"] = item.pop("")
    item["t_type"] = item.pop("")
    item["t_no"] = item.pop("")
    item["t_memo"] = item.pop("")
    item["t_no_sub"] = item.pop("")
    item["t_pos_start"] = item.pop("")
    item["t_pos_end"] = item.pop("")
    item["source"] = item.pop("")
    item["who"] = item.pop("")
    item["verified"] = item.pop("")
  __logger__.error("This function is a template")
  exit()


def read_xlsx_file(xlsx_file_name):
  json_from_xlsx = []
  global global_table_head
  date_regex = re.compile(r'(\d{4})/(\d+)/(\d+)')
  workbook = xlrd.open_workbook(xlsx_file_name)
  cur_sheet = workbook.sheet_by_name("1月30号")
  key_count = len(global_table_head)
  for row_idx in range(1, cur_sheet.nrows):
    if cur_sheet.cell_value(row_idx, key_count - 2) != "1":
      continue
    item = {}
    item["t_created"] = "2020-01-30"
    for col_idx in range(key_count):
      if col_idx == 0:
        item[global_table_head[col_idx]] = "CETC"
        continue
      elif col_idx == 1:
        date_items = date_regex.findall(cur_sheet.cell_value(row_idx, col_idx))
        if len(date_items) != 0:
          item[global_table_head[col_idx]] = "%d-%02d-%02d" % (
              int(date_items[0][0]),
              int(date_items[0][1]),
              int(date_items[0][2]),
          )
        else:
          item[global_table_head[col_idx]] = cur_sheet.cell_value(row_idx, col_idx)
        continue
      elif col_idx == 4:
        if cur_sheet.cell_value(row_idx, col_idx) == "客车" or cur_sheet.cell_value(row_idx,
                                                                                  col_idx) == "大巴":
          item[global_table_head[col_idx]] = "客车大巴"
        else:
          item[global_table_head[col_idx]] = cur_sheet.cell_value(row_idx, col_idx)
          continue
      else:
        item[global_table_head[col_idx]] = cur_sheet.cell_value(row_idx, col_idx)
    json_from_xlsx.append(item)
  return json_from_xlsx


def read_json_file(file_name):
  global global_item_list
  with open(file_name, 'r') as json_file:
    json_data = json.load(json_file)
    global_item_list = json_data["data"]
  global_item_list.sort(key=lambda x: (x.get('id', 0)))


def save_json_to_xlsx_file(file_path, json_object):
  global global_table_head
  nrows = len(json_object)
  ncols = len(global_table_head)
  workbook = xlwt.Workbook(encoding='utf-8')
  sheet = workbook.add_sheet("tx_data", cell_overwrite_ok=True)
  # sheet.write(0, 0, 'foobar')
  for idx in range(0, ncols):
    sheet.write(0, idx, global_table_head[idx])
  for row_idx in range(1, nrows + 1):
    for col_idx in range(0, ncols):
      sheet.write(row_idx, col_idx, json_object[row_idx - 1][global_table_head[col_idx]])
  workbook.save(file_path)
  return


def save_json(file_path):
  global global_item_list
  with open(file_path, "w") as json_file:
    json.dump(global_item_list, json_file, ensure_ascii=False)
  json_file.close()


def is_equal(object_1, object_2):
  score_1 = 0
  score_2 = 0
  if object_1["t_type"] == object_2["t_type"] and object_1["t_no"] == object_2["t_no"]:
    for key in object_1:
      if object_1[key] != "":
        score_1 = score_1 + 1
    for key in object_1:
      if object_1[key] != "":
        score_2 = score_2 + 1
    if score_1 >= score_2:
      return 2
    else:
      return 1
  else:
    return 0


def redundancy(list_object):
  cnt = 0
  while (cnt < len(list_object) - 1):
    idx = cnt + 1
    while (idx < len(list_object)):
      res = is_equal(list_object[cnt], list_object[idx])
      if res == 0:
        # * 不相同，不删除
        idx += 1
        continue
      elif res == 1:
        # * 删除前面的object
        list_object.pop(cnt)
        break
      else:
        # * 删除后面的object
        list_object.pop(idx)
        continue
    cnt += 1
  return list_object


def merge_jsons():
  global global_item_list
  # * 去冗余
  date_list = set(map(lambda x: x["t_date"], global_item_list))
  date_list = list(date_list)
  date_list.sort()
  group_list = []
  for date_item in date_list:
    group_list.append(list(filter(lambda x: x["t_date"] == date_item, global_item_list)))
  for item_list in group_list:
    item_list = redundancy(item_list)
  global_item_list = []
  for item_list in group_list:
    global_item_list += item_list
  sort_json("t_type", global_item_list)
  sort_json("t_date", global_item_list)
  cnt = 0
  for item_list in global_item_list:
    item_list["id"] = str(cnt)
    cnt += 1


def print_json(json_name, json_object):
  print("\n==================== %s START ====================\n" % json_name)
  for key_name in ["t_date", "t_type", "verified"]:
    print("Key_name = %s" % key_name)
    value_set = set(list(map(lambda x: x[key_name], json_object)))
    # value_set = list(value_set)
    # value_set.sort()
    print("Value has: %s" % value_set)
  print("\n===================== %s END =====================\n\n" % json_name)
  pass


def get_available_list(json_object):
  return list(map(lambda x: x["t_date"] + x["t_type"] + x["t_no"], json_object))


def statistical(table, json_object):
  global global_place_type
  sum = 0
  cnt = 1
  for key_name in [
      "无糖",
      "航班管家",
      "搜狗",
      "CETC",
  ]:
    temp_list = list(filter(lambda x: x["id"] == key_name, json_object))
    sum += len(temp_list)
    table[cnt].append(len(temp_list))
    cnt += 1
  table[cnt].append(sum)


def time_line(json_name, json_object):
  global global_place_type
  table = [[json_name]]
  for item in ["无糖","航班管家","搜狗"," CETC",]:
    table.append([item])
  table.append(["总数"])
  date_list = list(set(map(lambda x: x["t_date"], json_object)))
  date_list.sort()
  for date_item in date_list:
    table[0].append(date_item)
    temp_list = list(filter(lambda x: x["t_date"] == date_item, json_object))
    statistical(table, temp_list)
  print_table(json_name, table)


def print_table(name, table):
  print(name + "数据时间轴图")
  for line in table:
    line = map(lambda x: str(x), line)
    print("\t".join(line))
  print("\n")


def main():
  """Main function"""
  global nosugar_url
  global hbgj_gtgj_url
  global sogou_url
  global global_item_list
  global_item_list = []
  # read_json_file(ARGS.file)
  # * 无糖数据
  nosugar_json_data = get_nosugar_data(nosugar_url)
  global_item_list += nosugar_json_data
  __logger__.debug(len(global_item_list))

  # * 航班管家|高铁管家
  hbgj_gtgj_json_data = get_hbgj_gtgj_data(hbgj_gtgj_url)
  global_item_list += hbgj_gtgj_json_data
  __logger__.debug(len(global_item_list))

  # * 搜狗同乘
  sogou_json_data = get_sogou_data(sogou_url)
  global_item_list += sogou_json_data
  __logger__.debug(len(global_item_list))

  # * CETC 人工
  cetc_json_data = read_xlsx_file("tx_0130.xlsx")
  global_item_list += cetc_json_data
  __logger__.debug(len(global_item_list))

  # time_line("无糖", nosugar_json_data)
  # time_line("航班管家", hbgj_gtgj_json_data)
  # time_line("搜狗同乘", sogou_json_data)
  # time_line("CETC", cetc_json_data)
  time_line("总数据", global_item_list)

  merge_jsons()
  time_line("总数据（去重）", global_item_list)
  # print_json("all", global_item_list)
  # save_json("tx_data.json")
  # save_json_to_xlsx_file("tx_data.xls", global_item_list)
  __logger__.info("We got %d rules. Available check sum = %d" %
                  (len(global_item_list), len(set(get_available_list(global_item_list)))))
  # read_xlsx_file("")


if __name__ == '__main__':
  # ! Uncomment the next line to read args from cmd-line
  __logger__ = get_logger('read_json.py')
  # ARGS = set_argparse()
  main()
