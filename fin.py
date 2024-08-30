from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# Function to build the URL
def build_url(source, destination, departure_date, return_date):
    url2 = f"https://www.ixigo.com/search/result/flight?from={source}&to={destination}&date={departure_date}&adults=1&children=0&infants=0&class=e"
    return url2

# Function to fetch the flight details , 
def fetch_flight_details(url):
 
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=chrome_options) 
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)  # Wait for the page to load (adjust as needed)

    # Fetch all elements
    airline_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'body-md text-primary truncate max-w-[125px] airlineTruncate font-medium')]")
    pricing_elements = driver.find_elements(By.XPATH, "//h5[@data-testid='pricing' and contains(@class, 'h5 text-primary font-bold')]")
    duration_elements = driver.find_elements(By.XPATH, "//div[@class='flex items-center w-[110px] justify-center']//p[@class='body-xs text-secondary']")
    
    # Lists to store fetched data
    pricing_list = []
    airline_list = []
    duration_list = []

    for element in pricing_elements:
        pricing_list.append(element.text)
    
    for element in airline_elements:
        airline_list.append(element.text)

    for i in range(0, len(duration_elements), 2):
        duration_info = duration_elements[i].text +" "+ duration_elements[i + 1].text
        duration_list.append(duration_info)
    driver.quit()
    return {
        "pricing": pricing_list,
        "airlines": airline_list,
        "durations": duration_list
    }

# Flask route to fetch and return flight details
@app.route('/get-flight-details', methods=['GET'])
def get_flight_details():
    source = request.args.get('source', default='BLR')  # Default to 'BLR' if not provided
    destination = request.args.get('destination', default='DEL')  # Default to 'DEL' if not provided
    departure_date = request.args.get('departure_date', default='03092024')  # Default to '20240903'
    return_date = request.args.get('return_date', default='04092024')  # Default to '20240904'
    
    
    url = build_url(source, destination, departure_date, return_date)
    flight_details = fetch_flight_details(url)
    # http://localhost:5000/get-flight-details?source=BLR&destination=DEL&departure_date=09092024

    return jsonify(flight_details)

# -----------------------------------------hotel---------------------------------------------------
# 
# Function to build the URL for hotel search (modify based on actual URL)
def build_hotel_url(location, checkin_date, checkout_date):
    # Example URL structure; replace it with the actual URL structure
    # url = f"https://www.ixigo.com/hotels/search?location={location}&checkin={checkin_date}&checkout={checkout_date}"
    url2 = f"https://www.ixigo.com/hotels/search/result?locationName={location}&locationType=S&checkinDate={checkin_date}&adultCount=2&roomCount=1&childCount=0&ab="
    return url2

# Function to fetch hotel details
def fetch_hotel_details(url):
  
    driver = webdriver.Chrome() 
    driver.get(url)
    time.sleep(10)  # Wait for the page to load (adjust as needed)

    # Fetch hotel names and their associated prices and images
    hotel_elements = driver.find_elements(By.XPATH, "//h3[@data-testid='hotel-name' and contains(@class, 'h6 truncate font-medium text-primary')]")
    price_elements = driver.find_elements(By.XPATH, "//h5[contains(@class, 'h5 text-right text-primary font-medium')]")
    image_elements = driver.find_elements(By.XPATH, "//img[@loading='lazy' and @style='object-fit: cover; height: 200px;']")
    
    hotel_data = []

    for i in range(min(len(hotel_elements), len(price_elements), len(image_elements))):
        hotel_name = hotel_elements[i].text
        hotel_price = price_elements[i].text
        hotel_image = image_elements[i].get_attribute('src')
        
        hotel_data.append({
            "hotel_name": hotel_name,
            "hotel_price": hotel_price,
            "hotel_image": hotel_image
        })

    driver.quit()

    return hotel_data

# Flask route to fetch and return hotel details
@app.route('/get-hotel-details', methods=['GET'])
def get_hotel_details():
    # Extract query parameters
    location = request.args.get('location',default='BLR')
    checkin_date = request.args.get('checkin_date', default='03092024')
    checkout_date = request.args.get('checkout_date', default='04092024')
    
    if not all([location, checkin_date, checkout_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    url = build_hotel_url(location, checkin_date, checkout_date)
    hotel_details = fetch_hotel_details(url)
    # https://www.ixigo.com/hotels/search/result?locationName=goa&locationType=S&checkinDate=03092024&adultCount=2&roomCount=1&childCount=0&ab=
    return jsonify(hotel_details)

if __name__ == '__main__':
    app.run(debug=True)
