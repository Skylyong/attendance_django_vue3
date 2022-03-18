from django.db import connection

def my_custom_sql(self):
    with connection.cursor() as cursor:
        pass

        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        # cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        # row = cursor.fetchone()

    # return row
