from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Paths to ChromeDriver and Chrome binary
chromedriver_path = '/Users/chayma2/chromedriver/mac-125.0.6422.141/chromedriver-mac-x64/chromedriver'
chrome_path = '/Users/chayma2/chrome/mac-125.0.6422.141/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'

# Check if paths exist and are executable
if not (os.path.isfile(chromedriver_path) and os.access(chromedriver_path, os.X_OK)):
    raise FileNotFoundError(f"ChromeDriver not found or not executable at path: {chromedriver_path}")

if not (os.path.isfile(chrome_path) and os.access(chrome_path, os.X_OK)):
    raise FileNotFoundError(f"Chrome binary not found or not executable at path: {chrome_path}")

# Set up Chrome WebDriver with headless options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.binary_location = chrome_path

# Create a Chrome WebDriver instance with the specified options
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


import json
from datetime import datetime, timedelta

# Function to convert the date string to datetime object
def parse_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y")

# Calculate yesterday's date
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime("%d/%m/%Y")


try:
    # URL of the dynamic page
    url = 'https://actulegales.fr/recherche'
    driver.get(url)
# Wait for the search input to be visible
    search_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "main-search-input"))
    )

  
    # Input the search query
    search_input.send_keys("Procedure de sauvegarde")
    search_input.send_keys(Keys.ENTER)

    # Wait for the page to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#center-table-result')))

    # Find all articles using the provided CSS selector
    all_articles = driver.find_elements(By.CSS_SELECTOR, '#center-table-result > div > div.results-items > article')

    # Initialize list to store data for each article
    articles_data = []

    # Loop through each article to extract information
    for article in all_articles:
        title_element = article.find_element(By.CSS_SELECTOR, 'h2.entreprise-title a span[itemprop="name"]')
        title = title_element.text

        siren_element = article.find_element(By.CSS_SELECTOR, 'h2.entreprise-title a')
        siren = siren_element.text.split(':')[1].strip(') ')

        event_element = article.find_element(By.CSS_SELECTOR, 'dl > dd:nth-child(2) > span')
        event = event_element.text

        parution_element = article.find_element(By.CSS_SELECTOR, 'dl > dd:nth-child(4) > span')
        parution = parution_element.text

        date_element = article.find_element(By.CSS_SELECTOR, 'dl > dd:nth-child(6) > span')
        date = parse_date(date_element.text)

        # Check if the article is published yesterday
        if date.date() == yesterday.date():
            # Format the information as a dictionary for each article
            data = {
                "Title": title,
                "Siren": siren,
                "Événement": event,
                "Paru dans": parution,
                "Date": date.strftime("%d/%m/%Y")
            }
            # Append the data to the list
            articles_data.append(data)

    # Convert list of dictionaries to JSON format
    json_data = json.dumps(articles_data, indent=4, ensure_ascii=False)

    # Print the JSON data
    print(json_data)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the driver
    driver.quit()
