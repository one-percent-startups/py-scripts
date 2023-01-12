import json
import re
import sys
from selenium.webdriver.common.by import By

from Utils.browser import CreateDriver


file1 = open("record.txt", "a")

driver = CreateDriver()
link=sys.argv[0]
driver.get(link)
h1 = f"""<h1>{driver.find_element(By.XPATH, "//h1[@data-test-id='lesson-title-header']").text}</h1>"""
h6 = f"""<h6>{driver.find_element(By.XPATH, "//h2[@data-test-id='course-title-header']").text}</h6>"""
# driver.execute_script('var element = document.querySelectorAll(".anchor-link");'
#                                   'arrFiltered.forEach(function (el){el.parentNode.removeChild(el);})')
fin = ''
sections = driver.find_elements(By.TAG_NAME, 'section')
for sec in sections:
    header = sec.find_element(By.CLASS_NAME, 'anchor-link').get_attribute('innerText')
    kamke = sec.find_elements(By.XPATH, '*')[1:]
    tt = ''
    for kam in kamke:
        temp = kam.get_attribute('outerHTML')
        re.sub('class=".*?"', '', temp, flags=re.DOTALL)
        temp.replace('<code>','<span class="highlight">')
        temp.replace('</code>','</span>')
        tt += temp
    fin += f"""<h2>{header}</h2><div class="content">{tt}</div>"""

f = open(f"{link.split('/')[-1]}.html", "a")
f.write(f'{h1}{h6}{fin}')
f.close()
