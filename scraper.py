#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import sys, os, glob
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4, landscape

from utils import str2bool, make_url, parse_inputs, get_region
from item import Immobilier, Vehicule
from common import DEFAULT_LOCALISATIONS, DEFAULT_CATEGORIES, ALIAS_DEPARTMENT

def get_item(data, model):
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
    

def browse(url, categories):
    category = url.split('/')[3]
    if category not in categories:
        raise Exception("Wrong URL: category '%s' does not exist" % category)
    model = eval(categories[category])
    page = urlopen(url)
    data = BeautifulSoup(page.read(), "html.parser")
    if data.find('span', class_="total_page"):
        url_page = "https:" + data.find("a", class_="element page static link-like", id="next")["href"]
        nbr_page = int(data.find("span", class_="total_page").text)
        page_all = b''
        for i in range(1,nbr_page+1):
            print("page "+str(i)+"/"+str(nbr_page))
            url_current = url_page.replace("?o=2", "?o="+str(i))
            page_current = urlopen(url_current).read()
            page_all += page_current
        data_all = BeautifulSoup(page_all, "html.parser")
        return(get_item(data_all, model))
    else:
        return(get_item(data, model))

if __name__ == '__main__':
    # Parse inputs
    args = parse_inputs()

    # Loop on define location
    keys = list(DEFAULT_LOCALISATIONS.keys())
    # begin pdf file
    doc = SimpleDocTemplate(args.report_name,pagesize=landscape(A4))
    story=[]
    if(args.departement == -1):
        for key in keys:
            cp = key
            ville = DEFAULT_LOCALISATIONS[key]
            # Set URL if set unset nbr_piece
            URL = make_url(ville, cp, args)
            # Print current city and cp
            print(ville + " " + cp)
            # Loop on result for city
            for item in browse(URL, DEFAULT_CATEGORIES):
                try:
                    item.serialize(args.image)
                    story += item.save(doc, args.image)
                    print("-----")
                except:
                    print(item.ad_number())
                    print("%s: %s" % (sys.exc_info()[0], sys.exc_info()[1]))
            print("=====")
    else:
        cp = None
        ville = None
        # Set URL if set unset nbr_piece
        URL = make_url(ville, cp, args)
        # Print current city and cp
        print("search on region " + get_region(args) +", department "+ALIAS_DEPARTMENT[args.departement])
        # Loop on result for city
        for item in browse(URL, DEFAULT_CATEGORIES):
            try:
                item.serialize(args.image)
                story += item.save(doc, args.image)
                print("-----")
            except:
                print(item.ad_number())
                print("%s: %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                print("=====")
    # close pdf file
    doc.build(story)
    # Delete img files
    for f in glob.glob("*.jpg"):
        os.remove(f)

