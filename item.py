# -*- coding: utf-8 -*-
from utils import get_img_urls, write_pdf
from datetime import datetime
import json

class Immobilier(object):
    def __init__(self, item_url, data):
        self.item_url = item_url
        self.data = data
        self.serialized_data = None
        self.interest_data = None
        self.url_img_list = []
        self.description = ""

    def ad_number(self):
        p1 = self.item_url.rindex("/") + 1
        p2 = self.item_url.index(".htm")
        return self.item_url[p1:p2]

    def serialize(self, image):
        # get infos
        body = self.data.find('body')
        script_elt = str(body.findAll('script')[3])
        begin = script_elt.index('{')
        end = script_elt.rfind('}') + 1
        object_data = script_elt[begin:end]
        self.serialized_data = json.loads(object_data)['adview']
        self.description = self.serialized_data['body']
        self.interest_data = {
            'annonce' : self.serialized_data['owner']['type'],
            'publié le' : self.serialized_data['first_publication_date'],
            'dernière modification le' : self.serialized_data['index_date'],
            'photo disponible' : self.serialized_data['images']['nb_images'],
            'prix' : str(self.serialized_data['price'][0])+" €",
        }
        try:
            self.interest_data['surface'] = [d['value_label'] for d in self.serialized_data['attributes'] if d.get('key')=='square'][0]
        except:
            pass
        try:
            self.interest_data['nombre de pièces'] = [d['value'] for d in self.serialized_data['attributes'] if d.get('key')=='rooms'][0]
        except:
            pass
        try:
            self.interest_data['ges'] = [d['value_label'] for d in self.serialized_data['attributes'] if d.get('key')=='ges'][0]
        except:
            pass
        try:
            self.interest_data['nrj'] = [d['value_label'] for d in self.serialized_data['attributes'] if d.get('key')=='energy_rate'][0]
        except:
            pass

        # get picture urls
        if(image):
            self.url_img_list = self.serialized_data['images']['urls']
                
    def save(self, doc, args):
        item_last_update = datetime.strptime(self.serialized_data['index_date'], '%Y-%m-%d %H:%M:%S')
        if item_last_update > args.last_update:
            if "viager" not in self.data.text.lower(): 
                print(self.serialized_data['subject'])
                # generate pdf
                return(write_pdf(self, doc, args.image))
            else:
                print("viager")
                return()
        else:
            return()
            
    def __str__(self):
        return(self.item_url)



class Vehicule(object):
    def __init__(self, item_url, data):
        self.item_url = item_url
        self.data = data
        self.serialized_data = None
        self.interest_data = None
        self.url_img_list = []
        self.description = ""

    def ad_number(self):
        p1 = self.item_url.rindex("/") + 1
        p2 = self.item_url.index(".htm")
        return self.item_url[p1:p2]

    def serialize(self, image):
        # get infos
        body = self.data.find('body')
        script_elt = str(body.findAll('script')[3])
        begin = script_elt.index('{')
        end = script_elt.rfind('}') + 1
        object_data = script_elt[begin:end]
        self.serialized_data = json.loads(object_data)['adview']
        self.description = self.serialized_data['body']
        self.interest_data = {
            'annonce' : self.serialized_data['owner']['type'],
            'publié le' : self.serialized_data['first_publication_date'],
            'dernière modification le' : self.serialized_data['index_date'],
            'photo disponible' : self.serialized_data['images']['nb_images'],
            'prix' : str(self.serialized_data['price'][0])+" €",
        }
        try:
            self.interest_data['année'] = [d['value_label'] for d in self.serialized_data['attributes'] if d.get('key')=='regdate'][0]
        except:
            pass
        try:
            self.interest_data['kilométrage'] = [d['value_label'] for d in self.serialized_data['attributes'] if d.get('key')=='mileage'][0]
        except:
            pass
        try:
            self.interest_data['Cylindrée'] = [d['value_label'] for d in self.serialized_data['attributes'] if d.get('key')=='cubic_capacity'][0]
        except:
            pass

        # get picture urls
        if(image):
            self.url_img_list = self.serialized_data['images']['urls']
                
    def save(self, doc, args):
        item_last_update = datetime.strptime(self.serialized_data['index_date'], '%Y-%m-%d %H:%M:%S')
        if item_last_update > args.last_update:
                print(self.serialized_data['subject'])
                # generate pdf
                return(write_pdf(self, doc, args.image))
        else:
            return()
        
    def __str__(self):
        return(self.item_url)


    
class General(object):
    def __init__(self, item_url, data):
        self.item_url = item_url
        self.data = data
        self.serialized_data = None
        self.interest_data = None
        self.url_img_list = []
        self.description = ""

    def ad_number(self):
        p1 = self.item_url.rindex("/") + 1
        p2 = self.item_url.index(".htm")
        return self.item_url[p1:p2]

    def serialize(self, image):
        # get infos
        body = self.data.find('body')
        script_elt = str(body.findAll('script')[3])
        begin = script_elt.index('{')
        end = script_elt.rfind('}') + 1
        object_data = script_elt[begin:end]
        self.serialized_data = json.loads(object_data)['adview']
        self.description = self.serialized_data['body']
        self.interest_data = {
            'annonce' : self.serialized_data['owner']['type'],
            'publié le' : self.serialized_data['first_publication_date'],
            'dernière modification le' : self.serialized_data['index_date'],
            'photo disponible' : self.serialized_data['images']['nb_images'],
            'prix' : str(self.serialized_data['price'][0])+" €",
        }

        # get picture urls
        if(image):
            self.url_img_list = self.serialized_data['images']['urls']
                
    def save(self, doc, args):
        item_last_update = datetime.strptime(self.serialized_data['index_date'], '%Y-%m-%d %H:%M:%S')
        if item_last_update > args.last_update:
                print(self.serialized_data['subject'])
                # generate pdf
                return(write_pdf(self, doc, args.image))
        else:
            return()
        
    def __str__(self):
        return(self.item_url)


