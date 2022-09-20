# Download slides from: http://valser.org/webinar/slide/. 
# 2020-7-15 22:13:13

import re
import os
import string
import urllib.request
from urllib.parse import quote
import tqdm

# open the url and read
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 S#afari/537.36'}



from random import randint
 
USER_AGENTS = [
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
 
random_agent = USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
headers = {'User-Agent':random_agent,}

def getHtml(url):
    url_new=quote(url,safe=string.printable)
    req=urllib.request.Request(url=url_new, headers=headers)
    page=urllib.request.urlopen(req)
    html = page.read().decode('UTF-8')
    page.close()
    return html

# example: /webinar/slide/index.php/Home/Index/index/dir/20200710.html
# compile the regular expressions and find the stuff we need
def getDate(html):
    reg = r'/webinar/slide/index.php/Home/Index/index/dir/(\d{8}).html'
    tmp = re.compile(reg).findall(html)
    return tmp

# example:  <a target="_blank"  href="http://valser.org/webinar/slide/slides/20200710/howtoproperlyreviewaipapers-200710022751.pdf">howtoproperlyreviewaipapers-200710022751.pdf</a>
def getName(html):
    reg = r'<a target="_blank"  href="http://valser.org/webinar/slide/slides/(.*)/(.*)">(.*)</a>'
    tmp = re.compile(reg, re.IGNORECASE).findall(html)
    return tmp

# download a file
def getFile(url, file):
    f = open(file, 'wb')
    url_new = quote(url, safe = string.printable)
    u = urllib.request.urlopen(url_new)
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()

# make a directory to store the slides
slides_dir = 'slides'
if not os.path.exists(slides_dir):
    os.mkdir(slides_dir)

# store information of the slides
slides_info = 'slides_info'
FileHandle = open(slides_info, 'w', encoding='UTF-8')
FileHandle.close()

# main page: http://valser.org/webinar/slide/
url = 'http://valser.org/webinar/slide/'
html = getHtml(url)
date_list = getDate(html)

# example: http://valser.org/webinar/slide/index.php/Home/Index/index/dir/20200710.html
for date in date_list:
    url="http://valser.org/webinar/slide/index.php/Home/Index/index/dir/{}.html".format(date)
    try:
        html=getHtml(url)
    except:
        # output the error
        print("{} error".format(date))
        FileHandle = open(slides_info, 'a', encoding='UTF-8')
        FileHandle.write("{} error\n".format(date))
        FileHandle.close()
        continue

    file_list=getName(html)

    # example: http://valser.org/webinar/slide/slides/20200710/howtoproperlyreviewaipapers-200710022751.pdf
    #for i in tqdm(range(len(file_list))):
        #file = file_list[i][1]	
    for file in file_list:
        file=file[1]
        url="http://valser.org/webinar/slide/slides/{}/{}".format(date, file.replace(' ','%20')) # replace blank spaces
        file="{} {}".format(date, file)

        # output the file information
        print(file)
        FileHandle = open(slides_info, 'a', encoding='UTF-8')
        FileHandle.write("{}\n".format(file))
        FileHandle.close()

        # download the file
        getFile(url, "{}/{}".format(slides_dir, file))