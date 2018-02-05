# -*- coding: utf-8 -*-
from urllib.request import urlopen
import random
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image, PageBreak, Paragraph
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet

from common import ALIAS_CATEGORIES, DEFAULT_PRIX_MAX_IMMOBILIER, DEFAULT_PRIX_MAX_VEHICULE, DEFAULT_SURFACE, DEFAULT_TYPES, ALIAS_DEPARTMENT, ALIAS_REGION
from urllib.parse import quote
import argparse, sys, time
from datetime import datetime, timedelta


def parse_inputs():
    parser = argparse.ArgumentParser(description='Scrapper le bon coin.')
    parser.add_argument("type_bien", help="type de bien (maison, appartement, terrain)", type=str)
    parser.add_argument("--nbr_piece", help="nombre de pièce minimale (default = 0)", type=int, default=0)
    parser.add_argument("--prix_max", help="prix maximal (default = 0)", type=int, default=0)
    parser.add_argument("--surface_min", help="surface minimale (default = 0)", type=int, default=0)
    parser.add_argument("--image", type=str2bool, nargs='?', const=True, default=False, help="display images in report (default = False)")
    parser.add_argument("--cylindre_min", help="cylindré minimal (default = 0)", type=int, default=0)
    parser.add_argument("--report_name", help="nom du rapport (default = report.pdf)", type=str, default="report.pdf")
    parser.add_argument("--departement", help="id du département considéré (default=-1)", type=int, default=-1)
    parser.add_argument("--last_update", help="nombre de jour max depuis la dernière modification (default=0)", type=int, default=0)

    args = parser.parse_args()
    
    # Check inputs
    if str(args.type_bien) not in ALIAS_CATEGORIES:
            sys.exit("Wrong TYPE: type "+args.type_bien+" does not exist, cadidates are ["+"; ".join([str(k) for k in ALIAS_CATEGORIES.keys()])+"]")
    if ALIAS_CATEGORIES[args.type_bien] == "ventes_immobilieres":
        if str(args.prix_max) not in DEFAULT_PRIX_MAX_IMMOBILIER:
            sys.exit("Wrong PRICE: price "+str(args.prix_max)+" does not exist, cadidates are ["+"; ".join([str(k) for k in DEFAULT_PRIX_MAX_IMMOBILIER.keys()])+"]")

    elif ALIAS_CATEGORIES[args.type_bien] == "motos":
        if str(args.prix_max) not in DEFAULT_PRIX_MAX_VEHICULE:
            sys.exit("Wrong PRICE: price "+str(args.prix_max)+" does not exist, cadidates are ["+"; ".join([str(k) for k in DEFAULT_PRIX_MAX_VEHICULE.keys()])+"]")
    else:
        pass

    if str(args.surface_min) not in DEFAULT_SURFACE:
        sys.exit("Wrong SURFACE: surface "+str(args.surface_min)+" does not exist, cadidates are ["+"; ".join([str(k) for k in DEFAULT_SURFACE.keys()])+"]")

    if args.last_update >= 0:
        if args.last_update == 0:
            args.last_update = datetime(year=1, month=1, day=1)
        else:
            args.last_update = datetime.today() - timedelta(days=args.last_update)
    else:
        sys.exit("Wrong LAST_UPDATE: last_update may be positif")
    return(args)



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

def write_pdf(item, doc, image):
    styles = getSampleStyleSheet()
    Story=[]
    Story.append(Paragraph(item.serialized_data['titre'].replace('"',''), styles["Title"]))
    Story.append(Paragraph("url : " + item.item_url, styles["Bullet"]))
    Story.append(Paragraph("ville : " + item.serialized_data['city'].replace('"','') + " ("+item.serialized_data['cp'].replace('"','')+")", styles["Bullet"]))
    for key in item.interest_data:
        Story.append(Paragraph(key+" : "+item.interest_data[key].replace('"',''), styles["Bullet"]))
    Story.append(Paragraph(item.description, styles["Bullet"]))
    Story.append(PageBreak())

    if(image):
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

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_region(args):
    for k, v in iter(ALIAS_REGION.items()):
        if args.departement in v:
            return(k)
    return(None)
    
def make_url(ville, cp, args):
    if args.departement == -1:
        if ALIAS_CATEGORIES[args.type_bien] == "ventes_immobilieres":
            if args.nbr_piece != 0:
                URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/provence_alpes_cote_d_azur/bouches_du_rhone/?th=1&location='+quote(ville, safe='')+'%20'+cp+'&pe='+DEFAULT_PRIX_MAX_IMMOBILIER[str(args.prix_max)]+'&sqs='+DEFAULT_SURFACE[str(args.surface_min)]+'&ros='+str(args.nbr_piece)+'&ret='+DEFAULT_TYPES[str(args.type_bien)]
            else:
                URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/provence_alpes_cote_d_azur/bouches_du_rhone/?th=1&location='+quote(ville, safe='')+'%20'+cp+'&pe='+DEFAULT_PRIX_MAX_IMMOBILIER[str(args.prix_max)]+'&sqs='+DEFAULT_SURFACE[str(args.surface_min)]+'&ret='+DEFAULT_TYPES[str(args.type_bien)]
        elif ALIAS_CATEGORIES[args.type_bien] == "motos":
            URL = 'https://www.leboncoin.fr/motos/offres/provence_alpes_cote_d_azur/bouches_du_rhone/?th=1&q='+args.type_bien+'&location='+quote(ville, safe='')+'%20'+cp+'&pe='+DEFAULT_PRIX_MAX_VEHICULE[str(args.prix_max)]+'&ccs='+str(args.cylindre_min)
        else:
            URL=""
    else:
        region = get_region(args)
        if region:
            if ALIAS_CATEGORIES[args.type_bien] == "ventes_immobilieres":
                if args.nbr_piece == 0:
                    URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/'+region+'/'+quote(ALIAS_DEPARTMENT[args.departement], safe='')+'/?th=1&pe='+DEFAULT_PRIX_MAX_IMMOBILIER[str(args.prix_max)]+'&sqs='+DEFAULT_SURFACE[str(args.surface_min)]+'&ros='+args.nbr_piece+'&ret='+DEFAULT_TYPES[str(args.type_bien)]
                else:
                    URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/'+region+'/'+quote(ALIAS_DEPARTMENT[args.departement], safe='')+'/?th=1&pe='+DEFAULT_PRIX_MAX_IMMOBILIER[str(args.prix_max)]+'&sqs='+DEFAULT_SURFACE[str(args.surface_min)]+'&ret='+DEFAULT_TYPES[str(args.type_bien)]
            elif ALIAS_CATEGORIES[args.type_bien] == "motos":
                URL = 'https://www.leboncoin.fr/motos/offres/'+region+'/'+quote(ALIAS_DEPARTMENT[args.departement], safe='')+'/?th=1&q='+args.type_bien+'&pe='+DEFAULT_PRIX_MAX_VEHICULE[str(args.prix_max)]+'&ccs='+str(args.cylindre_min)
            else:
                URL=""
        else:
            URL=""


    return(URL)
