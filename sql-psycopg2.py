
import psycopg2


connection = psycopg2.connect(database="chinook")

# Example Queries for your tables:

# Query 1 - select all records from the "CustomUser" table
cursor.execute('SELECT * FROM "CustomUser"')

# Query 2 - select all profiles and their associated users
cursor.execute('SELECT * FROM "Profile" INNER JOIN "CustomUser" ON "Profile"."user_id" = "CustomUser"."id"')

# Query 3 - select all rooms that are available
cursor.execute('SELECT * FROM "Room" WHERE "available" = TRUE')

# Query 4 - select all bookings with a "confirmed" status
cursor.execute('SELECT * FROM "Booking" WHERE "status" = %s', ['confirmed'])

# Fetch the results
results = cursor.fetchall()

# Close the connection
connection.close()

# Print the results
for result in results:
    print(result)


