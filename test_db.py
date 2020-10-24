import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    user="root",
    passwd="password",
    host="localhost",
    database="testdatabase"
)

class NewModel():
    """
    docstring
    """
    def __init__(self, **kwargs):
        """
        docstring
        """
        self.cursor = db.cursor()

        self.class_name = self.__class__.__name__
        self.select = "SELECT * FROM "

        self.create = "CREATE TABLE "

        self.table_content = ()
        self.key_type = ''

        for key in kwargs:
            if type(kwargs[key]) == str:
                self.key_type = "VARCHAR(100)"
            if type(kwargs[key]) == int:
                self.key_type = "int"

            self.table_content = (key + ' ' + self.key_type)
        try: #If TABLE exists
            self.cursor.execute(self.select + self.class_name)
            for x in self.cursor:
                print(x)
        except: #If not create it
            print("Creating class " + self.class_name)
            self.cursor.execute(self.create + self.class_name + " (id int PRIMARY KEY AUTO_INCREMENT)")


# mycursor = db.cursor()
# user = Person(name=('VARCHAR', ), age=25)
user = NewModel(name = 'Person', age = 18)
# mycursor.execute("CREATE TABLE Test (name VARCHAR(50) NOT NULL, created datetime NOT NULL, gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY AUTO_INCREMENT)")

# mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", user.get())
# db.commit()
# mycursor.execute("SELECT * FROM Unknown")

# for x in mycursor:
#     print(x)
