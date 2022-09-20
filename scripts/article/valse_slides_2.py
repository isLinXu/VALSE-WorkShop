# Download PDF files from:
# http://valser.org/portal.php?mod=attachment&id=1
# http://valser.org/portal.php?mod=attachment&id=2
# ……
# http://valser.org/portal.php?mod=attachment&id=79

# Python download without supplying a filename - Stack Overflow
# https://stackoverflow.com/questions/2795331/python-download-without-supplying-a-filename

import cgi
import urllib
from urllib.request import urlopen
from urllib.request import urlretrieve

for num in range(1, 80, 1):
    if num != 11:
        url = 'http://valser.org/portal.php?mod=attachment&id={}'.format(num)
        remotefile = urlopen(url)
        blah = remotefile.info()['Content-Disposition']
        value, params = cgi.parse_header(blah)
        filename = params["filename"]

        filename_new = "{:0>2d} {}".format(num, filename)
        print(filename_new)

        # 11, 15, 41, 65
        try:
            urlretrieve(url, filename_new)
        except urllib.error.ContentTooShortError:
            print("{:0>2d} error".format(num))