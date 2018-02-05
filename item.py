# -*- coding: utf-8 -*-
from utils import javascript_array2python_list, get_img_urls, write_pdf
from datetime import datetime

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
        begin_option = object_data[1:].index('options')
        end_option = object_data[:-1].rfind('}') + 1
        object_data = object_data[0:begin_option-1]+object_data[end_option+10:]
        self.serialized_data = javascript_array2python_list(object_data)
        self.description = self.data.find('p', class_="value", itemprop="description").text
        self.interest_data = {
            'annonce' : self.serialized_data['offres'],
            'publié le' : self.serialized_data['publish_date'],
            'dernière modification le' : self.serialized_data['last_update_date'],
            'photo disponible' : self.serialized_data['nbphoto'],
            'prix' : self.serialized_data['prix'],
        }
        try:
            self.interest_data['surface'] = self.serialized_data['surface']
        except:
            pass
        try:
            self.interest_data['nombre de pièces'] = self.serialized_data['pieces']
        except:
            pass
        try:
            self.interest_data['ges'] = self.serialized_data['ges']
        except:
            pass
        try:
            self.interest_data['nrj'] = self.serialized_data['nrj']
        except:
            pass

        # get picture urls
        if(image):
            if(self.serialized_data['nbphoto'].replace('"','')!="1"):
                script_img = body.find_all('script')[7]
                self.url_img_list = get_img_urls(script_img)
            elif(self.serialized_data['nbphoto'].replace('"','')=="1"):
                self.url_img_list = [self.data.find("meta", property="og:image")["content"]]
            elif(self.serialized_data['nbphoto'].replace('"','')=="0"):
                pass
                
    def save(self, doc, args):
        item_last_update = datetime.strptime(self.serialized_data['last_update_date'], '"%d/%m/%Y"')
        if item_last_update > args.last_update:
            if "viager" not in self.data.text.lower(): 
                print(self.serialized_data['titre'])
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
        begin_option = object_data[1:].index('options')
        end_option = object_data[:-1].rfind('}') + 1
        object_data = object_data[0:begin_option-1]+object_data[end_option+10:]
        self.serialized_data = javascript_array2python_list(object_data)
        self.description = self.data.find('p', class_="value", itemprop="description").text
        self.interest_data = {
            'annonce' : self.serialized_data['offres'],
            'publié le' : self.serialized_data['publish_date'],
            'dernière modification le' : self.serialized_data['last_update_date'],
            'photo disponible' : self.serialized_data['nbphoto'],
            'prix' : self.serialized_data['prix']
        }
        try:
            self.interest_data['année'] = self.serialized_data['annee']
        except:
            pass
        try:
            self.interest_data['kimométrage'] = self.serialized_data['km']
        except:
            pass
        try:
            self.interest_data['Cylindrée'] = self.serialized_data['cc']
        except:
            pass

        # get picture urls
        if(image):
            if(self.serialized_data['nbphoto'].replace('"','')!="1"):
                script_img = body.find_all('script')[7]
                self.url_img_list = get_img_urls(script_img)
            elif(self.serialized_data['nbphoto'].replace('"','')=="1"):
                self.url_img_list = [self.data.find("meta", property="og:image")["content"]]
            elif(self.serialized_data['nbphoto'].replace('"','')=="0"):
                pass
                
    def save(self, doc, args):
        item_last_update = datetime.strptime(self.serialized_data['last_update_date'], '"%d/%m/%Y"')
        if item_last_update > args.last_update:
                print(self.serialized_data['titre'])
                # generate pdf
                return(write_pdf(self, doc, args.image))
        else:
            return()
        
    def __str__(self):
        return(self.item_url)


