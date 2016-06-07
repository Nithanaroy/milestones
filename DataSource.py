import mysql.connector
import os
from mysql.connector.errors import InterfaceError


class MySQL:
    def __init__(self):
        pass

    @staticmethod
    def insert(table, columns):
        """
        MySQL insert command
        Ref: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
        :param table: name of relational table
        :param columns: list of columns
        :return: SQL insert command string
        """
        values = ','.join(map(lambda x: '%({})s'.format(x), columns))
        return """
            INSERT INTO {}
            ({})
            VALUES ({})
        """.format(table, ','.join(columns), values)

    @staticmethod
    def update(table, columns_to_update, condition_columns, condition_operators, condition_types=[]):
        """
        MySQL update command
        Ref: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
        :param table: name of the relational table
        :param columns_to_update: list of columns to update
        :param condition_columns: list of columns in-order to appear in the WHERE clause
        :param condition_operators: list of operators (=, <=, >=, <, >, <>) joining condition columns and values
        :param condition_types: list of combiners joining conditions (AND, OR)
        :return: update SQL string
        """
        values = map(lambda x: '{}=%({})s'.format(x, x), columns_to_update)
        conditions_and_types = MySQL._create_conditions(condition_columns, condition_types, condition_operators)
        return """
            UPDATE {}
            SET {}
            WHERE {}
        """.format(table, ','.join(values), ' '.join(conditions_and_types))

    @staticmethod
    def select(table, columns, operators, condition_types=[]):
        """
        MySQL select command
        :param table: source table on which SELECT has to be executed
        :param columns: list of columns in-order participating in WHERE condition
        :param operators: list of operators joining the columns and values
        :param condition_types: list of 'AND' or 'OR' terms
        :return: Returns entire tuples which match the selection criteria
        """
        conditions_and_types = MySQL._create_conditions(columns, condition_types, operators)
        return """
        SELECT *
        FROM {}
        WHERE {}
        """.format(table, ' '.join(conditions_and_types))

    @staticmethod
    def _create_conditions(columns, condition_types, operators):
        if len(columns) is not len(operators) is not len(condition_types) - 1:
            raise ValueError("Number of conditions, values and conditions do not match")
        conditions = ["{} {} %({})s".format(columns[i], op, columns[i]) for i, op in enumerate(operators)]
        if len(condition_types) > 0:
            conditions_and_types = [None] * (2 * len(conditions) - 1)
            conditions_and_types[::2] = conditions
            conditions_and_types[1::2] = condition_types
        else:
            conditions_and_types = conditions
        return conditions_and_types

    @staticmethod
    def execute(query, params, database="milestones"):
        con = None
        try:
            con = MySQL.get_connection(database)
            c = con.cursor()
            c.execute(query, params)
            con.commit()
            return {'rows': c.fetchall(), 'columns': c.column_names}
        except InterfaceError:
            pass  # happens when query is an INSERT query and no rows are returned
        finally:
            if con: con.close(); c.close();

    @staticmethod
    def get_connection(database='milestones'):
        """
        Returns an open Database connection
        Set db_username, db_password and db_name environment variables if defaults are not good
        :param database: database name to connect to
        :return: open MySQL connection
        """
        # TODO: Do not use root to connect by default
        host = os.environ['DB_HOSTNAME'] if 'DB_HOSTNAME' in os.environ else '127.0.0.1'
        user = os.environ['DB_USERNAME'] if 'DB_USERNAME' in os.environ else 'root'
        password = os.environ['DB_PASSWORD'] if 'DB_PASSWORD' in os.environ else 'root'
        connection = mysql.connector.connect(user=user, password=password, database=database, host=host)
        connection.sql_mode = ''  # Disable strict mode
        return connection
