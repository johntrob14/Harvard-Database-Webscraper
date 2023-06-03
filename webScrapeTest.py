from bs4 import BeautifulSoup
import requests


def main():
    page = requests.get("https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=6671509a1")
    page2 = requests.get("https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=6671509a2")
    # print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    #soup2 = BeautifulSoup(page.content, 'html.parser')
    print('with verification')
    print(soup.prettify())
    #print('without verification')
    #print(soup2.prettify())
    x = soup.get_text()
    print('x')
    print(x)
    html = list(soup.children)[1]
    #html2 = list(soup2.children)[1]
    # print(html.text)
    #print(html2.text)


main()
