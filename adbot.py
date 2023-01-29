import csv
import pandas
import json
import os
import requests
from pathvalidate import sanitize_filename

def download_image(url, title):
    headers = {'x-test': 'true'}
    response = requests.get(url, headers=headers)

    # Si on obtient une réponse 404 (page non trouvée)
    if response.status_code == 404:
        # On écrit le titre de l'image dans un fichier log.txt (pour le télécharger manuellement plus tard par exemple).
        with open('log.txt', 'a') as f:
            f.write(f"{title}\n")

    # Sinon, on récupère les informations de l'image au format json
    else:
        data_json = response.json()

        # On extrait la version de l'image avec la plus grande résolution possible.
        new_size = max((size['width'], size['height']) for size in data_json['sizes'])
        new_img_url = url.replace('200,200', f"{new_size[0]},{new_size[1]}")
        image_path = os.path.join("downloadedImages/", f"{sanitize_filename(title)}.jpg")

        with open(image_path, 'wb') as f:
            f.write(requests.get(new_img_url).content)

def art_downloader(img_ids, img_titles, start_index):
    published = "published_images.csv"

    with open(published, 'rt', encoding="utf8") as f:
        data = csv.reader(f)

        # On ignore la première (en-tête) ligne du fichier car elle contient les clés.
        next(data)

        for row in data:
            url = row[1]
            title = row[10]
            download_image(url, title)
            print(f"Artwork number {start_index} done.")
            start_index += 1

objects = "objects_text_entries.csv"
images_ids = []
images_titles = []

with open(objects, 'rt', encoding="utf8") as o:
    data = csv.reader(o)

    # On ignore la première ligne (en-tête) du fichier car elle contient les clés.
    next(data)

    for row in data:
        images_ids.append(int(row[0]))
        images_titles.append(row[1])

# On demande à l'utilisateur de saisir l'index de départ pour le téléchargement.
try:
    start_idx = int(input("Entrez l'index de départ à partir de laquelle vous souhaitez commencer le téléchargement: "))
except ValueError:
    print("Entrée non valide, veuillez entrer un nombre entier.")
    start_idx = int(input("Entrez l'index de départ à partir de laquelle vous souhaitez commencer le téléchargement: "))

art_downloader(images_ids, images_titles, start_idx)