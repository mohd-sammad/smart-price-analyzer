# 🛒 Smart Price Analyzer

A Streamlit web application that helps users compare product prices across different online stores (DMart, Jiomart, and BigBasket) to find the best deals.

## ✨ Features

- **💰 Price Scraping**: Automatically extracts prices from product pages using Selenium and regex pattern matching
- **💾 Price Storage**: Saves price data in a SQLite database for historical comparison
- **📊 Price Comparison**: Identifies the store offering the lowest price for a product
- **🖥️ User-Friendly Interface**: Simple Streamlit interface for entering product information and viewing results


## 🚀 Installation

1. Clone this repository:
   ```
   git clone https://github.com/mohd-sammad/smart-price-analyzer.git
   cd smart-price-analyzer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Chrome browser and ChromeDriver:
   - The application uses Chrome for web scraping
   - Ensure ChromeDriver is compatible with your Chrome browser version

## 📝 Usage

1. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Enter product details in the web interface:
   - Product name
   - DMart product URL
   - Jiomart product URL
   - BigBasket product URL

3. Click "Fetch Prices" to scrape and compare current prices ⏱️
4. Click "Retrieve Prices" to view previously saved prices from the database 📅

## ⚙️ How It Works

1. The application uses Selenium WebDriver to load product pages from various e-commerce websites 🌐
2. It extracts price information using regex pattern matching (optimized for Indian Rupee format: ₹) 🔍
3. Prices are stored in a SQLite database along with timestamps 🗄️
4. The application highlights the store offering the lowest price 🏷️

## ⚠️ Limitations

- The current regex pattern is optimized for Indian Rupee (₹) format
- Price extraction relies on pattern matching that may need adjustment if store websites change their format
- The application requires an active internet connection and Chrome browser

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
