# Luo Y
# 2023-04-19
# *-* coding: utf-8 *-*
import time
import threading
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import os

# 构造webdriver相对路径
executable_path = os.path.join(os.path.dirname(__file__), 'config/msedgedriver.exe')

# 初始化与关闭浏览器实例
class Browser:

    _driver = None
    _lock = threading.Lock()

    @classmethod
    def get_driver(cls,IMPLICIT_TIME,headless):
        with cls._lock:
            try:
                if cls._driver is None:
                    start_time = time.time()
                    service = Service(executable_path=executable_path)
                    options = Options()
                    options.use_chromium = True
                    options.add_argument("--disable-usb-keyboard-detect")
                    options.add_argument("--disable-extensions")
                    if headless:
                        options.add_argument("--headless")
                    cls._driver = webdriver.Edge(service=service, options=options)
                    cls._driver.implicitly_wait(IMPLICIT_TIME)  # 设置隐式等待时间
                    end_time = time.time()
                    print("Browser started in {:.2f} seconds".format(end_time - start_time))
            
            except Exception as e:
                raise e
                print(f"Error creating driver")

        return cls._driver

    @classmethod
    def close_browser(cls):
        if cls._driver is not None:
            try:
                cls._driver.quit()
                cls._driver = None
            except Exception as e:
                print(f"Error closing browser")
