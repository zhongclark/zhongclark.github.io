#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import fileinput
# 使用 pod cache list 查看看缓存

# 使用 pod cache clean --all 清除缓存


# 如果上传 pod 库成功了 但是却搜索不到这个库 可以在终端进行以下操作
# 1.pod sutup
# 2.rm ~/Library/Caches/CocoaPods/search_index.json


# 忽略警告上传代码

# pod repo push QGSpecs QGTool.podspec --allow-warningsc (允许警告上传代码)



# pod 更新本地的索引文件

# pod update --no-repo-update

# 1、注册账号: pod trunk register garretming@outlook.com 'Clark8' --description='Clark MacBook Air' --verbose
# // 注册完成后，[pod trunk me]查看信息
# pod trunk me

# 2.创建.podspec文件
# cd /Users/hans/HKHttpManager/HKHttpManager //到clone下来的文件目录下
# $ pod spec create [NAME]
# > [NAME]: podspec 名称，与工程名相同

# 在使用git clone https://github.com/CocoaPods/Specs 报:[!] Unable to add a source with url https://github.com/CocoaPods/Specs.git named master-1.
# You can try adding it manually in ~/.cocoapods/repos or via pod repo add.

# 解决答案:
# $ brew remove git
# $ brew remove curl

# $ brew install openssl
# $ brew install --with-openssl curl
# $ brew install --with-brewed-curl --with-brewed-openssl git


#python3 auto.py btrouter https://gitlab.com/Clark8/btrouter.git
# pod repo add specs https://gitlab.com/Clark8/btrouter.git
def podCommandEdit():
    global lib_command
    global pod_push_command
    source_suffix = 'https://github.com/CocoaPods/Specs.git,'+sourcePath
    # 如果找不到依赖库，--source一定要包含你引用的私有库组件
    # lib_command = 'pod lib lint --verbose --no-clean --use-libraries --allow-warnings --sources='
    lib_command = 'pod lib lint --no-clean --allow-warnings --sources='
    pod_push_command = 'pod repo push ' + project_name + ' ' + podspec_file_name
    if len(sources) > 0:
        # rely on  private sourece
        pod_push_command += ' --sources='

        for index,source in enumerate(sources):
            lib_command += source
            lib_command += ','
            pod_push_command += source
            pod_push_command += ','

        lib_command += source_suffix
        pod_push_command += source_suffix

    else:
        lib_command = 'pod lib lint'


def updateVersion():
    f = open(spec_file_path, 'r+')
    infos = f.readlines()
    f.seek(0, 0)
    file_data = ""
    new_line = ""
    global find_version_flag

    for line in infos:
        if line.find(".version") != -1:
            if find_version_flag == False:
                # find s.version = "xxxx"

                spArr = line.split('.')
                last = spArr[-1]
                last = last.replace('"', '')
                last = last.replace("'", "")
                newNum = int(last) + 1

                arr2 = line.split('"')
                arr3 = line.split("'")

                versionStr = ""
                if len(arr2) > 2:
                    versionStr = arr2[1]

                if len(arr3) > 2:
                    versionStr = arr3[1]
                numArr = versionStr.split(".")

                numArr[-1] = str(newNum)
                # rejoint string
                global new_tag
                for index,subNumStr in enumerate(numArr):
                    new_tag += subNumStr
                    if index < len(numArr)-1:
                        new_tag += "."

                # complete new_tag

                if len(arr2) > 2:
                    line = arr2[0] + '"' + new_tag + '"' + '\n'

                if len(arr3) > 2:
                    line = arr3[0] + "'" + new_tag + "'" + "\n"

                # complete new_line

                print("this is new tag  " + new_tag)
                find_version_flag = True

        file_data += line


    with open(spec_file_path, 'w', ) as f1:
        f1.write(file_data)

    f.close()

    print("--------- auto update version -------- ")


def libLint():
    print("-------- waiting for pod lib lint checking ...... ---------")
    os.system(lib_command)

def gitOperation():
    os.system('git add .')
    commit_desc = "version_" + new_tag
    commit_command = 'git commit -m "' + commit_desc + '"'
    os.system(commit_command)
    # git push
    r = os.popen('git symbolic-ref --short -q HEAD')
    current_branch = r.read()
    r.close()
    push_command = 'git push origin ' + current_branch
    
    # tag
    tag_command = 'git tag -m "' + new_tag + '" ' + new_tag
    os.system(tag_command)
    
    # push tags
    os.system('git push --tags')

def podPush():
    print("--------  waiting for pod push  ...... ---------")
    os.system(pod_push_command)




def main(argv):
    global new_tag
    global lib_command
    global pod_push_command
    global spec_file_path
    global find_version_flag
    global sources
    global project_name
    global podspec_file_name
    global sourcePath
    # ======================  edit by yourself  ======================
    sourcePath = argv[1]
    sources = [
            #'https://github.com/YinTokey/Egen.git',
            argv[1],
            ]

    project_name = argv[0]+'-master'
    podspec_file_name = argv[0]+'.podspec'


    # ==================================================================

    new_tag = ""
    lib_command = ""
    pod_push_command = ""
    spec_file_path = "./" + podspec_file_name
    find_version_flag = False


    updateVersion()
    podCommandEdit()
    libLint()
    gitOperation()
    podPush()
    
   
# run commands
if __name__ == '__main__':
    main(sys.argv[1:])
   




