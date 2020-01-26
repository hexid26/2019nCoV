#!/usr/bin/env python
# coding:utf-8
"""gen_jpg.py"""

import logging
import csv
import numpy as np
import matplotlib.pyplot as plt
from pypinyin import pinyin, lazy_pinyin, Style

rows = []


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


__logger__ = get_logger('gen_jpg.py')


def create_png(index):
  x_array = rows[0][2:]
  # __logger__.debug(x_array)
  y_array_1 = list(map(int, rows[index + 0][2:]))
  y_array_2 = list(map(int, rows[index + 1][2:]))
  y_array_3 = list(map(int, rows[index + 2][2:]))
  y_array_4 = list(map(int, rows[index + 3][2:]))
  # __logger__.debug(y_array_1)
  fig, ax = plt.subplots()
  ax.plot(x_array, y_array_1, color='red', marker='^', linestyle='-', label="Comfirmed")
  if index == 1:
    # ! 暂时没有各地方的疑似数据（全国加入疑似数据）
    ax.plot(x_array, y_array_2, color='orange', marker='v', linestyle='--', label="Suspected")
  ax.plot(x_array, y_array_3, color='green', marker='o', linestyle='-.', label="Cured")
  ax.plot(x_array, y_array_4, color='black', marker='s', linestyle=':', label="Dead")
  ax.legend(loc='lower left', shadow=False)
  ax.set_title(''.join(lazy_pinyin(rows[index][0])))
  fig.savefig("/var/www/html/2019nCoV/" + str(rows[index][0]) + ".png", format='png')
  fig.clear()
  plt.close()


def read_csv(file_path):
  global rows
  with open(file_path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    rows = [row for row in reader]
    # __logger__.debug(rows[0])
    for index in range(0, int((len(rows) - 1) / 4)):
      # for index in range(0, 2):
      create_png(1 + 4 * index)


def main():
  """Main function"""
  # __logger__.info('Process start!')
  read_csv("/root/2019nCoV/history.csv")
  # __logger__.info('Process end!')


if __name__ == '__main__':
  # ! Uncomment the next line to read args from cmd-line
  main()
