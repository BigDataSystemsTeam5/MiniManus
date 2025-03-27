import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define the URL to scrape
url = "https://investor.nvidia.com/financial-info/quarterly-results/default.aspx"


download_folder = "downloaded_pdfs"
# Create download directory
os.makedirs(download_folder, exist_ok=True)


# Set up headless Chrome
options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled") 

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the page
url = "https://investor.nvidia.com/financial-info/quarterly-results/"
driver.get(url)

# Get page source and parse it
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()


print(soup)
