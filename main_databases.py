import sqlite3
from pynput.mouse import Listener, Button

# Global flag to enable custom positioning
Custom_Pos = True


# Function to capture mouse clicks and assign to global variables
def custom_map_coordinates():
    # List to store click positions
    clicks = []
    print("Welcome to Custom mapping of Socketeer. \n Please in the exact following way: \nShop, Warehouse, "
          "Artisan Wind and Upgrade button")

    # Define what happens on a mouse click
    def on_click(x, y, button, pressed):
        # Only consider left button down events
        if button == Button.left and pressed:
            clicks.append((x, y))
            # If five clicks have been captured, stop the listener
            if len(clicks) == 4:
                return False

    # Start the listener in its own thread to avoid blocking
    listener = Listener(on_click=on_click)
    listener.start()
    listener.join()  # Wait until the listener stops

    # Check if we captured exactly five clicks
    if len(clicks) == 4:
        save_coord_and_update(conn_main, 'Shop', clicks[0][0], clicks[0][1], 'Custom_1')
        save_coord_and_update(conn_main, 'Warehouse', clicks[1][0], clicks[1][1], 'Custom_1')
        save_coord_and_update(conn_main, 'Artisan_Wind', clicks[2][0], clicks[2][1], 'Custom_1')
        save_coord_and_update(conn_main, 'Upgrade', clicks[3][0], clicks[3][1], 'Custom_1')


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as err:
        print(err)
    return conn


def modify_coordinates_table_to_integers(conn):
    """
    Modify the Coordinates table so Coord_X and Coord_Y hold integer values.
    """
    try:
        # Create a new table with the desired column types
        conn.execute('''CREATE TABLE IF NOT EXISTS Coordinates (
    Coord_Name TEXT,
    Coord_X INTEGER,
    Coord_Y INTEGER,
    Type TEXT,
    PRIMARY KEY (Coord_Name, Type));''')

        # Copy data from the old table to the new table, converting values to integers
        conn.execute('''INSERT INTO Coordinates_new (Coord_Name, Coord_X, Coord_Y)
                        SELECT Coord_Name, CAST(Coord_X AS INTEGER), CAST(Coord_Y AS INTEGER)
                        FROM Coordinates;''')

        # Drop the old table
        conn.execute('''DROP TABLE Coordinates;''')

        # Rename the new table to the original name
        conn.execute('''ALTER TABLE Coordinates_new RENAME TO Coordinates;''')

        conn.commit()
        print("Table 'Coordinates' has been modified to store integers.")
    except sqlite3.Error as er:
        print(er)


def save_coord_and_update(conn, coord_name, coord_x, coord_y, coord_type):
    """
    Save a new coordinate into the Coordinates table
    """
    sql = '''
    INSERT INTO Coordinates (Coord_Name, Coord_X, Coord_Y, Type)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(Coord_Name, Type) DO UPDATE SET
    Coord_X=excluded.Coord_X, Coord_Y=excluded.Coord_Y;
    '''

    cur = conn.cursor()
    cur.execute(sql, (coord_name, coord_x, coord_y, coord_type))
    conn.commit()


def get_coord(coord_name, coord_type='Default'):
    """
    Query coordinates by name
    """
    conn = create_connection(database_name)
    cur = conn.cursor()
    cur.execute("SELECT Coord_X, Coord_Y FROM Coordinates WHERE Coord_Name = ? and Type = ?",
                (coord_name, coord_type))
    result = cur.fetchone()
    return result


def modify_coord(conn, coord_name, coord_x, coord_y, coord_type='Default'):
    """
    Update the coordinates for a given name in the Coordinates table.
    """
    sql = ''' UPDATE Coordinates
              SET Coord_X = ?, Coord_Y = ?
              WHERE Coord_Name = ?
              AND Type = ?;'''
    cur = conn.cursor()
    # Interesting placeholders usage
    cur.execute(sql, (coord_x, coord_y, coord_name, coord_type))
    conn.commit()


def drop_table(conn, table_name):
    """
    Drop the specified table from the database.
    """
    try:
        sql = f'DROP TABLE IF EXISTS {table_name};'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(f"Table '{table_name}' dropped successfully.")
    except sqlite3.Error as err:
        print(f"Error occurred: {err}")


def get_db_connection(db_file):
    conn = sqlite3.connect(db_file)
    try:
        yield conn
    finally:
        conn.close()


def create_table():
    global conn_main
    # Create table if it doesn't exist
    if conn_main is not None:
        create_table_sql = '''
CREATE TABLE Coordinates (
    Coord_Name TEXT NOT NULL,
    Coord_X INTEGER NOT NULL,
    Coord_Y INTEGER NOT NULL,
    Type TEXT NOT NULL,
    PRIMARY KEY (Coord_Name, Type)
                              );'''
        try:
            cur = conn_main.cursor()
            cur.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    # Insert the provided coordinates

    coords = [
        ('Shop', 510, 408, 'Default'),
        ('Warehouse', 319, 305, 'Default'),
        ('First_WH_MS', 241, 388, 'Default'),
        ('Artisan_Wind', 688, 502, 'Default'),
        ('Upgrade', 276, 285, 'Default')
    ]

    for coord_name_main, coord_x_main, coord_y_main, coords_type in coords:
        save_coord_and_update(conn_main, coord_name_main, coord_x_main, coord_y_main, coords_type)


database_name = 'XXXX.db'

# Connect to the SQLite database
conn_main = create_connection(database_name)
c = conn_main.cursor()

# c.execute("Drop table Coordinates")

# Custom mapping NPCs coordinates on new position.
# custom_map_coordinates()

if __name__ == "__main__":
    # Create Table
    create_table()

    c.execute("SELECT * FROM Coordinates")
    rows = c.fetchall()  # Fetch all rows of the query result

    for row in rows:
        print(row)  # Print each row

    # Remember to close the connection to the database when you're done
    conn_main.close()


