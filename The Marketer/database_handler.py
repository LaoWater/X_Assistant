import pandas as pd
import sqlite3


def process_data_to_db(current_market_df, dealer_presets_path='Dealer_Presets.xlsx'):
    # Connect to SQLite database
    conn = sqlite3.connect('market_data.db')

    # Process current market data
    # Rename the relevant columns
    current_market_df.rename(columns={
        'Item Name': 'Item',
        'Gem 1': 'Gem1',
        'Gem 2': 'Gem2'
    }, inplace=True)
    # Create or replace the Current_Market table
    current_market_df.to_sql('Current_Market', conn, if_exists='replace', index=False)

    # Read Dealer Presets data
    df_dealer_presets = pd.read_excel(dealer_presets_path)
    # Create or replace the Dealer_Presets table
    df_dealer_presets.to_sql('Dealer_Presets', conn, if_exists='replace', index=False)

    # SQL Query to join and filter data
    join_query = '''
        SELECT Current_Market.*
        FROM Current_Market
        JOIN Dealer_Presets ON
            COALESCE(Current_Market.Item, '') = COALESCE(Dealer_Presets.Item, '') AND
            COALESCE(Current_Market.Quality, '') = COALESCE(Dealer_Presets.Quality, '') AND
            COALESCE(Current_Market.Plus, '') = COALESCE(Dealer_Presets.Plus, '') AND
            COALESCE(Current_Market.Gem1, '') = COALESCE(Dealer_Presets.Gem1, '') AND
            COALESCE(Current_Market.Gem2, '') = COALESCE(Dealer_Presets.Gem2, '')
        WHERE Current_Market.Price <= Dealer_Presets.Price1
    '''

    # Execute the query and fetch results
    result = pd.read_sql_query(join_query, conn)
    conn.close()
    return result
