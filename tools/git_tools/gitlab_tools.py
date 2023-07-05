# coding=utf-8
# -*- coding: UTF-8 -*-
# 操作Gitlab的一些工具（未使用Gitlab API）

import requests

GITLAB_URL = "https://git.magotown.com"
GITLAB_HOST = "git.magotown.com"
# 从浏览器抓取，并填入如下信息
COOKIE = 'hide_auto_devops_implicitly_enabled_banner_1=false; frequently_used_emojis=beer; preferred_language=zh_CN; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc3lYU3dpSkRKaEpERXdKR1J2ZVZwU2NqRm1jMHMzUkRVelNqQjBNMmxHWVdVaUxDSXhOamc0TlRRd01qRTJMak0xTnpnd09DSmQiLCJleHAiOiIyMDIzLTA3LTE5VDA2OjU2OjU2LjM1N1oiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdXNlcl90b2tlbiJ9fQ%3D%3D--8c3d43c5b6f1ec34d31a58429ef89fd2e1d0c892; known_sign_in=NzZZaHMxRXZNU2YzM1R2ODZybUpHZXljQm10d3N3a0RwVTNkenMyRTlTdDZRbVNFOHNPS29lRldTQUxDQTI4bHg5bkcwUW9tSFQwcnFMbDk1c2JqMW9GTEZkQ05Jc1N2MXNHd0RaK3pDR2MyazNMSXVTbXc2RzM4UUhvcWhwQi8tLWNkUnhKcVJ1ZDZvdHd0c1IzTm5TVlE9PQ%3D%3D--e612c129a0e500d4de110a24d907681a92e85128; _gitlab_session=2790c0a7b5bcf5f12c7596231578bd61; event_filter=all'
TOKEN = "r7o20BME1GsCG87bYaq9HtK6CXThQD3PoovtVQ3wUzoiklmrPFCglhTpdGatgwz6G14vBWg6t-vfxct4WLP7FQ"
#-------------- 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Host': GITLAB_HOST,
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie':COOKIE
    }

session = requests.Session()
session.headers.update(headers)

createProjectPayloads = {
    "authenticity_token":TOKEN,
    "project[ci_cd_only]": False,
    "project[name]": "ios-framework-bdsdebug",
    "project[selected_namespace_id]": 3,
    "project[namespace_id]":3,
    "project[path]":"ios-framework-bdsdebug",
    "project[visibility_level]":0
}

deleteProjectPayloads = {
    "authenticity_token":TOKEN,
    "_method": "delete",
}

# Gitlab创建工程（工程所属群组/个人ID，工程名称）// 名称全小写
def createProject(namespaceId, projectName):
    createProjectPayloads["project[selected_namespace_id]"] = namespaceId
    createProjectPayloads["project[namespace_id]"] = namespaceId
    createProjectPayloads["project[name]"] = projectName
    createProjectPayloads["project[path]"] = projectName
    apiUrl = "%s/projects"%GITLAB_URL
    ret = session.post(apiUrl, timeout=3,params=createProjectPayloads)
    print(projectName," ---> ",ret.status_code) 


# # Gitlab删除工程（工程所属群组/个人ID，工程名称）// 名称全小写
# def deleteProject(namespace, projectName):
#     apiUrl = "%s/bds/%s"%(GITLAB_URL,namespace+"-"+projectName)
#     print(apiUrl)
#     ret = session.post(apiUrl, timeout=3,params=deleteProjectPayloads)
#     print(projectName," ---> ",ret.status_code) 

data = '''
auction-website
bag-transaction
bdsjs
bds-mp-app
chunxi
cms
cycx
doc
dol-customer-app
dol-lab-app
dol-oms
elements
h5
identify
jz-appraisal
lingque
ocms
packages
saas
sl-h5
sloms
slyxoms
static
test-js
website
webview
wechat
wx-activities
'''

if __name__ == '__main__':
    i = 0
    for p in data.split("\n"):
        i+=1
        if i > 2:
            break 
        deleteProject("front-end-web",p)
    



