# Luo Y
# 2023-08-03
# -*- coding: utf-8 -*-
from Regular_act import *

class loginhandler:
    def __init__(self, driver):
        self.driver = driver
        self.element = elementselector(self.driver)

    def login(self, username, password,website,user,pwd,log):
        self.driver.get(website)
        if username != None:
            try:
                self.element.interact_element(locator_type='id',locator=user,input_text=username)
                self.element.interact_element(locator_type='id',locator=pwd,input_text=password)
                self.element.interact_element(locator_type='id',locator=log, n=1)
                print("Login successfully")

            except Exception as e:
                raise e
                print("Login failed")

        else:
            print('Please input username and password')
