# This is a sample Python script.
import requests
import csv
from bs4 import BeautifulSoup
import shutil
import itertools

# a basic csv row writer function
def write(s, file):
    with open(file, 'a') as f:
        # create the csv writer
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(s)
        # write a row to the csv file


# initialize an array of string values and labels for the csv data
def main():
    header = ['GenBank Accession', 'PrimerBankID', 'FPrimer', 'FPrimer length', 'FPrimer tm', 'FPrimer location',
              'RPrimer', 'RPrimer length', 'FPrimer tm', 'RPrimer location', 'Coding Sequence', 'Validation Results']
    #with open("toScrape.txt", 'r') as f:
      #  IDs = f.readlines() 
      # Deprecated - formerly attempting to only scrape known IDs
    
    max_length = 6 #Maximum String length of ID to search for
    for len in range(1,max_length):
        IDs = generate_IDs(len)
        write(IDs, "IDs.csv")
        print(IDs)
       
    write(header, file="scrape_all_entries.csv")
    count = 1
    with open(file="IDs.csv") as f:
        reader = csv.reader(f, lineterminator='\n')
        IDs  = reader.__next__()
        for x in IDs:
            url = "https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=" + x.strip()
            print("Trying: " + url)
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            all_html = soup.get_text()
            if ("No primer pair is found for" not in all_html):
                print("PrimerID Found")
                data = scrape(url, x.strip(), count)
                count += 1
                write(data, file="scrape_all_entries.csv")
            else:
                print("Failed")


def parse_coding_sequence(html_text, i):
    data = ''
    while len(html_text[i]) != 0:
        for n in range(len(html_text[i].split())):
            if n > 0 & n < len(html_text[i].split()) - 1:
                data += html_text[i].split()[n]
        i += 1

    return data
    # this is the final piece to finish, I need to parse the html file and make sure I only get the strings of
    # nucleotides this should also remove all spaces in the strings so that they are one large continuous stream of
    # nucleotide bases


# scrape will eventually use beautiful soup to extract all text from the html and parse the html for a row of values.
# the values will be returned as an array of strings which will be written by the write function

def validation_image_scrape(primer_id):
    url = "http://pga2.mgh.harvard.edu:8080/rtpcr/displayResult.do?primerPairId=" + primer_id
    image_soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    images = image_soup.findAll('Plot')
    y = image_soup.findAll('img')
    amp = y[8].attrs['src']
    diss = y[9].attrs['src']
    print(amp)
    url_base = "http://pga2.mgh.harvard.edu:8080"  # Original website
    url_ext = amp  # The extension you pulled earlier
    full_url = url_base + url_ext  # Combining first 2 variables to create       a complete URL
    r = requests.get(full_url, stream=True)  # Get request on full_url
    if r.status_code == 200:  # 200 status code = OK
        with open("images/" + primer_id + 'amp.jpg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    url_ext = diss  # The extension you pulled earlier
    full_url = url_base + url_ext  # Combining first 2 variables to create       a complete URL
    r = requests.get(full_url, stream=True)  # Get request on full_url
    if r.status_code == 200:  # 200 status code = OK
        with open("images/" + primer_id + 'diss.jpg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def scrape(s, primer_id, count):
    print("Accessing: " + s)
    print("number: " + str(count))
    soup = BeautifulSoup(requests.get(s).content, 'html.parser')
    all_html = soup.get_text().splitlines()
    y = soup.get_text()
    # print(all_html)
    data = []
    i = 0
    for x in all_html:
        if x == 'PrimerBank ID':
            data.append(all_html[i + 1])
        elif x == 'GenBank Accession':
            data.append(all_html[i + 1])
        elif x == 'Forward Primer':
            data.append(all_html[i + 1])
            data.append(all_html[i + 2])
            data.append(all_html[i + 3])
            data.append(all_html[i + 4])
        elif x == 'Reverse Primer':
            data.append(all_html[i + 1])
            data.append(all_html[i + 2])
            data.append(all_html[i + 3])
            data.append(all_html[i + 4])
        elif x == 'Location in Coding Sequence (primers and amplicon highlighted)':
            x = parse_coding_sequence(all_html, i + 4)
            data.append(x)
        i += 1

    if 'Validation Results' in y:
        data.append('YES')
        validation_image_scrape(primer_id)
    else:
        data.append('NO')

    return data

def generate_IDs(len):
    IDs = []
    # possible = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    # possible = 'abcdefghijklmnopqrstuvwxyz0123456789'
    possible = ['a','b','c','0','1','2','3','4','5','6','7','8','9']
    new = itertools.product(possible, repeat=len)
    for combo in new:
        IDs.append(''.join(combo))
        print(''.join(combo))
            
            
    return IDs
        
main()

