#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@author: liweizhen
#@email: liweizhen1990@gmail.com
"""
配置文件帮助类 读取yaml格式的配置文件
"""
import os
import yaml
# 获取当前文件夹路径
curPath = os.path.dirname(os.path.realpath(__file__))
# 获取yaml配置文件路径
confPath = os.path.join(curPath, "ConfigHelper.yaml")
# open方法打开文件直接读出来
confFile = open(confPath, 'r', encoding='utf-8')
confInfo = confFile.read()
confDict = yaml.safe_load(confInfo.encode('utf-8'))
# 无用===================================================================================
# 用safe_load方法转字典
# 加入 json.dumps 防止双引号转为单引号
# 这种方式会降双引号转为单引号
# confDict = yaml.safe_load(confInfo.encode('utf-8'))
# confDict = json.loads(json.dumps(yaml.safe_load(confInfo.encode('utf-8'))))
# confDict = json.dumps(yaml.safe_load(confInfo.encode('utf-8')))
# confDict = json.loads(confDict.replace('\'', '\"'))
# 无用===================================================================================

class ConfigHelper:
    """
    帮助类
    @author: liweizhen
    @email: liweizhen1990@gmail.com
    """
    @staticmethod
    def getBranch():
        """
        获取 需同步的分支名称
        :return:
        """
        return confDict["_BRANCH_NAME_"]
    @staticmethod
    def getCodeEvent() -> str:
        """
        获取 代码事件
        :return:
        """
        return confDict["_CODE_EVENT_"].__str__()
    @staticmethod
    def getAccessToken() -> str:
        """
        获取访问 AccessToken
        :return:
        """
        return confDict["_ACCESS_TOKEN_"].__str__()

    @staticmethod
    def getSecretToken() -> str:
        """
        获取访问 SecretToken
        :return:
        """
        return confDict["_SECRET_TOKEN_"].__str__()
    @staticmethod
    def getMasterRepoSshUrl() -> list:
        """
        获取 GitSshUrl 信息
        :return:
        """
        return confDict["_REPO_SSH_URL_MASTER_"]
    @staticmethod
    def getTestRepoSshUrl() -> list:
        """
        获取 GitSshUrl 信息
        :return:
        """
        return confDict["_REPO_SSH_URL_TEST_"]
    @staticmethod
    def getDevRepoSshUrl() -> list:
        """
        获取 GitSshUrl 信息
        :return:
        """
        return confDict["_REPO_SSH_URL_DEV_"]