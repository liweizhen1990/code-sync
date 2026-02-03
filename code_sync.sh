#!/bin/sh
# @author: liweizhen
# @email: liweizhen1990@gmail.com
# Code Sync Shell Script
# 源路径地址
_SOURCE_SSH_URL_=$1
# 目标路径地址
_DIST_SSH_URL_=$2
# 库名称
_REPO_NAME_=$3
# 代码克隆路径
_CODE_DIR_=$4
# 分支名称
_BRANCH_NAME_=$5
echo '####################################################################'
echo '打印源路径地址'
echo $_SOURCE_SSH_URL_
echo '打印目标路径地址'
echo $_DIST_SSH_URL_
echo '打印分支名称'
echo $_REPO_NAME_
echo '打印克隆代码库文件夹名称'
echo $_CODE_DIR_
echo '打印同步分支名称后缀'
echo $_BRANCH_NAME_
echo '####################################################################'
echo '克隆代码'
git clone -b $_BRANCH_NAME_ $_SOURCE_SSH_URL_ $_CODE_DIR_
echo '进入克隆代码库'
cd $_CODE_DIR_
echo '更新代码到最新'
git pull
echo '切换分支'
git branch $_REPO_NAME_-$_BRANCH_NAME_
git checkout $_REPO_NAME_-$_BRANCH_NAME_
echo '打印克隆分支名称'
echo $_REPO_NAME_-$_BRANCH_NAME_
echo '推送代码到远端'
git push $_DIST_SSH_URL_ $_REPO_NAME_-$_BRANCH_NAME_:$_REPO_NAME_-$_BRANCH_NAME_
echo '删除代码库文件夹'
cd ..
rm -rf $_CODE_DIR_
echo '代码同步结束'
echo '####################################################################'