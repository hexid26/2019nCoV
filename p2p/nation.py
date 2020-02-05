#!/usr/bin/env python
# coding:utf-8
"""nation.py"""

import argparse
import logging
import json
import xlwt, xlrd

# def set_argparse():
#   """Set the args&argv for command line mode"""
#   parser = argparse.ArgumentParser()
#   parser.add_argument("file", type=str, default="", help="input data file")
#   return parser.parse_args()

# ! jbyfkzzx
china_json = []


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


def read_json_file(file_name):
  temp_json = []
  with open(file_name, 'r') as json_file:
    temp_json = json.load(json_file)
  return temp_json


def save_json(file_path, json_object):
  with open(file_path, "w") as json_file:
    json.dump(json_object, json_file, ensure_ascii=False)
  json_file.close()


def save_json_to_xlsx_file(file_path, json_object):
  workbook = xlwt.Workbook(encoding='utf-8')
  sheet = workbook.add_sheet("疾病预防控制中心", cell_overwrite_ok=True)
  # sheet.write(0, 0, 'foobar')
  row_idx = 0
  col_idx = 0
  for province in json_object:
    for city in province["cities"]:
      sheet.write(row_idx, col_idx, province["id"])
      col_idx += 1
      sheet.write(row_idx, col_idx, province["provinceName"])
      col_idx += 1
      sheet.write(row_idx, col_idx, city["id"])
      col_idx += 1
      sheet.write(row_idx, col_idx, city["name"])
      col_idx += 1
      for jbyfkzzx in city["jbyfkzzx"]:
        sheet.write(row_idx, col_idx, jbyfkzzx["name"])
        col_idx += 1
        sheet.write(row_idx, col_idx, jbyfkzzx["phone"])
        col_idx += 1
      row_idx += 1
      col_idx = 0
  workbook.save(file_path)
  return


def build_china_json():
  global china_json
  provinces_json = read_json_file("china_regions-3.3/json/province.json")
  cities_json = read_json_file("china_regions-3.3/json/city.json")
  city_object_json = read_json_file("china_regions-3.3/json/city_object.json")
  for province in provinces_json:
    province_item = {
        "id": province["id"],
        "provinceName": province["name"],
    }
    city_items = []
    for city_idx in cities_json[province["id"]]:
      city = {}
      city["id"] = city_object_json[city_idx["id"]]["id"]
      if city_object_json[city_idx["id"]]["name"] == "县" or city_object_json[
          city_idx["id"]]["name"] == "省直辖县级行政区划":
        continue
      elif city_object_json[city_idx["id"]]["name"] == "市辖区":
        city["name"] = city_object_json[city_idx["id"]]["province"]
      else:
        city["name"] = city_object_json[city_idx["id"]]["name"]
      city["jbyfkzzx"] = []
      city_items.append(city)
    province_item["cities"] = city_items
    china_json.append(province_item)


def read_txt_file():
  temp_data = []
  with open("cs_ocr_2020-01-30_00-33-47.txt", 'r') as txt_file:
    lines = txt_file.readlines()
    for line in lines:
      temp_data.append(line.split(" "))
  return temp_data


def insert_info(txt_list):
  cnt = 0
  global china_json
  for txt_item in txt_list:
    found_flag = False
    for province in china_json:
      for city in province["cities"]:
        if city["name"] in txt_item[0]:
          city["jbyfkzzx"].append({
              "name": txt_item[0],
              "phone": txt_item[1][0, len(txt_item[1]) - 1]
          })
          found_flag = True
          cnt += 1
          break
      if found_flag:
        break
  return cnt


# ! 疾病预防控制中心
def read_xls_file_jbyfkzzx(xlsx_file_name):
  json_from_xlsx = []
  workbook = xlrd.open_workbook(xlsx_file_name)
  cur_sheet = workbook.sheet_by_name("疾病预防控制中心")
  __logger__.debug(cur_sheet.nrows)
  __logger__.debug(cur_sheet.ncols)
  province_item = {
      "id": cur_sheet.cell_value(0, 0),
      "provinceName": cur_sheet.cell_value(0, 1),
      "cities": []
  }
  for row_idx in range(cur_sheet.nrows):
    if province_item["provinceName"] != cur_sheet.cell_value(row_idx, 1):
      json_from_xlsx.append(province_item)
      province_item = {
          "id": cur_sheet.cell_value(row_idx, 0),
          "provinceName": cur_sheet.cell_value(row_idx, 1),
          "cities": []
      }
    province_item["cities"].append({
        "id": cur_sheet.cell_value(row_idx, 2),
        "name": cur_sheet.cell_value(row_idx, 3),
        "jbyfkzzx": []
    })
    for col_idx in range(4, cur_sheet.ncols, 2):
      if cur_sheet.cell_value(row_idx, col_idx) != "":
        province_item["cities"][len(province_item["cities"]) - 1]["jbyfkzzx"].append({
            "name": cur_sheet.cell_value(row_idx, col_idx),
            "phone": cur_sheet.cell_value(row_idx, col_idx + 1),
        })
  json_from_xlsx.append(province_item)
  return json_from_xlsx


def main():
  """Main function"""
  # __logger__.info('Process start!')
  global china_json
  # build_china_json()
  # china_json = read_json_file("nation.json")
  # txt_list = read_txt_file()
  # res = insert_info(txt_list)
  read_json = read_xls_file_jbyfkzzx("同行交通工具.xlsx")
  # __logger__.debug(json.dumps(read_json, ensure_ascii=False))
  save_json_to_xlsx_file("history/jbyfkzzx.xls", read_json)
  save_json("history/jbyfkzzx.json", read_json)


# __logger__.info('Process end!')

if __name__ == '__main__':
  # ! Uncomment the next line to read args from cmd-line
  __logger__ = get_logger('nation.py')
  # ARGS = set_argparse()
  main()
