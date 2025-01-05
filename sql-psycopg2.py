import psycopg2
from psycopg2 import Error


def run_database_queries():
    """Execute and display results of various database queries."""
    try:
        # Establish database connection
        connection = psycopg2.connect(database="chinook")
        cursor = connection.cursor()

        # Query 1 - select all records from the "CustomUser" table
        cursor.execute('SELECT * FROM "CustomUser"')
        user_results = cursor.fetchall()
        print("\nCustom Users:")
        for user in user_results:
            print(user)

        # Query 2 - select all profiles and their associated users
        cursor.execute(
            'SELECT * FROM "Profile" '
            'INNER JOIN "CustomUser" ON '
            '"Profile"."user_id" = "CustomUser"."id"'
        )
        profile_results = cursor.fetchall()
        print("\nUser Profiles:")
        for profile in profile_results:
            print(profile)

        # Query 3 - select all rooms that are available
        cursor.execute('SELECT * FROM "Room" WHERE "available" = TRUE')
        room_results = cursor.fetchall()
        print("\nAvailable Rooms:")
        for room in room_results:
            print(room)

        # Query 4 - select all bookings with a "confirmed" status
        cursor.execute(
            'SELECT * FROM "Booking" WHERE "status" = %s',
            ["confirmed"]
        )
        booking_results = cursor.fetchall()
        print("\nConfirmed Bookings:")
        for booking in booking_results:
            print(booking)

    except (Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nDatabase connection is closed")


if __name__ == "__main__":
    run_database_queries()
