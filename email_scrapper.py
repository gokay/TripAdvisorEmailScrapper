import requests
import xlwt
from bs4 import BeautifulSoup
import time

page_url = 'https://www.tripadvisor.com.tr/Restaurants-g293974-Istanbul.html'


def getPageList(urlString):
    """ This function gets the last page in given URL

    Parameters:
    urlString (str): URL of the page

    Returns:
    int: Last page number value

   """
    page_links1 = []
    page_links2 = []

    r1 = requests.get(urlString)
    soup1 = BeautifulSoup(r1.content, 'html.parser')

    for link in soup1.findAll('a', {'class': 'pageNum'}):
        page_links1.append(link['data-page-number'])

    page_links2.append(1)
    page_links2.append(int(page_links1[-1]))

    print('getPageList fonksiyonu çalıştı')
    # print(f'SAYFALAR1 = {page_links1}')
    # print(f'SAYFALAR2 = {page_links2}')

    # return page_links1
    print('getPageList fonksiyonu bitti')
    return int(page_links1[-1])


def constructUrls(lastPage):
    url_list = []
    i = 0

    print('constructUrl fonksiyonu çalıştı')

    for page in range(1, lastPage):
        i += 30
        currentPage = 'https://www.tripadvisor.com.tr/Restaurants-g293974-oa' + str(
            i) + '-Istanbul.html#EATERY_LIST_CONTENTS'

        r = requests.get(currentPage)
        soup = BeautifulSoup(r.content, 'html.parser')

        for link in soup.findAll('a', {'class': 'property_title'}):
            try:
                url_list.append('https://www.tripadvisor.com.tr' + link['href'])
                # print('https://www.tripadvisor.com.tr' + link['href'])
            except KeyError:
                pass

                # print (currentPage)
        # url_list.append(currentPage)

        if (lastPage * 30) < i:
            break

    return url_list


def getAllEmailsInUrls(allPages):
    print('getAllEmailsInUrls fonksiyonu çalıştı')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Emails')
    ws.write(0, 0, 'Emails')

    emailList = []
    L = []
    r = 0
    u = 0

    # print(f'allPages = {allPages}')

    for page in allPages:
        # getH=requests.get(urlString)
        getH = requests.get(page)
        h = getH.content
        soup = BeautifulSoup(h, 'html.parser')
        mailtos = soup.select('a[href^=mailto]')
        for i in mailtos:
            href = i['href']
            try:
                str1, str2 = href.split(':')
            except ValueError:
                break

            emailList.append(str2)
            print(str2)
            # time.sleep(5)

            # adding scraped emails to an excel sheet
            for email in emailList:
                email = email.replace('?subject=?', '')
                r = r + 1
                ws.write(r, 0, email)
                # print(f'email = {email}')

        wb.save('emails.xls')
    print('getAllEmailsInUrls fonksiyonu bitti')


print('###########################################################')

# def getPageList(page_url)
# getPageList(page_url)

# def constructUrls(lastPage)
# constructUrls(getPageList(page_url))

# def getAllEmailsInUrls(allPages)
getAllEmailsInUrls(constructUrls(getPageList(page_url)))
