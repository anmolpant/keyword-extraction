import urllib3
from bs4 import BeautifulSoup

def spider(name,url, found_titles, found):
    try:
        page = urllib3.urlopen(url)
        soup = BeautifulSoup(page,'html.parser')

        title = soup.title.string.lower()
        keywords = soup.select('meta[name="keywords"]')[0]['content'].lower().split(', ')

        if name in keywords:
            keywords.remove(name)
        
        cleaned_keywords = []
        for k in keywords:
            if k in title:
                cleaned_keywords.append(k)
        
        if len(cleaned_keywords) > 0 and title not in found_titles:
            found_titles.append(title)

            print (title)
            print (cleaned_keywords)
            print

            f=open('keyword_data.txt','a')
            f.write(
                title + "\t" + ' '.join(
                    k.replace(' ','_') for k in cleaned_keywords
                ) + "\n"
            )
            f.close()

        for a in soup.select('a[href]'):
            b = a['href'].replace('#replies', '')
            if 'http://' + name +'.com' in b and b not in found:
                found.append(b)
                spider(name, b, found_titles, found)
    


def main():
    name