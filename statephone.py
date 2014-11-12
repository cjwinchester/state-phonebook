from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time

driver = webdriver.Chrome()
driver.get("https://ne-phonebook.ne.gov/PhoneBook/faces/welcome.jsp")

print "Connected!"

f = open('phonebook.txt', 'wb')

elem = driver.find_element_by_id('welcomeForm:nameSearchButton')
elem.click()

page = driver.page_source
soup = BeautifulSoup(page)

regexin = re.search(r'Page 1/\d+', str(soup))
targetpage = regexin.group().replace("Page 1/","")
pagelimit = int(targetpage)

counter = 0

while counter < pagelimit:
    print "souping page " + str(counter)
    page = driver.page_source
    soup = BeautifulSoup(page)
    table = soup.find('table', {'id':'resultsForm:phoneBook'})

    for row in table.findAll('tr')[1:]:
        col = row.findAll('td')
        rest = col[0].text.strip()
        last = col[1].text.strip()
        print rest + " " + last
        agencyblob = col[2].text.strip().split(' -- ')
        agencyname = agencyblob[0].replace(', DEPARTMENT OF','').replace(', DEPT OF','').replace('PATROL, NEBRASKA STATE', 'NEBRASKA STATE PATROL')
        agencynum = agencyblob[1].replace('AGENCY ','')
        division = col[3].text.strip()
        phone = col[4].text.strip()
        email = str(col[5].a['href']).replace('mailto:','')
        rec = (last, rest, agencyname, agencynum, division, phone, email)
        f.write("|".join(rec) + "\n")

    next = driver.find_element_by_id('resultsForm:dtNext_Msg')
    next.click()
    counter += 1
    time.sleep(1)
    
f.flush()
f.close()
driver.close()