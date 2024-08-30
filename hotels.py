from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# Function to build the URL for hotel search (modify based on actual URL)
def build_hotel_url(location, checkin_date, checkout_date):
    # Example URL structure; replace it with the actual URL structure
    url = f"https://www.ixigo.com/hotels/search?location={location}&checkin={checkin_date}&checkout={checkout_date}"
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
@app.route('/ge', methods=['GET'])
def get_hotel_details():
    # Extract query parameters
    location = request.args.get('location',default='BLR')
    checkin_date = request.args.get('checkin_date', default='03092024')
    checkout_date = request.args.get('checkout_date', default='04092024')
    
    if not all([location, checkin_date, checkout_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    url = build_hotel_url(location, checkin_date, checkout_date)
    hotel_details = fetch_hotel_details(url)
    
    return jsonify(hotel_details)

if __name__ == '__main__':
    app.run(debug=True)
