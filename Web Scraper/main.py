import os
import re
import time
import csv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    input_file_path, output_file_path, cleaned_data_file_path = get_input_paths()

    # Read and process input data
    entries = read_and_process_input(input_file_path)

    # Initialize web scraping components
    driver = initialize_web_scraping()

    # Scrape and save links
    scrape_and_save_links(driver, entries)

    # Clean data and save
    cleaned_data_str = clean_data()
    save_cleaned_data(cleaned_data_str, cleaned_data_file_path)

def get_input_paths():
    submit_input_files = input("Do you want to submit the input files? (Y/N): ").lower()
    
    if submit_input_files == "y":
        desktop = os.path.expanduser("~/Desktop")
        input_file_path = os.path.join(desktop, "input.txt")
    else:
        raise FileNotFoundError("Input file not specified by the user")

    submit_output_files = input("Do you want to submit the output files? (Y/N): ").lower()
    
    if submit_output_files == "y":
        input_file = os.path.join(os.path.expanduser("~"), "C:\Users\Jon\Desktop\linkbypasser\LinkScraper", "input.txt")
        output_file = os.path.join(os.path.expanduser("~"), "C:\Users\Jon\Desktop\linkbypasser\LinkScraper", "output.txt")
    else:
        raise FileNotFoundError("Output file not specified by the user")

    cleaned_data_file_path = os.path.join(os.path.expanduser("~"), "C:\Users\Jon\Desktop\linkbypasser\LinkScraper", "cleaned_data.txt")

    return input_file_path, output_file, cleaned_data_file_path

def read_and_process_input(input_file_path):
    with open(input_file_path, 'r') as input_file:
        data = input_file.read()

    entries = re.split('\n\n+', data.strip())
    pattern = r'^(.+?):\s+(https?://\S+)'
    return re.findall(pattern, data, flags=re.MULTILINE)

def initialize_web_scraping():
    profile_path = r'C:\Users\Jonathan Bolton\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default'
    brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
    
    chrome_options = Options()
    chrome_options.binary_location = brave_path
    chrome_options.add_argument('--user-data-dir=' + profile_path)

    driver_path = r'C:\Users\Jonathan Bolton\Desktop\chromedriver.exe'
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_and_save_links(driver, entries):
    # Create or open the mega_files.txt file on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    filename = os.path.join(desktop_path, 'mega_files.txt')

    try:
        with open(filename, 'a') as mega_file:
            for name, url in entries:
                try:
                    # Scrape the mega.nz links from the webpage
                    links = scrape_links(driver, url)

                    # Print the links to check if the scraping process is working
                    logger.info(f"{name}")
                    for link in links:
                        logger.info(link)

                    # Write the links to the mega_files.txt file
                    for link in links:
                        mega_file.write(f"{name}: {link}\n")

                    # Wait for 3 seconds before scraping the next webpage
                    time.sleep(3)
                except Exception as e:
                    logger.error(f"An error occurred while scraping {url}: {e}")

        logger.info(f"Links have been written to {filename}")
    except Exception as e:
        logger.error(f"An error occurred while opening or writing to {filename}: {e}")

def scrape_links(driver, url):
    # Navigate to the webpage
    driver.get(url)

    # Wait for 3 seconds before scraping the webpage content
    time.sleep(3)

    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the elements that contain the information you want to scrape
    # For example, to scrape all the links on the webpage that contain "mega.nz":
    links = soup.find_all('a', href=lambda href: href and 'mega.nz' in href)

    # Extract the href attributes from the links and return them as a list
    return [link.get('href') for link in links]

def clean_data():
    # Read the output data
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    output_file_path = os.path.join(desktop_path, 'output.txt')

    with open(output_file_path, "r") as f:
        output_data = f.read()

    cleaned_data_str = ""
    for line in output_data.strip().split('\n'):
        name, link = line.strip().split(': ')
        name = name.strip().title()
        link = link.strip()
        cleaned_data_str += f"{name}: {link}\n"

    return cleaned_data_str

def save_cleaned_data(cleaned_data_str, cleaned_data_file_path):
    with open(cleaned_data_file_path, 'w') as f:
        f.write(cleaned_data_str)

if __name__ == "__main__":
    main()
