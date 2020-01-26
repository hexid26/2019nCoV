#!/bin/bash
# -----------------------------------------------------------------------------
# Filename:    clear.sh
# Revision:    None
# Date:        2020/01/22 - 06:32
# Author:      Haixiang HOU
# Email:       hexid26@outlook.com
# Website:     [NULL]
# Notes:       [NULL]
# -----------------------------------------------------------------------------
# Copyright:   2018 (c) Haixiang
# License:     GPL
# -----------------------------------------------------------------------------
# Version [1.0]
# [Description]

SCRIPT_NAME=$(basename ${0})      # 脚本名称
BASEPATH=$(cd `dirname $0`; pwd)  # 脚本所在目录
tput setaf 2
echo "# ${SCRIPT_NAME} Running"
echo "========================================"
tput sgr0
# 1 红 2 绿 3 黄 4 蓝 5 粉 6 青 7 白 8 灰 9 橙 10 墨绿

rm history.*

tput setaf 2
echo "# ${SCRIPT_NAME} Done"
echo "========================================"
tput sgr0
