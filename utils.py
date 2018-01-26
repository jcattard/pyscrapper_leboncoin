# -*- coding: utf-8 -*-

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
