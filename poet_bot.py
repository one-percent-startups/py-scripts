import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.browser import CreateDriver
import xlrd
from json_excel_converter import Converter
from json_excel_converter.xlsx import Writer
# from allocated import get_allocate
import os
from Resource import PathResource as path

file1 = open("record.txt", "a")

driver = CreateDriver()
driver.get(
    'http://kavitakosh.org/kk/%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A5%80_%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A5%80')
time.sleep(5)
pls = driver.find_elements(By.CLASS_NAME, 'poet-list-section')
data = []
links = []
for n, seci in enumerate(pls):
    lis = seci.find_elements(By.TAG_NAME, 'li')
    for l in lis:
        links.append(l.find_element(By.TAG_NAME, 'a').get_attribute('href'))
print(len(links))
for n, poet in enumerate(links[2800:]):
        try:
            obj = {}
            obj['poems'] = []
            driver.get(poet)
            obj['name'] = driver.find_element(By.ID, 'kkparichay-name').text
            try:
                obj['imageurl'] = driver.find_element(By.CLASS_NAME, 'kkparichay-poet-photo').get_attribute('src')
            except:
                obj['imageurl'] = ''

            sin_links = []
            for sin in driver.find_element(By.ID, 'mw-content-text').find_elements(By.TAG_NAME, 'li'):
                sin_links.append(sin.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            # print(sin_links)
            for sinli in sin_links:
                try:
                    driver.get(sinli)
                    WebDriverWait(driver, 9).until(
                        EC.presence_of_element_located((By.ID, "firstHeading")))
                    poem_obj = {}
                    poem_obj['name']=obj['name']
                    poem_obj['imageurl']=obj['imageurl']
                    poem_obj['poem_name'] = driver.find_element(By.ID, 'firstHeading').find_element(By.TAG_NAME, 'span').text
                    poem_obj['content'] = driver.find_element(By.CLASS_NAME, 'poem').find_element(By.TAG_NAME, 'p').text
                    poem_obj['tags'] = []
                    tags = driver.find_element(By.ID, 'mw-normal-catlinks').find_elements(By.TAG_NAME, 'li')
                    for t in tags:
                        poem_obj['tags'].append(t.find_element(By.TAG_NAME, 'a').text)
                    data.append(poem_obj)
                    print(poem_obj)
                except:
                    continue
            # conv = Converter()
            # conv.convert(data, Writer(file=f'data{n}.xlsx '))



        except Exception as e:
            print('----------',e)
            continue

        # obj={}
        # obj['name']=l.find_element(By.TAG_NAME,'a').text
        # obj['poems']={}

        # data.append(obj)
        # json_object=json.dumps(data)
        # conv = Converter()
        # conv.convert(data, Writer(file='data.xlsx '))
conv = Converter()
conv.convert(data, Writer(file=f'data_khatam.xlsx'))