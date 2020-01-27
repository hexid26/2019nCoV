#!/bin/bash
# -----------------------------------------------------------------------------
# Filename:    download.sh
# Revision:    None
# Date:        2020/01/22 - 07:34
# Author:      Haixiang HOU
# Email:       hexid26@outlook.com
# Website:     [NULL]
# Notes:       [NULL]
# -----------------------------------------------------------------------------
# Copyright:   2018 (c) Haixiang
# License:     GPL
# -----------------------------------------------------------------------------
# Version [1.0]
# 下载 history.log

SCRIPT_NAME=$(basename ${0})      # 脚本名称
BASEPATH=$(cd `dirname $0`; pwd)  # 脚本所在目录
tput setaf 2
echo "# ${SCRIPT_NAME} Running"
echo "========================================"
tput sgr0
# 1 红 2 绿 3 黄 4 蓝 5 粉 6 青 7 白 8 灰 9 橙 10 墨绿

file='history.log'
vpslist='96.30.193.243 139.180.130.111 167.179.72.4'

scp root@96.30.193.243:/root/2019nCoV/history.csv ${BASEPATH}/csv/data_us.csv
scp root@167.179.72.4:/root/2019nCoV/history.csv ${BASEPATH}/csv/data_jp.csv
scp root@139.180.130.111:/root/2019nCoV/history.csv ${BASEPATH}/csv/data_sgp.csv
scp root@139.180.130.111:/root/2019nCoV/json/* ${BASEPATH}/json/
scp root@139.180.130.111:/root/2019nCoV/history-areas* ${BASEPATH}/

tput setaf 2
echo "# ${SCRIPT_NAME} Done"
echo "========================================"
md5sum ${BASEPATH}/csv/data_us.csv ${BASEPATH}/csv/data_jp.csv ${BASEPATH}/csv/data_sgp.csv

tput sgr0
