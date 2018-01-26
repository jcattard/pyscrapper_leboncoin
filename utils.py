# -*- coding: utf-8 -*-
from urllib.request import urlopen
import random
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image, PageBreak, Paragraph
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet


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

def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def write_pdf(item, doc):
    styles = getSampleStyleSheet()
    Story=[]
    Story.append(Paragraph(item.serialized_data['titre'].replace('"',''), styles["Title"]))

    Story.append(Paragraph("url : " + item.item_url, styles["Bullet"]))
    Story.append(Paragraph("annonce : " + item.serialized_data['offres'].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph("ville : " + item.serialized_data['city'].replace('"','') + " ("+item.serialized_data['cp'].replace('"','')+")", styles["Bullet"]))
    Story.append(Paragraph("publié le : " + item.serialized_data['publish_date'].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph("dernière modification le : " + item.serialized_data['last_update_date'].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph("photo disponible : " + item.serialized_data['nbphoto'].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph("prix : " + item.serialized_data['prix'].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph("surface : " + item.serialized_data['surface'].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph("nombre de pièces : " + item.serialized_data['pieces'].replace('"',''), styles["Bullet"]))
    try:
        Story.append(Paragraph("ges : " + item.serialized_data['ges'].replace('"',''), styles["Bullet"]))
    except:
        pass
    try:
        Story.append(Paragraph("nrj : " + item.serialized_data['nrj'].replace('"',''), styles["Bullet"]))
    except:
        pass
    Story.append(Paragraph(item.description, styles["Bullet"]))
    Story.append(PageBreak())

    # Download and write img
    for i in range(0,len(item.url_img_list)):
        filename = str(int(random.random()*100000))+str(i)+".jpg"
        url = item.url_img_list[i]
        f = open(filename,'wb')
        f.write(urlopen(url).read())
        f.close()
        # write imgs
        im = Image(filename, 20*cm, 15*cm)
        Story.append(im)
        Story.append(PageBreak())
        
    return(Story)
