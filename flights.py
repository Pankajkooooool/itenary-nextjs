from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to build the URL
def build_url(source, destination, departure_date, return_date):
    
    url2 = f"https://www.ixigo.com/search/result/flight?from={source}&to={destination}&date={departure_date}&adults=1&children=0&infants=0&class=e"
    return url2

# Function to open the browser and navigate to the URL
def open_browser(url, browser_choice='chrome'):
    if browser_choice == 'chrome':
        driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    elif browser_choice == 'firefox':
        driver = webdriver.Firefox()  # Ensure geckodriver is in PATH
    else:
        print("Unsupported browser choice. Use 'chrome' or 'firefox'.")
        return

    driver.get(url)
    time.sleep(5)  # Wait for the page to load (adjust as needed)
       # Fetch all elements with the specified tag and class
    airline_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'body-md text-primary truncate max-w-[125px] airlineTruncate font-medium')]")
    pricing_elements = driver.find_elements(By.XPATH, "//h5[@data-testid='pricing' and contains(@class, 'h5 text-primary font-bold')]")
      # Fetch all duration and stop elements
    duration_elements = driver.find_elements(By.XPATH, "//div[@class='flex items-center w-[110px] justify-center']//p[@class='body-xs text-secondary']")
    
    # Lists to store fetched data
    pricing_list = []
    airline_list = []
    duration_list = []
    for element in pricing_elements:
        pricing_list.append(element.text)
    
    # Store the text of each airline element found
    for element in airline_elements:
        airline_list.append(element.text)
    
    # Store the text of each duration and stop element found
    for i in range(0, len(duration_elements), 2):
        duration_info = duration_elements[i].text + " " + duration_elements[i + 1].text
        duration_list.append(duration_info)

    # Print the stored lists
    print("Pricing Details:", pricing_list)
    print("Airline Names:", airline_list)
    print("Duration and Stop Information:", duration_list)
    driver.quit()

# Main script execution
if __name__ == "__main__":
    # Use the given details
    source = 'BLR'  # Bangalore
    destination = 'DEL'  # Paris
    departure_date = '03092024'  # September 3, 2024
    return_date = '04092024'  # September 4, 2024
    
    url = build_url(source, destination, departure_date, return_date,)
    
    
    open_browser(url, browser_choice='chrome')
