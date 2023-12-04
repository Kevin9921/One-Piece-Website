from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import unidecode as uc

def get_characterData():
    url = "https://onepiece.fandom.com/wiki/List_of_Canon_Characters"
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
   
    table = soup.find_all('table')[0]

    column_data = table.find_all('tr')
    #print(column_data)
    urlList = []
    list = []
    index = 0
    for row in column_data:
        row_data = row.find_all('td')
        url_element = row_data[1].find('a') if row_data and len(row_data) > 1 else None
        url = url_element['href'] if url_element else None
        urlList.append(url)
        cell = [data.text.strip() for data in row_data]
        #print(cell)
        cell.append(url)
        # if url:
        #     list.insert(index, url)
        # index = index + 1
        list.append(cell)
        
    list = list[1:]
    # print(urlList[0])
    # print(urlList[1]+list[1])
    # print(urlList[2])
    # list[0].append(urlList[1])
    # print(list[0])
    # print(list[1])
    # print(list[2])
    return list

def onlyCanon(listName):
    #print(listName[1])
    charNames = []
    dataBook =["SBS", "Blue databook", "Blue Deep databook", "Vivre Card", "Green databook", "Yellow databook", "Grand Ship Collection", " One Piece novel A", "Mentioned only character", "One Piece Magazine"]
    for i in listName:
        # print(i[6])
        databookFlag = False
        for text in dataBook:
            if text in i[5]:
                databookFlag = True
        if databookFlag == False:
            charNames.append([i[1], i[6]])   
    return charNames

def formateName(listName):
    charNames = []
    lastName = ["Charlotte ", "Vinsmoke ","Kozuki " , "Donquixote ", ".", "-","Charlotte ", "Monkey D. ", "Kurozumi ", "Shimotsuki ", "Portgas D. ", "Nefertari ", "Nefertari D. "]
    for i in listName:
        wordTemp = i[0]
        for name in lastName:
            if name in i[0]:
                wordTemp = i[0].replace(name,'') 
        wordTemp = uc.unidecode(wordTemp)
        charNames.append([wordTemp, i[1]])        
    return charNames

def UrlName(listName,formattedNames):
    url = "https://onepiece.fandom.com/wiki/"
    mergedList = []
    for i,e in enumerate(listName):
        wordTemp = e.replace(' ','_') 
        mergedList.append([url+wordTemp, formattedNames[i]])
    return mergedList

def saveImage(charLinks):
    url = "https://onepiece.fandom.com"
    # Create a directory to store images
    os.makedirs('character_images', exist_ok=True)

    for i in charLinks:
        image_path = os.path.join('character_images', f"{i[0]}.jpg")
        if not os.path.exists(image_path):
            try:
                page_to_scrape = requests.get(url + i[1])
                page_to_scrape.raise_for_status()  # Raise an HTTPError for bad responses
            except requests.exceptions.RequestException as e:
                print(f"Error accessing the page: {e}")
                continue

            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            img = soup.find_all(class_="image image-thumbnail")

            links = []
            if img:
                image_url = img[0].get('href')
                if image_url:
                    response = requests.get(image_url).content
                    with open(image_path, 'wb') as img_file:
                        img_file.write(response)
                    print(f"Downloaded image for ", f"{i[0]}")
                else:
                    print(f"No image found for ", f"{i[0]}")
            else:
                print("No elements found with class 'pi-item pi-image'")

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
#gets the data from the website
charData = get_characterData()
#print(len(charData))
# for i in charData:
#     if not len(i) == 7:
#         print(i)


#excludes non canon characters
canonNames = onlyCanon(charData)
#print(canonNames)

#reformats the names
formatedNames = formateName(canonNames)
#print(formatedNames)

#Creates a list of names and urls
#urlList = UrlName(canonNames, formatedNames)
#print(urlList)

#Uncomment to save images
#saveImage(formatedNames)

#uncomment below to add to database
#connection = create_db_connection("localhost", "root", "root", "one Piece") # Connect to the Database
#execute_query(connection, create_teacher_table) # Execute our defined query



#count = 1
# for characters in temp:
#     insert_varibles_into_table(connection, count, characters)
#     count = count + 1
# print("data added to table")