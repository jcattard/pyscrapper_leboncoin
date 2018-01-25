# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import argparse
from common import DEFAULT_CATEGORIES, DEFAULT_LOCALISATIONS, DEFAULT_TYPES

def browse(url, categories):
    category = url.split('/')[3]
    if category not in categories:
        raise Exception("Wrong URL: category '%s' does not exist" % category)
    model = categories[category]

    page = urlopen(url)
    data = BeautifulSoup(page.read(), "html.parser")
    items = data.find('section', class_="tabsContent block-white dontSwitch")
    if items:
        for link in items.findAll('a'):
            item_url = "http:"+link.get('href')
            item_page = urlopen(item_url)
            item_data = BeautifulSoup(item_page.read(), "html.parser")
            obj = model(item_url, item_data)
            yield obj
    else:
        print("Pas d'annonce")


if __name__ == '__main__':
    # parse inputs
    parser = argparse.ArgumentParser(description='Scrapper le bon coin.')
    parser.add_argument("type_bien", help="type de bien (maison, appartement, terrain)", type=str)
    parser.add_argument("--nbr_piece", help="nombre de pièce (default = 0)", type=int, default=0)
    args = parser.parse_args()
    type_bien = args.type_bien.lower()
    nbr_piece = args.nbr_piece

    keys = list(DEFAULT_LOCALISATIONS.keys())
    for key in keys:
        cp = key
        ville = DEFAULT_LOCALISATIONS[key]
        if(nbr_piece>0):
            URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/provence_alpes_cote_d_azur/bouches_du_rhone/?th=1&location='+quote(ville, safe='')+'%20'+cp+'&pe=10&sqs=6&ros='+str(nbr_piece)+'&ret='+DEFAULT_TYPES[type_bien]
        else:
            URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/provence_alpes_cote_d_azur/bouches_du_rhone/?th=1&location='+quote(ville, safe='')+'%20'+cp+'&pe=10&sqs=6&ret='+DEFAULT_TYPES[type_bien]
        print(ville + " " + cp)
        for item in browse(URL, DEFAULT_CATEGORIES):
            try:
                item.serialize()
                item.save()
                print("-----")
            except:
                print(item.ad_number())
                print("%s: %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                break
        print("=====")
