#!/bin/bash
# -----------------------------------------------------------------------------Ï
# Filename:    upload.sh
# Revision:    0.0.1
# Date:        2018/03/29 - 17:54
# Author:      Haixiang HOU
# Email:       hexid26@outlook.com
# Website:     [NULL]
# Description: [...]
# Notes:       [NULL]
# -----------------------------------------------------------------------------
# Copyright:   2018 (c) Haixiang
# License:     GPL
# -----------------------------------------------------------------------------
# Version [1.0]
# 把本程序上传到服务器

SCRIPT_NAME=$(basename ${0})      # 脚本名称
BASEPATH=$(cd `dirname $0`; pwd)  # 脚本所在目录

file_list='crawler.py clear.sh gen_jpg.py merge_json.py'
# vpslist='139.180.130.111'
vpslist='96.30.193.243 139.180.130.111 167.179.72.4'

for vps in $vpslist; do
  tput setaf 1
  echo Processing $vps
  tput sgr0
  for file in $file_list; do
    tput setaf 4
    echo scp ${BASEPATH}/$file root@$vps:/root/2019nCoV/
    tput sgr0
    eval 'scp ${BASEPATH}/$file root@$vps:/root/2019nCoV/'
  done
done

exit
