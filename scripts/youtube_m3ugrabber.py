import requests
import os
import sys
from bs4 import BeautifulSoup

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    response = requests.get(url, timeout=15).text
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response, 'html.parser')
    
    # Extract all text content (or modify this as needed to extract specific tags)
    text_content = soup.get_text()
    
    # Save the extracted text to a file
    with open('extracted_content.txt', 'a') as file:
        file.write(f"\n\nURL: {url}\n")
        file.write(text_content)
    
    # Continue with your existing logic to find .m3u8 links
    if '.m3u8' not in response:
        if windows:
            print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')
            return
        
        os.system(f'curl "{url}" > temp.txt')
        response = ''.join(open('temp.txt').readlines())
        
        if '.m3u8' not in response:
            print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')
            return
    
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner : end]:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    
    print(f"{link[start : end]}")

print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')

# Make sure 'banner' is defined or remove this line
# print(banner)

# Open the file containing YouTube channel information
with open('../youtube_channel_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            grab(line)
            
# Clean up temporary files if they exist
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
