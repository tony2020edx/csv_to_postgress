import pandas as pd
import psycopg2

def connect_to_db():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(
        host="localhost",
        database="mydatabase",
        user="myusername",
        password="mypassword"
    )
    return conn

def read_csv_file(filename):
    """Read the CSV file using Pandas."""
    df = pd.read_csv(filename)
    return df

def convert_pandas_types_to_postgresql_types(column_types):
    """Convert Pandas data types to PostgreSQL data types."""
    postgresql_types = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'object': 'TEXT'
    }
    return [postgresql_types[str(x)] for x in column_types]

def create_table(conn, column_names, column_types, table_name):
    """Create a table in the database with the given column names and types."""
    # Construct the CREATE TABLE statement using the extracted information
    columns = [f"{column_names[i]} {column_types[i]}" for i in range(len(column_names))]
    create_table_statement = f"CREATE TABLE {table_name} (\n\t" + ",\n\t".join(columns) + "\n);"
    
    # Execute the CREATE TABLE statement
    with conn.cursor() as cur:
        cur.execute(create_table_statement)
    
    # Commit the transaction
    conn.commit()

def main():
    """Main function to run the program."""
    # Connect to the PostgreSQL database
    conn = connect_to_db()
    
    # Read the CSV file using Pandas
    df = read_csv_file('mycsvfile.csv')
    
    # Extract the column names and data types
    column_names = df.columns.tolist()
    column_types = df.dtypes.tolist()
    
    # Convert Pandas data types to PostgreSQL data types
    column_types = convert_pandas_types_to_postgresql_types(column_types)
    
    # Create the table in the database
    table_name = 'mytable'
    create_table(conn, column_names, column_types, table_name)
    
    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()

