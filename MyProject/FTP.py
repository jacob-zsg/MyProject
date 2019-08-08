# coding=utf-8

import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import configparser
import logging

def main():
    # 新建一个用户组
    authorizer = DummyAuthorizer()

    # 读取用户配置
    config = configparser.ConfigParser()
    config.read("init.ini", encoding="utf-8")

    user_list = config.sections()
    for user in user_list:
        if user == "syscfg":
            syscfg = user
        else:
            passwd = config[user]["password"]
            perm = config[user]["perm"]
            home_dir = config[user]["home"]
            # 将用户名，密码，指定目录，权限 添加到里面
            authorizer.add_user(user, passwd, homedir=home_dir, perm=perm)

    # 添加匿名用户 只需要路径
    if config[syscfg]["ENABLE_ANONYMOUS"] == 'on':
        authorizer.add_anonymous(config[syscfg]["ANONYMOUS_PATH"])

    # 下载上传速度设置
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = config[syscfg]["MAX_DOWNLOAD"]
    dtp_handler.write_limit = config[syscfg]["MAX_UPLOAD"]

    # 初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer

    # 欢迎信息
    handler.banner = config[syscfg]["WELCOME_MSG"]

    # 监听ip 和 端口
    server = FTPServer((config[syscfg]["IP"], int(config[syscfg]["PORT"])), handler)

    # 最大连接数
    server.max_cons = config[syscfg]["MAX_CONS"]
    server.max_cons_per_ip = config[syscfg]["MAX_PER_IP"]

    #日志路径
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename=config[syscfg]["LOGING_NAME"], level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, filemode='a+')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)

    # 开始服务
    logging.debug("FTP service %s starts listening" % (config[syscfg]["IP"] + ":" + config[syscfg]["PORT"]))
    server.serve_forever()

if __name__=="__main__":
    main()