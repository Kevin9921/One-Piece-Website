from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
import pandas as pd
import unidecode as uc


url = "https://onepiece.fandom.com/wiki/List_of_Canon_Characters"
page_to_scrape = requests.get(url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
#print(soup)
table = soup.find_all('table')[0]
# charNames = soup.find_all('th')
# charTableTitles = [name.text.strip() for name in charNames]


column_data = table.find_all('tr')
#print(column_data)

list = []
for row in column_data:
    row_data = row.find_all('td')
    cell = [data.text.strip() for data in row_data]
    #print(cell)
    list.append(cell)
list = list[1:]

temp = []
dataBook =["SBS", "Blue databook", "Blue Deep databook", "Vivre Card", "Green databook", "Yellow databook", "Grand Ship Collection", " One Piece novel A", "Mentioned only character"]
lastName = ["Charlotte ", "Vinsmoke ","Kozuki " , "Donquixote ", ".", "-","Charlotte ", "Monkey D. ", "Kurozumi ", "Shimotsuki ", "Portgas D. ", "Nefertari ", "Nefertari D. "]
for i in list:
    databookFlag = False
    for text in dataBook:
        if text in i[5]:
            databookFlag = True
    if databookFlag == False:
        wordTemp = i[1]
        for name in lastName:
            if name in i[1]:
                wordTemp = i[1].replace(name,'') 
            
        
        wordTemp = uc.unidecode(wordTemp)
        #print(wordTemp)
        temp.append(wordTemp)        
#print(temp)
#print(len(temp))
# print(list[0][5])
# for i in list:
#     #print(i[1])
#     temp.append(i[1])
# #print(temp)
# print(len(temp))
'''
#quotes = soup.findAll("span", attrs ={"class": "text"})
#authors = soup.findAll("span", attrs ={"class": "author"})

#<table class="wikitable sortable jquery-tablesorter">
#print(table)



#print(worldTableTieles)

column_data = table.find_all('tr')

list = []
for row in column_data:
    row_data = row.find_all('td')
    cell = [data.text.strip() for data in row_data]
    #print(cell)
    list.append(cell)
list = list[1:]
#print(list)

'''



def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
        #mycursor = connection.cursor()
        #mycursor.execute("CREATE DATABASE companies")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def insert_varibles_into_table(connection, id, name):
    cursor = connection.cursor()
    try:
        mySql_insert_query = """INSERT INTO OnePiece_Characters (character_id, name) 
                                VALUES (%s, %s) """

        record = (id, name)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


create_teacher_table = """
CREATE TABLE OnePiece_Characters (
  character_id INT PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  image_url VARCHAR(255) NOT NULL

  );
 """
add_data_table = """
INSERT INTO products (character_id, name)
VALUES (%d, %s)

"""

connection = create_db_connection("localhost", "root", "root", "one Piece") # Connect to the Database
execute_query(connection, create_teacher_table) # Execute our defined query

#count = 1
# for characters in temp:
#     insert_varibles_into_table(connection, count, characters)
#     count = count + 1
# print("data added to table")