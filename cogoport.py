import json
import re
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
driver.get('https://github.com/freeCodeCamp/freeCodeCamp/tree/main/curriculum/challenges/english')
time.sleep(5)
ni = driver.find_elements(By.CLASS_NAME, 'js-navigation-item')
exes = ["Create a Text Field",
        "Add Placeholder Text to a Text Field",
        "Create a Form Element",
        "Add a Submit Button to a Form",
        "Use HTML5 to Require a Field",
        "Create a Set of Radio Buttons",
        "Create a Set of Checkboxes",
        "Use the value attribute with Radio Buttons and Checkboxes",
        "Check Radio Buttons and Checkboxes by Default"]
stack = []
for n in ni:
    try:
        stack.append(n.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    except:
        continue
print(stack)
exercises = []
for s in stack[6:]:
    stack2 = []
    driver.get(s)
    #
    # WebDriverWait(driver, 40).until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, "box")))
    time.sleep(3)
    sin = driver.find_elements(By.CLASS_NAME, 'js-navigation-item')
    for s in sin:
        try:
            stack2.append(s.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        except:
            continue
    for st in stack2[6:]:
        driver.get(st)
        time.sleep(3)
        stack3 = []
        mds = driver.find_elements(By.CLASS_NAME, 'js-navigation-item')
        for m in mds:
            try:
                exname = m.find_element(By.TAG_NAME, 'a').text
                for name in exes:
                    if name.replace(' ', '-').lower() in exname:
                        stack3.append(m.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                continue
        print('mds==============', stack3)
        for s3 in stack3:
            sinex = {}
            driver.get(s3)
            time.sleep(3)
            driver.execute_script('var element = document.querySelector(".zeroclipboard-container");'
                                  'console.log(element);'
                                  'if (element) element.parentNode.removeChild(element);')
            celems = driver.find_element(By.ID, 'readme').find_element(By.TAG_NAME, 'article').find_elements(By.XPATH,
                                                                                                             '*')
            order = ['Description', 'Instruction', 'Hint', 'Seeds', 'Solution']
            flag = 0
            for cc in celems:

                pointer = order[0]
                print('-----------', cc.tag_name)
                print(sinex.keys(), pointer, order)
                if cc.tag_name == 'h1' and flag == 0:
                    sinex[pointer] = ''
                    flag = 1
                elif cc.tag_name == 'h1' and flag == 1:
                    order.remove(pointer)
                    pointer = order[0]
                    sinex[pointer] = ''

                elif pointer in list(sinex.keys()) and pointer != 'Seeds':
                    temp=str(cc.get_attribute('outerHTML')).replace('"', "'")
                    re.sub('<svg".*?</svg>', '', temp, flags=re.DOTALL)

                    sinex[pointer] +=temp
            exercises.append(sinex)
json_object = json.dumps(exercises, indent=4)

# Writing to sample.json
with open("cogo.json", "w") as outfile:
    outfile.write(json_object)
