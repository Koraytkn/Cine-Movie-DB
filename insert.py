#Standard library import
import mysql.connector

#Connect with the precise info, also with dataset name
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="your_password",
  database="your_schema_name"
)


#Command needed to modify/access inside database(s)
mycursor = mydb.cursor()

#SQL Script in form of string
sql1 = "INSERT INTO your_schema_name.db_manager (username, password) VALUES (%s, %s)"

sql2 = "INSERT INTO your_schema_name.genre (genre_id, genre_name) VALUES (%s, %s)"

sql3 = "INSERT INTO your_schema_name.rating_platform (platform_id, platform_name) VALUES (%s, %s)"


val1 = [
  ('manager1', 'managerpass1'),
  ('manager2', 'managerpass2'),
  ('manager35', 'managerpass35'),
]

val2 = [
  ('80001', 'Animation'),
  ('80002', 'Comedy'),
  ('80003', 'Adventure'),
  ('80004', 'Real Story'),
  ('80005', 'Thriller'),
  ('80006', 'Drama'),
]

val3 = [
  ('10130', 'IMDB'),
  ('10131', 'Letterboxd'),
  ('10132', 'FilmIzle'),
  ('10133', 'Filmora'),
  ('10134', 'BollywoodMDB'),
]


#Execute the SQL Script, notice the seperate parameters, also the "many"
mycursor.executemany(sql1, val1)
mycursor.executemany(sql2, val2)
mycursor.executemany(sql3, val3)

#Apply changes when modifying the inside of a table
mydb.commit()

#Print the changes count
print(mycursor.rowcount, "was inserted.")