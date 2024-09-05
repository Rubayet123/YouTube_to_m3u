import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

windows = False
if 'win' in sys.platform:
    windows = True

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Automatically download and setup ChromeDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

def grab(url):
    driver.get(url)  # Use Selenium to get the page
    response = driver.page_source  # Get the page source after JavaScript is executed

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response, 'html.parser')

    # Extract all text content (or modify this as needed to extract specific tags)
    text_content = soup.get_text()

    # Save the extracted text to a file
    with open('extracted_content.txt', 'a') as file:
        file.write(f"\n\nURL: {url}\n")
        file.write(text_content)

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

# Close the Selenium WebDriver
driver.quit()
