import re
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

def main() -> None:
    website_url = sys.argv[1]
    if r := requests.get(website_url):
        soup = BeautifulSoup(r.text, 'html.parser')
        entries = []
        master_title = sys.argv[2]
        for li in soup.find_all('li', onclick = True):
            onclick = li['onclick']
            m = re.search(r"loadPlayer\('([^']+)'\)", onclick)
            video_url = m.group(1)
            ep_number, title = li.get_text(strip = True).split(maxsplit = 1)
            ep_number = ep_number[:-1]
            entries.append([ video_url, ep_number, title ])
        max_ep_number_len = max(map(len, map(lambda e: e[1], entries)))
        for e in entries:
            e[1] = '0' * (max_ep_number_len - len(e[1])) + e[1]
            ext = subprocess.getoutput(f'yt-dlp {e[0]} --print filename').split('.')[-1]
            ext = 'unknown' if ext is None or ext == '' else ext
            subprocess.run(f'yt-dlp {e[0]} -o "{master_title} - {e[1]} - {e[2]}.{ext}"', shell = True)

if __name__ == '__main__':
    main()
