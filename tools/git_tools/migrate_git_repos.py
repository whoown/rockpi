# coding=utf-8
# -*- coding: UTF-8 -*-
# 用于GIT仓库整体复制迁移（包含所有分支及Commit记录）
#
import os
import subprocess
OLD_GIT_URL = "https://git.aishepin8.com/"
NEW_GIT_URL = "https://github.com/whoown/"

# 根据不同情况，以最低成本填入
GIT_REPOS_MAPPER = {
    "Android":["Hermes"],
    "iOS":[
        "documents",
        "app-Hermes",
        "framework-bdsbasecore", 
        "framework-bdsdebug", 
        "framework-bdsdycode",
        "tools-appdebuger",
        "tools-autoarchive",
        "tools-ipaarchive",
    ],
    "mobile":[
        "app_doc",
        "Bvlgari",
        "camera_plugin",
        "flutter-oc-plugin",
        "Mago",
        "MagoDemo",
        "message_plugin",
        "payment_plugin",
        "zm_payment_plugin",
    ],
    "server":[
        "aries",
        "aries_doc",
        "captcha",
        "admin_dashboard",
        "dashboard_api",
        "docs",
        "docsify",
        "gemini",
        "gemini_stat",
        "gemini_url",
        "go-mysql-elasticsearch",
        "micro_service",
        "notify",
        "third_party",
    ],
    "web":[
        "auction-website",
        "bag-transaction",
        "bdsjs",
        "bds-mp-app",
        "chunxi",
        "cms",
        "cycx",
        "doc",
        "dol-customer-app",
        "dol-lab-app",
        "dol-oms",
        "elements",
        "h5",
        "identify",
        "jz-appraisal",
        "lingque",
        "ocms",
        "packages",
        "saas",
        "sl-h5",
        "sloms",
        "slyxoms",
        "static",
        "test-js",
        "website",
        "webview",
        "wechat",
        "wx-activities",
    ],
    "zhangyan":[
        "CertMaker",
        "Audit",
    ],
    "juanpengke":[
        "sdcsrz",
        "feisu",
        "vue3-realize",
        "tools",
        "backend",
        "talkdata",
        "m-website",
    ],
}

# 根据GIT_REPOS_MAPPER解析新旧Git仓库的对应关系
def parse_git_migrate_map():
    migrate_map = {}
    for owner in GIT_REPOS_MAPPER:
        for repo in GIT_REPOS_MAPPER[owner]:
            group = owner
            if group == 'web':
                group = "front-end-web"
            oldUrl = "git@git.aishepin8.com:%s/%s.git"%(group,repo.lower())
            if group in ["zhangyan","juanpengke"]:
                group = "bds"
            if group == "front-end-web":
                group = "web"
            newRepo = ("%s-%s"%(group,repo)).lower()
            newUrl = "git@git.magotown.com:%s/%s.git"%("bds", newRepo)
            migrate_map[oldUrl] = newUrl
    return migrate_map


def migrate_single_repo(old_git, new_git):
    repoName = old_git.split("/")[-1]
    process = subprocess.Popen(["cmd"],stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    commands = [
        "chdir",
        "cd D:\\Work\\temp",
        "chdir",
        "git clone --bare %s\n"%(old_git),
        "cd %s"%(repoName),
        "git push --mirror %s\n"%(new_git)
    ]
    omniCmd = "\n".join(commands)+"\n"
    outs, errs = process.communicate(omniCmd.encode("gbk"))
    print(outs.decode("gbk"))

def migrate_repos(startIndex=-1, endIndex=-1):
    n = 0
    migrate_info = parse_git_migrate_map()
    for old_git in migrate_info:
        if startIndex >=0 and n < startIndex:
            n += 1
            continue
        if endIndex >=0 and n >= endIndex:
            break 
        new_git = migrate_info[old_git]
        print(n,": ", old_git, '--->', new_git)
        migrate_single_repo(old_git,new_git)
        n+=1


########################

if __name__ == '__main__':
    # for owner in GIT_REPOS_MAPPER:
    #     for repo in GIT_REPOS_MAPPER[owner]:
    #         if owner == "web":
    #             print(repo)
    migrate_repos(startIndex=10,endIndex=-1)  


