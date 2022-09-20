# Download PDF files from:
# http://valser.org/article-269-1.html
# http://valser.org/article-270-1.html
# ……
# http://valser.org/article-356-1.html

import re
import os
import string
import urllib.request
from urllib.parse import quote

# open the url and read
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('UTF-8')
    page.close()
    return html

# compile the regular expressions and find the stuff we need
def getUrl(html):
    reg1 = r'http://valser.org/webinar/slide/slides/.*?.pdf'
    url_lst1 = re.compile(reg1).findall(html)

    reg2 = r'http://valser.org/webinar/slide/slides/.*?.PDF'
    url_lst2 = re.compile(reg2).findall(html)

    url_lst = url_lst1 + url_lst2

    return(url_lst)

# download the file with certain url
def getFile(url, file_name):
    f = open(file_name, 'wb')

    url_new = quote(url, safe = string.printable)
    u = urllib.request.urlopen(url_new)
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)

    f.close()

# Processing pages
pageNum = 400
for page in range(269, 357, 1):
    print('Processing {}/{} pages'.format(page, pageNum))
    url_raw = 'http://valser.org/article-{}-1.html'.format(page)

    html = getHtml(url_raw)
    url_lst = getUrl(html)

    cnt = 0
    for url in url_lst[:]:
        cnt += 1
        file_name = '{}{} {}'.format(page, cnt, url.split('/')[-1])
        print(file_name)
        getFile(url, file_name)