import streamlit as st
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Connect to SQLite Database
conn = sqlite3.connect('price_data.db')
cursor = conn.cursor()

# Create a table to store the prices
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_prices (
        product_name TEXT,
        store_name TEXT,
        price REAL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Function to retrieve price from a store using regex and page source analysis
def get_price_from_store(product_url):
    driver = webdriver.Chrome()

    try:
        driver.get(product_url)

        # Wait until the body is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Get the page source
        page_source = driver.page_source

        # Use regular expressions to find all prices on the page
        price_patterns = re.findall(r'₹\s?[\d,]+(?:\.\d{1,2})?', page_source)

        # Debugging: Print all detected price patterns
        print(f"Detected price patterns: {price_patterns}")

        # Ensure at least one price is found
        if not price_patterns:
            raise ValueError("No price found on the page.")

        # Clean the first detected price by removing currency symbols and commas
        cleaned_price_text = price_patterns[0].replace('₹', '').replace(',', '').strip()

        # Convert cleaned price to float
        price = float(cleaned_price_text)

        return price

    except Exception as e:
        print(f"Error fetching price from {product_url}: {e}")
        raise

    finally:
        driver.quit()

# Save price data to the database, deleting previous entries for the same product and store
def save_price_data(product_name, store_name, price):
    # Delete any existing records for the product from the same store
    cursor.execute('''
        DELETE FROM product_prices WHERE product_name = ? AND store_name = ?
    ''', (product_name, store_name))
    
    # Insert the new price into the database
    cursor.execute('''
        INSERT INTO product_prices (product_name, store_name, price)
        VALUES (?, ?, ?)
    ''', (product_name, store_name, price))
    
    conn.commit()

# Main Streamlit app
st.title("Smart Price Analyzer")

# Input fields for the product name and URLs
product_name = st.text_input("Enter Product Name")
dmart_url = st.text_input("Dmart URL")
jiomart_url = st.text_input("Jiomart URL")
bigbasket_url = st.text_input("BigBasket URL")

# Fetch Prices button
if st.button("Fetch Prices"):
    if product_name:
        store_data = [
            {"store_name": "Dmart", "url": dmart_url},
            {"store_name": "Jiomart", "url": jiomart_url},
            {"store_name": "BigBasket", "url": bigbasket_url}
        ]
        
        prices_fetched = []
        for store in store_data:
            if store['url']:
                try:
                    # Fetch price from the store
                    price = get_price_from_store(store['url'])
                    
                    # Save the fetched price to the database
                    save_price_data(product_name, store['store_name'], price)
                    
                    prices_fetched.append((store['store_name'], price))
                except Exception as e:
                    st.error(f"Error fetching price from {store['store_name']}: {e}")
        
        if prices_fetched:
            st.success("Prices fetched and saved successfully!")
            lowest_price = None
            cheapest_store = None
            for store_name, price in prices_fetched:
                st.write(f"₹{price} from {store_name}")
                
                # Find the lowest price and the corresponding store
                if lowest_price is None or price < lowest_price:
                    lowest_price = price
                    cheapest_store = store_name
            
            # Suggest the store with the lowest price
            if cheapest_store and lowest_price:
                st.markdown(f"""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 10px; background-color: #f9f9f9;">
                    <strong>Great news!</strong> You can get the best value for your money with the lowest price of <strong>₹{lowest_price}</strong> at <strong>{cheapest_store}</strong>. 
                    This store offers a combination of affordability and quality, making it the best choice for your purchase.
                    <br><br><strong>Save time and money by shopping at {cheapest_store} today!</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("No prices were fetched.")
    else:
        st.error("Please enter a product name.")

# Retrieve Prices button
if st.button("Retrieve Prices"):
    if product_name:
        cursor.execute('''
            SELECT store_name, price, last_updated
            FROM product_prices
            WHERE product_name = ?
            ORDER BY last_updated DESC
        ''', (product_name,))
        
        rows = cursor.fetchall()

        if rows:
            st.write(f"Prices for {product_name}:")
            lowest_price = None
            cheapest_store = None
            for row in rows:
                store_name, price, last_updated = row
                st.write(f"Store: {store_name}, Price: ₹{price}, Last Updated: {last_updated}")
                
                # Track the lowest price and store
                if lowest_price is None or price < lowest_price:
                    lowest_price = price
                    cheapest_store = store_name

            # Suggest the store with the lowest price
            if cheapest_store and lowest_price:
                st.markdown(f"""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 10px; background-color: #f9f9f9;">
                    <strong>Congratulations!</strong> The lowest price for <strong>{product_name}</strong> is <strong>₹{lowest_price}</strong> at <strong>{cheapest_store}</strong>. 
                    This store is known for delivering excellent value and quality. 
                    <br><br><strong>Don’t miss out on this opportunity to get the best deal!</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"No prices found for {product_name}.")
    else:
        st.error("Please enter a product name.")

# Close the database connection when done
conn.close()