# -*- coding: utf-8 -*-
from urllib.request import urlopen
import os
from reportlab.lib.units import inch, cm

def javascript_array2python_list(array):
    results = dict()
    for i in array[1:-1].split(','):
        subres_list = i[1:].replace(' ','').split(':')
        results[subres_list[0]] = subres_list[1]
    return(results)


def get_img_urls(script_img):
    url_img_list = []
    for line in script_img.contents[0].split('\t'):
        if "images[" in line:
            begin_url = line.index('"') 
            end_url = line.rfind('"')
            url_img_list.append(line[begin_url+1:end_url])
    return(url_img_list)


def write_pdf(item, c):
    c.setFont('Helvetica-Bold', 15)
    c.drawString(100,750,item.serialized_data['titre'])
    c.setFont('Helvetica', 8)    
    c.drawString(100,700,"url : " + item.item_url)
    c.drawString(100,650,"annonce : " + item.serialized_data['offres'])
    c.drawString(100,600,"publié le : " + item.serialized_data['publish_date'])
    c.drawString(100,550,"dernière modification le : " + item.serialized_data['last_update_date'])
    c.drawString(100,500,"photo disponible : " + item.serialized_data['nbphoto'])
    c.drawString(100,450,"prix : " + item.serialized_data['prix'])
    c.drawString(100,400,"surface : " + item.serialized_data['surface'])
    c.drawString(100,350,"nombre de pièces : " + item.serialized_data['pieces'])
    try:
        c.drawString(100,300,    "ges : " + item.serialized_data['ges'])
    except:
        pass
    try:
        c.drawString(100,250,    "nrj : " + item.serialized_data['nrj'])
    except:
        pass
    c.showPage()

    # Download img
    for i in range(0,len(item.url_img_list)):
        url = item.url_img_list[i]
        f = open(str(i)+".jpg",'wb')
        f.write(urlopen(url).read())
        f.close()
        # write img in pdf
        c.drawImage(str(i)+".jpg", 0, 0, 20*cm, 30*cm)
        # Delete img files
        os.remove(str(i)+".jpg")
        c.showPage()
        

