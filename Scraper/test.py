import requests
from bs4 import BeautifulSoup
import os

url = "https://onepiece.fandom.com/wiki/"
url2 = url + "Attach"

try:
    page_to_scrape = requests.get(url2)
    page_to_scrape.raise_for_status()  # Raise an HTTPError for bad responses
except requests.exceptions.RequestException as e:
    print(f"Error accessing the page: {e}")
    exit()

soup = BeautifulSoup(page_to_scrape.text, "html.parser")
table = soup.find_all(class_="image image-thumbnail")

links = []
if table:
    #print(table)
    # for a in table:
    #     links.append(a['href'])
    # print(links[0])
    image_url = table[0].get('href')

    # Create a directory to store images
    os.makedirs('character_images', exist_ok=True)

    if image_url:
        response = requests.get(image_url).content
        image_path = os.path.join('character_images', "yu.png")
        with open(image_path, 'wb') as img_file:
            img_file.write(response)

        print(f"Downloaded image for ")
    else:
        print(f"No image found for ")

else:
    print("No elements found with class 'pi-item pi-image'")