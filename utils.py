# -*- coding: utf-8 -*-
from urllib.request import urlopen
import os, random
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image


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
    # write infos
    c.setFont('Helvetica-Bold', 15)
    c.drawString(100,750,item.serialized_data['titre'].replace('"',''))
    c.setFont('Helvetica', 8)    
    c.drawString(100,700,"url : " + item.item_url)
    c.drawString(100,680,"annonce : " + item.serialized_data['offres'].replace('"',''))
    c.drawString(100,660,"ville : " + item.serialized_data['city'].replace('"','') + " ("+item.serialized_data['cp'].replace('"','')+")")
    c.drawString(100,640,"publié le : " + item.serialized_data['publish_date'].replace('"',''))
    c.drawString(100,620,"dernière modification le : " + item.serialized_data['last_update_date'].replace('"',''))
    c.drawString(100,600,"photo disponible : " + item.serialized_data['nbphoto'].replace('"',''))
    c.drawString(100,580,"prix : " + item.serialized_data['prix'].replace('"',''))
    c.drawString(100,560,"surface : " + item.serialized_data['surface'].replace('"',''))
    c.drawString(100,540,"nombre de pièces : " + item.serialized_data['pieces'].replace('"',''))
    try:
        c.drawString(100,520,"ges : " + item.serialized_data['ges'].replace('"',''))
    except:
        pass
    try:
        c.drawString(100,500,"nrj : " + item.serialized_data['nrj'].replace('"',''))
    except:
        pass

    textobject = c.beginText()
    textobject.setTextOrigin(100, 480)
    textobject.textLines(item.description.replace('.','.\n'))
    c.drawText(textobject)
    c.showPage()

    c.setPageSize(landscape(A4))
    # Download and write img
    for i in range(0,len(item.url_img_list)):
        noise = str(int(random.random()*100000))
        url = item.url_img_list[i]
        f = open(noise+str(i)+".jpg",'wb')
        f.write(urlopen(url).read())
        f.close()
        image = Image(noise+str(i)+".jpg")
        # write img in pdf
        c.drawImage(noise+str(i)+".jpg", 0, 0, image.drawWidth*(landscape(A4)[0]/image.drawWidth), image.drawHeight*(landscape(A4)[1]/image.drawHeight))
        # Delete img files
        os.remove(noise+str(i)+".jpg")
        c.showPage()
        

    c.setPageSize(A4)
