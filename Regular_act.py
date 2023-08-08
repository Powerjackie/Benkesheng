# Luo Y
# 2023-04-19
# **-*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    InvalidArgumentException,
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    ElementNotSelectableException,
    MoveTargetOutOfBoundsException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import configparser

# 获取当前文件所在目录的绝对路径,构造相对路径
config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
# 读取配置文件
config = configparser.ConfigParser()
with open(config_path, encoding='utf-8') as f:
    config.read_file(f)

time = config['time']
WAIT_TIME = int(time['WAIT_TIME'])



class elementselector:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def interact_element(self, locator, locator_type='xpath', wait_type='explicit', n=1, input_text=None, clear=False,
                    submit=False, get_attribute=None, switch=None, execute_script=None, drag=None, visible=False,
                    enabled=False, selected=False):
        """
        通用的元素操作函数
        :param driver: webdriver对象
        :param locator: 元素定位表达式
        :param locator_type: 元素定位方式，默认为xpath
        :param wait_type: 等待方式，默认为显式等待
        :param n: 操作类型，1：点击，2：执行脚本模拟点击，3：鼠标点击
        :param input_text: 需要输入的文本，如果不为None，则执行输入操作
        :param clear: 是否需要清空元素内容
        :param submit: 是否需要提交表单
        :param get_attribute: 需要获取的元素指定属性的值，如果不为None，则返回该值
        :param switch: 是否需要切换浏览器窗口或 iframe
        :param execute_script: 需要执行的 JavaScript 代码，如果不为None，则执行该代码
        :param drag: 是否需要模拟拖拽操作
        :param visible: 是否需要判断元素是否可见
        :param enabled: 是否需要判断元素是否可用
        :param selected: 是否需要判断元素是否被选中
        :param select_option: 需要选择的下拉选项，如果不为None，则选择该选项
        :param select_locator_type: 下拉列表元素的定位方式，默认为value
        """
        if wait_type == 'explicit':
            if visible:
                try:
                    element = self.wait.until(EC.visibility_of_element_located((getattr(By, locator_type.upper()), locator)))
                except (TimeoutException, InvalidArgumentException, NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException, ElementNotSelectableException, MoveTargetOutOfBoundsException):
                    return None
            elif enabled:
                try:
                    element = self.wait.until(EC.element_to_be_clickable((getattr(By, locator_type.upper()), locator)))
                except (TimeoutException, InvalidArgumentException, NoSuchElementException, StaleElementReferenceException,
                         ElementNotInteractableException, ElementClickInterceptedException, ElementNotSelectableException, MoveTargetOutOfBoundsException):
                    return None
            elif selected:
                try:
                    element = self.wait.until(EC.element_to_be_selected((getattr(By, locator_type.upper()), locator)))
                except (TimeoutException, InvalidArgumentException, NoSuchElementException, StaleElementReferenceException, 
                        ElementNotInteractableException, ElementClickInterceptedException, ElementNotSelectableException, MoveTargetOutOfBoundsException):
                    return None
            else:
                try:
                    element = self.wait.until(EC.presence_of_element_located((getattr(By, locator_type.upper()), locator)))
                except (TimeoutException, InvalidArgumentException, NoSuchElementException, 
                        StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException, ElementNotSelectableException, MoveTargetOutOfBoundsException):
                    return None
                
        else:
            self.driver.implicitly_wait(10) # 10秒超时时间，可以根据需要修改
            try:
                element = self.driver.find_element(getattr(By, locator_type.upper()), locator)
            except (...):
                return None
            else:
                pass

        if switch is not None:
            if switch == 'default':
                self.driver.switch_to.default_content()
            else:
                self.driver.switch_to.frame(switch)

        if execute_script is not None:
            self.driver.execute_script(execute_script, element)  # 执行的是一个自定义的 JavaScript 脚本zz

        if n == 1:
            try:
                element.click()
            except UnboundLocalError:
                print("Error")
                return None
        elif n == 2:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except (InvalidArgumentException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException):
                return None
        elif n == 3:
            try:
                ActionChains(self.driver).click(element).perform()
            except (InvalidArgumentException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException):
                return None
        if clear:
            try:
                element.clear()
            except (InvalidArgumentException, StaleElementReferenceException, ElementNotInteractableException):
                return None

        if input_text is not None:
            if clear:
                element.clear()
            element.send_keys(input_text)

        if get_attribute is not None:
            return element.get_attribute(get_attribute)

        if drag is not None:
            ActionChains(self.driver).drag_and_drop(element, drag).perform()

        if submit:
            element.submit()

        return element


    def select_option_element(self,element, locator,  select_option=None):
            """
            选择下拉列表选项
            :param locator: 下拉列表元素的定位表达式
            :param select_option: 需要选择的下拉选项
            """
            if select_option is not None:
                select = Select(element)
                select.select_by_value(locator)