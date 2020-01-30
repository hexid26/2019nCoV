#!/usr/bin/env python
# coding:utf-8
"""read_json"""

import argparse
import logging
import json
import csv


def set_argparse():
  """Set the args&argv for command line mode"""
  parser = argparse.ArgumentParser()
  parser.add_argument("file", type=str, default="", help="input data file")
  return parser.parse_args()


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


__logger__ = get_logger('read_json.py')
global_item_list = ""
global_place_type = ["飞机", "火车", "地铁", "客车大巴", "公交车", "出租车", "轮船", "其它公共场所"]


def read_json_file(file_name):
  global global_item_list
  with open(file_name, 'r') as json_file:
    json_data = json.load(json_file)
    global_item_list = json_data["data"]
  global_item_list.sort(key=lambda x: (x.get('id', 0)))
  # __logger__.debug(json.dumps(global_item_list, ensure_ascii=False))


def save_csv_file(file_path):
  with open(file_path, 'w', encoding='utf-8-sig') as f:
    csv_write = csv.writer(f)
    csv_head = [
        "id", "t_date", "t_start", "t_end", "t_type", "t_no", "t_memo", "t_no_sub", "t_pos_start",
        "t_pos_end", "source", "who", "verified"
    ]
    csv_write.writerow(csv_head)
    for item in global_item_list:
      row_data = []
      row_data.append(str(item["id"]))
      row_data.append(str(item["t_date"]))
      row_data.append(str(item["t_start"]))
      row_data.append(str(item["t_end"]))
      row_data.append(str(global_place_type[item["t_type"] - 1]))
      row_data.append(str(item["t_no"]))
      row_data.append(str(item["t_memo"]))
      row_data.append(str(item["t_no_sub"]))
      row_data.append(str(item["t_pos_start"]))
      row_data.append(str(item["t_pos_end"]))
      row_data.append(str(item["source"]))
      row_data.append(str(item["who"]))
      row_data.append(str(item["verified"]))
      csv_write.writerow(row_data)


def main():
  """Main function"""
  # __logger__.debug(ARGS.file)
  read_json_file(ARGS.file)
  save_csv_file("data.csv")


if __name__ == '__main__':
  # ! Uncomment the next line to read args from cmd-line
  ARGS = set_argparse()
  main()
