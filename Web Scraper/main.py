import csv
import os
import re
import time

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Prompt the user to submit the input files
submit_input_files = input("Do you want to submit the input files? (Y/N): ")

if submit_input_files.lower() == "y":
    # Define the path to the input file
    desktop = os.path.expanduser("~/Desktop")
    input_file_path = os.path.join(desktop, "input.txt")
else:
    print("System closed " + FileNotFoundError)
    

    # Read the input data from the file
    with open(input_file_path, 'r') as input_file:
        data = input_file.read()

    # Split the data into individual entries
    entries = re.split('\n\n+', data.strip())

    # Define a regex pattern to extract the name and URL from each entry
    pattern = r'^(.+?):\s+(https?://\S+)'



# Rest of the code...

# -------------------------------------

# Prompt the user to submit the output files
submit_output_files = input("Do you want to submit the output files? (Y/N): ")

if submit_output_files.lower() == "y":
    input_file = os.path.join(os.path.expanduser("~"), "C:/Desktop/linkbypasser", "input.txt")
    output_file = os.path.join(os.path.expanduser("~"), "C:/Desktop/linkbypasser", "output.txt")

else: print(FileExistsError)

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        data = f_in.read()
        pattern = r"^(.+):\s*(https?://\S+)\s*$"
        for match in re.findall(pattern, data, flags=re.MULTILINE):
            name, link = match
            f_out.write(f"{name}: {link}\n")

# -------------------------------------

# Read the output data
with open(os.path.join(os.path.expanduser("~"), "C:/Desktop/linkbypasser", "output.txt"), "r") as f:
    output_data = f.read()

# Convert the output data into a string
cleaned_data_str = ""
for line in output_data.strip().split('\n'):
    name, link = line.strip().split(': ')
    name = name.strip().title()
    link = link.strip()
    cleaned_data_str += f"{name}: {link}\n"

# Write the cleaned data into a text file on the desktop
with open(os.path.join(os.path.expanduser("~"), "C:/Desktop/linkbypasser", "cleaned_data.txt"), 'w') as f:
    f.write.__new__(cleaned_data_str)


# Path to your Brave browser profile directory
profile_path = r'C:\Users\Jonathan Bolton\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default'

# Path to the Brave browser executable file
brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

# Create a ChromeOptions object to specify the profile directory and the location of the Brave executable
chrome_options = Options()
chrome_options.binary_location = brave_path
chrome_options.add_argument('--user-data-dir=' + profile_path)

# Path to the Chrome driver executable
driver_path = r'C:\Users\Jonathan Bolton\Desktop\chromedriver.exe'

# Function to scrape mega.nz links from a webpage
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

# Open the cleaned_data.txt file on the desktop and read the name-link pairs into a dictionary
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
filename = os.path.join(desktop_path, 'cleaned_data.txt')
models = {}
with open(filename, 'r') as f:
    for line in f:
        name, link = line.strip().split(': ')
        models[name] = link

# Create a new Chrome session with the specified profile, driver path, and options
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create or open the mega_files.txt file on the desktop
filename = os.path.join(desktop_path, 'mega_files.txt')

try:
    mega_file = open(filename, 'a')

    # Loop through the models and scrape their links
    for name, url in models.items():
        try:
            # Scrape the mega.nz links from the webpage
            links = scrape_links(driver, url)

            # Print the links to check if the scraping process is working
            print(f"{name}")
            for link in links:
                print(link)

            # Write the links to the mega_files.txt file
            for link in links:
                mega_file.write(f"{name}: {link}\n")

            # Wait for 3 seconds before scraping the next webpage
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred while scraping {url}: {e}")

    print(f"Links have been written to {filename}")
except Exception as e:
    print(f"An error occurred while opening or writing to {filename}: {e}")
finally:
    # Close the file and the Chrome session
    mega_file.close()
    driver.quit()
    # Read the content from mega_files.txt

# Read the links from mega_files.txt
with open(os.path.join(desktop_path, 'mega_files.txt'), 'r') as f:
    links = f.readlines()

# Remove duplicates
unique_links = list(set(links))

# Sort the links alphabetically
sorted_links = sorted(unique_links)

# Write the sorted links to a new file
output_file_path = os.path.join(desktop_path, 'mega_files.txt')
with open(output_file_path, 'w') as f:
    f.writelines(sorted_links)

print(f" Links have been written to {output_file_path}.")
