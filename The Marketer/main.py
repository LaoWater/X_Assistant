import time
from web_scraper import scrape_market_data
from database_handler import process_data_to_db


def slow_print(df):
    # Convert DataFrame to a string for slow printing
    result_str = df.to_string()
    for line in result_str.split('\n'):
        print(line)
        time.sleep(0.1)  # Adjust the time as needed for the desired speed


def main():
    # User input for selecting the server
    print("Hello, my friend.")
    print("Welcome to the Marketer!")
    choice = input("Enter your choice: ")

    if choice == '1':
        desired_server = "US"
    elif choice == '2':
        desired_server = "EU"
    else:
        print("Invalid choice. Exiting.")
        return

    print("Scrapping.... prepare your money")
    time.sleep(2)
    # Scrape market data for the chosen server
    current_market_df = scrape_market_data(desired_server)
    if current_market_df is not None:
        print("Loading results into Database...\n")
        result = process_data_to_db(current_market_df)
        print("Analyzing Results...")
        time.sleep(1.5)
        print("All items found based on your Dealer_Presets:")
        slow_print(result)
    else:
        print("Failed to scrape market data.")

    print("\nGood Luck Dealing!")


if __name__ == "__main__":
    main()
