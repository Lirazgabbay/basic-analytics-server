"""
    A class to manage database operations.
"""
from db import DB

class TableMethods:
    '''
        Contains a TableMethods class for higher-level operations,
        like creating tables and processing events, using the DB class
    '''
    def __init__(self, db: DB):
        self.db = db

    def create_table(self, table_name: str, columns: dict):
        """
        Create a table in the database.

        Args:
            table_name (str): The name of the table to create.
            columns (dict): A dictionary of column names and their SQL data types.
        """
        try:
            # Build the column definitions from the provided dictionary
            column_definitions = ", ".join(f"{column_name} {data_type}" for column_name, data_type in columns.items())

            table_schema = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {column_definitions}
            );
            """

            self.db.execute(table_schema)
            self.db.commit()

            print(f"Table '{table_name}' created successfully.")

        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            self.db.rollback()  # Rollback to maintain database integrity


    def insert_to_table(self, table_name: str, columns: dict):
        """
        Insert a row into a table in the database.

        Args:
            table_name (str): The name of the table to insert into.
            columns (dict): A dictionary of column names and their values to insert into the table for the row.
        """
        try:
            # Build the column names and placeholders for the query
            column_names = ", ".join(columns.keys())
            value_placeholders = ", ".join("?" for _ in columns)

            insert_query = f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({value_placeholders});
            """

            self.db.execute(insert_query, tuple(list(columns.values())))
            self.db.commit()

            print(f"Data inserted into table '{table_name}' successfully.")

        except Exception as e:
            print(f"Error inserting data into table '{table_name}': {e}")
            self.db.rollback()  # Rollback to maintain database integrity
  
