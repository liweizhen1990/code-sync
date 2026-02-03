#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@author: liweizhen
#@email: liweizhen1990@gmail.com
"""
代码库同步脚本
"""
import json
import os
import subprocess
import sys

from flask import Flask, request, jsonify

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ConfigHelper import ConfigHelper

app = Flask(__name__)

# 需同步的分支名称列表
_BRANCH_NAME_ = ConfigHelper.getBranch()
# 代码库事件
_CODE_EVENT_ = ConfigHelper.getCodeEvent()
# 访问TOKEN
_ACCESS_TOKEN_ = ConfigHelper.getAccessToken()
# 加密TOKEN
_SECRET_TOKEN_ = ConfigHelper.getSecretToken()
# 需同步的代码库地址列表 Master
_REPO_SSH_URL_MASTER_ = ConfigHelper.getMasterRepoSshUrl()
# 需同步的代码库地址列表 Test
_REPO_SSH_URL_TEST_ = ConfigHelper.getTestRepoSshUrl()
# 需同步的代码库地址列表 Dev
_REPO_SSH_URL_DEV_ = ConfigHelper.getDevRepoSshUrl()

# # 微信WebHooks通知地址
# _WECHAT_WEBHOOKS_ = ConfigHelper.getWeChatWebHooks()

def getCommand(source_url: str, dist_url: str, branch_name: str, dir_name: str, suffix_name: str) -> str:
    command = "sh code_sync.sh {source_url} {dist_url} {branch_name} {dir_name} {suffix_name}".format(
        source_url=source_url,
        dist_url=dist_url,
        branch_name=branch_name,
        dir_name=dir_name,
        suffix_name=suffix_name)
    print(command)
    return command
def execCommand(command: str) -> None:
    """
    执行 脚本命令
    :param command:     需要执行的命令
    """
    stdout, stderr = subprocess.Popen(command,
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      encoding="utf-8").communicate()
    print("execCommand:\n %s\n stdout is:\n %s" % (command, stdout))
    print("==============================================================================================")
    print("execCommand:\n %s\n stderr is:\n %s" % (command, stderr))
def codeSync(git_ssh_url: str, trace_id: str, branch_name: str, pRepoList: list) -> None:
    """
    代码同步方法
    :param git_ssh_url:         代码库地址
    :param trace_id:            请求ID
    :param pRepoList:           repo 地址列表
    :param branch_name:           repo 地址列表
    :return:
    """
    print("git_ssh_url is %s" % git_ssh_url)
    print("trace_id is %s" % trace_id)
    for inx, val in enumerate(pRepoList):
        if git_ssh_url in val[0]:
            print("match url is %s" % git_ssh_url)
            # for inx_s, val_s in enumerate(val[0]):
            #     print(val[0])
            for inx_d, val_d in enumerate(val[1]):
                # 源地址
                source_url = git_ssh_url
                print("源地址: %s" % source_url)
                # 目标地址
                dist_url = val_d
                print("目标地址: %s" % dist_url)
                # 库名称
                repo_name = git_ssh_url.split('/')[-1].split('.')[0]
                print("库名称: %s" % repo_name)
                print("分支名称: %s" % branch_name)
                # 文件夹名称
                dir_name = trace_id + "_" + (inx.__str__() +
                                             repo_name.__str__() + inx_d.__str__())
                print("源地址: %s" % source_url)
                command = getCommand(source_url, dist_url, repo_name,
                                     dir_name, branch_name)
                execCommand(command)
        else:
            print("未匹配到对应GIT地址")
@app.route('/hooks', methods=['POST'])
def Hooks():
    try:
        print("开始处理请求: %s" % request)
        if request.method == 'GET':
            # 处理 GET 请求的逻辑
            return jsonify({"message": "Webhook endpoint is ready"})
        else:
            # 获取请求头
            pHeader = request.headers
            print(pHeader)
            pHToken = pHeader['X-Codeup-Token']
            pHTraceId = pHeader['Eagleeye-Traceid']

            # 获取请求数据
            pData = str(request.data, encoding='utf-8')
            # 获取token
            post_token = request.args['access_token']
            if _ACCESS_TOKEN_ == post_token and _SECRET_TOKEN_ == pHToken:
                print("请求校验通过")
            else:
                print("请求校验失败")
                return jsonify({"status": 403})
            # 打印请求头
            print("请求头为:\n %s" % pHeader)
            # 打印请求数据
            print("请求数据为:\n %s" % pData)
            # 获取请求头事件信息
            CodeupEvent = pHeader['X-Codeup-Event']
            print("事件信息为: %s" % CodeupEvent)

            if _CODE_EVENT_ == CodeupEvent:
                jsonData = json.loads(pData)
                print("事件为PUSH HOOK")
                repository = jsonData['repository']
                git_ssh_url = repository['git_ssh_url']
                print("代码库地址: %s" % git_ssh_url)
                branch_name = jsonData['ref'].split('/')[2]
                print("分支名称: %s" % branch_name)

                # 代码同步
                # 先判断是否为 master 分支; 只有 master 分支有变动的时候才会触发代码同步
                # if branch_name in _BRANCH_NAME_:
                if branch_name == "master":
                    codeSync(git_ssh_url, pHTraceId, branch_name, _REPO_SSH_URL_MASTER_)
                elif branch_name == "test":
                    codeSync(git_ssh_url, pHTraceId, branch_name, _REPO_SSH_URL_TEST_)
                elif branch_name == "dev":
                    codeSync(git_ssh_url, pHTraceId, branch_name, _REPO_SSH_URL_DEV_)
                else:
                    print("未匹配到对应分支代码推送事件，跳过")
                    return jsonify({"status": 200})
            else:
                print("非代码推送事件，跳过")
                return jsonify({"status": 200})
            return jsonify({"status": 200})
    except Exception as ex:
        print("报错了")
        print(ex)
        print(ex.__str__())
        return jsonify({"status": 500})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
