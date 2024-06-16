import re
import os
import string
import urllib.request
from urllib.parse import quote
from tqdm import tqdm


class PDFDownloader:
    def __init__(self, start_page=1, end_page=10000, base_url='http://valser.org/article-{}-1.html'):
        self.start_page = start_page
        self.end_page = end_page
        self.base_url = base_url

    # Get the HTML content of the given URL
    def get_html(self, url):
        page = urllib.request.urlopen(url)
        html = page.read().decode('UTF-8')
        page.close()
        return html

    # Extract the PDF URLs from the HTML content
    def get_urls(self, html):
        reg1 = r'http://valser.org/webinar/slide/slides/.*?.pdf'
        url_lst1 = re.compile(reg1).findall(html)

        reg2 = r'http://valser.org/webinar/slide/slides/.*?.PDF'
        url_lst2 = re.compile(reg2).findall(html)

        url_lst = url_lst1 + url_lst2

        return (url_lst)

    # Download the PDF file from the URL and save it with the given file name
    def download_file(self, url, file_name):
        with open(file_name, 'wb') as f:
            url_new = quote(url, safe=string.printable)
            u = urllib.request.urlopen(url_new)
            block_sz = 8192
            with tqdm(total=u.length, unit='B', unit_scale=True, desc=file_name) as pbar:
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                    f.write(buffer)
                    pbar.update(len(buffer))

    # Process each page, download the PDF files, and skip the existing files
    def process_pages(self):
        for page in range(self.start_page, self.end_page + 1):
            print(f'Processing {page}/{self.end_page} pages')
            url_raw = self.base_url.format(page)

            html = self.get_html(url_raw)
            url_lst = self.get_urls(html)

            cnt = 0
            for url in url_lst:
                cnt += 1
                file_name = f'{page}{cnt} {url.split("/")[-1]}'

                # Check if the file already exists, skip it if it does
                if os.path.exists(file_name):
                    print(f'{file_name} already exists, skipping...')
                    continue

                print(f'Downloading {file_name}')
                self.download_file(url, file_name)


if __name__ == "__main__":
    downloader = PDFDownloader()
    downloader.process_pages()