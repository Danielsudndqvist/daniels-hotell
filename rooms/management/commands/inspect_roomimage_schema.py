from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Inspect RoomImage table schema'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            try:
                # PostgreSQL specific query to get column information
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'rooms_roomimage';
                """)
                columns = cursor.fetchall()
                
                self.stdout.write(self.style.SUCCESS('Columns in rooms_roomimage:'))
                for column in columns:
                    self.stdout.write(f"{column[0]}: {column[1]}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
