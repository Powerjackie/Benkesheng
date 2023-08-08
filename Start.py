# Luo Y
# 2023-08-03
# -*- coding: utf-8 -*-
def main():
    import os
    import configparser
    from Browser import Browser
    from Login import loginhandler

    # 获取当前文件所在目录构造相对路径
    current_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    # 读取配置文件
    config = configparser.ConfigParser()
    with open(current_path, encoding= 'utf-8') as f:
        config.read_file(f)

    login = config['login']
    website = 'https://jwgl.njtech.edu.cn/xtgl/login_slogin.html'
    username = login['username']
    password = login['password']
    user = 'yhm'
    pwd = 'mm'
    log = 'dl'
    headless = False
    IMPLICIT = 10

    # 定义全局变量
    driver = None
    try:
        # 创建浏览器实例
        driver = Browser.get_driver(IMPLICIT, headless)
        # 传入浏览器实例
        loginhandler = loginhandler(driver)

        # 登录
        loginhandler.login(username, password, website, user, pwd, log)

    except Exception as e:
        None
    
if __name__ == '__main__':
    main()

