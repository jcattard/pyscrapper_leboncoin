# -*- coding: utf-8 -*-
from utils import javascript_array2python_list
import json

class Item(object):
    def __init__(self, item_url, data):
        self.item_url = item_url
        self.data = data
        self.serialized_data = None

    def ad_number(self):
        p1 = self.item_url.rindex("/") + 1
        p2 = self.item_url.index(".htm")
        return self.item_url[p1:p2]

    def serialize(self):
        body = self.data.find('body')
        script_elt = str(body.findAll('script')[3])
        begin = script_elt.index('{')
        end = script_elt.rfind('}') + 1
        object_data = script_elt[begin:end]
        begin_option = object_data[1:].index('options')
        end_option = object_data[:-1].rfind('}') + 1
        object_data = object_data[0:begin_option-1]+object_data[end_option+10:]
        self.serialized_data = javascript_array2python_list(object_data)

    def save(self):
        try:
            print(self.serialized_data['titre'])
            print("annonce : " + self.serialized_data['offres'])
            print("publié le : " + self.serialized_data['publish_date'])
            print("dernière modification le : " + self.serialized_data['last_update_date'])
            print("photo disponible : " + self.serialized_data['nbphoto'])
            print("prix : " + self.serialized_data['prix'])
            print("surface : " + self.serialized_data['surface'])
            print("nombre de pièces : " + self.serialized_data['pieces'])
            print("ges : " + self.serialized_data['ges'])
            print("nrj : " + self.serialized_data['nrj'])
            print("url : " + self.url)
        except:
            pass
        
    def __str__(self):
        return(self.item_url)


