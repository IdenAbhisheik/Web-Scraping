import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# Set ChromeDriver path
driver_path = r"D:\Web Scraping\Web Scraping\car_scraper\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the website
url = "https://www.cars24.com/buy-used-cars-chennai/"
driver.get(url)

# Wait for listings to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "styles_carCardWrapper__sXLIp")))

car_cards = driver.find_elements(By.CLASS_NAME, "styles_carCardWrapper__sXLIp")
print(f"Found {len(car_cards)} car listings")

car_data = []

for card in car_cards:
    try:
        # Title: "2021 Maruti Swift" → Split into Year and Car Model
        title_elem = card.find_element(By.XPATH, ".//span[contains(@class, 'kjFjan')]")
        title_text = title_elem.text.strip()

        if title_text[:4].isdigit():
            year_of_manufacture = title_text[:4]
            car_model = title_text[5:]  # Skip the year and space
        else:
            year_of_manufacture = "N/A"
            car_model = title_text

        # Kilometers Driven, Fuel, Transmission
        specs = card.find_elements(By.XPATH, ".//p[contains(@class, 'kvfdZL')]")
        kilometers = specs[0].text.strip() if len(specs) > 0 else "N/A"
        fuel = specs[1].text.strip() if len(specs) > 1 else "N/A"
        transmission = specs[2].text.strip() if len(specs) > 2 else "N/A"

        # Price
        price_elem = card.find_element(By.XPATH, ".//div[contains(@class, 'styles_price')]")
        price = price_elem.text.strip()

        # Store in required format
        car_data.append({
            "Car Model": car_model,
            "Kilometers Driven": kilometers,
            "Year of Manufacture": year_of_manufacture,
            "Fuel Type": fuel,
            "Transmission": transmission,
            "Price": price
        })

    except Exception as e:
        print(f"Skipped one listing due to error: {e}")
        continue

# Save to CSV
csv_file = "cars24_data_selenium.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=car_data[0].keys())
    writer.writeheader()
    writer.writerows(car_data)

print(f"\nData saved to: {csv_file}")
driver.quit()
