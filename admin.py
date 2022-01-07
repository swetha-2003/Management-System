import mysql.connector

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='flask',
                                         user='root',
                                         password='')

    sql_select_Query = "select * from paperpresentation"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)


except mysql.connector.Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")