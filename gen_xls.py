import requests
from bs4 import BeautifulSoup
import json
from PIL import Image
from openpyxl import Workbook
from openpyxl import load_workbook
import random

def rearrange(specifications):
    rearranged = {}
    keys = specifications[0].keys()
    for key in keys:
        rearranged[key] = []
    for spec in specifications:
        for key in keys:
            if((spec[key][0] not in rearranged[key]) and (len(rearranged[key]) < 20)):
                rearranged[key].append(spec[key][0])
    return rearranged


if __name__ == '__main__':
    f = open('out.json', 'r')
    equipment_data = json.load(f)
    f.close()
    wb = load_workbook(filename = 'sample.xlsx')
    
    i = 3
    j = 2
    for product in equipment_data:
        slug = product['name'].strip().split(' ')[0] + str(random.randrange(100, 1000))
        if(len(product['specifications']) > 0):
            if ('Value(CR)' in  product['specifications'][0].keys()):
                price = product['specifications'][0]['Value(CR)'][0]
            elif ('Value (Cr)' in  product['specifications'][0].keys()):
                price = product['specifications'][0]['Value (Cr)'][0]
            elif ('Value(Cr)' in  product['specifications'][0].keys()):
                price = product['specifications'][0]['Value(Cr)'][0]
            elif ('Value (CR)' in  product['specifications'][0].keys()):
                price = product['specifications'][0]['Value (CR)'][0]
            else:
                price = 10000
            if('Mass(T)' in product['specifications'][0].keys()):
                mass = product['specifications'][0]['Mass(T)'][0]
            elif('Mass (T)' in product['specifications'][0].keys()):
                mass = product['specifications'][0]['Mass (T)'][0]
            else:
                mass = '100'
        else:
            price = 10000
            mass = '100'

        if(mass.find(',') != -1):
            print('Replacing , in: ' + mass)
            mass = mass.replace(',', '.')
            print('Replaced: ' + mass)

        if(product['img_url']):
            img_filename = product['img_url'].strip().split('/')[-2]
            if(img_filename[-1] == '/'):
                img_filename = img_filename[:-1]
        else:
            img_filename = ''
        

        sheet_main = wb['Main']
        sheet_main['A' + str(i)].value = slug
        sheet_main['B' + str(i)].value = 'YES'
        sheet_main['D' + str(i)].value = slug
        sheet_main['E' + str(i)].value = product['name']
        sheet_main['F' + str(i)].value = 'Equipment'
        sheet_main['G' + str(i)].value = '$0'
        sheet_main['H' + str(i)].value = '$' + str(price)
        sheet_main['I' + str(i)].value = '$' + str(price)
        sheet_main['J' + str(i)].value = 'Saud Kruger'
        sheet_main['L' + str(i)].value = img_filename
        sheet_main['M' + str(i)].value = product['descr']
        sheet_main['T' + str(i)].value = float(mass)
        sheet_main['AI' + str(i)].value = 'TRUE'

        if(len(product['specifications']) > 0):
            choices = rearrange(product['specifications'])
            sheet_choices = wb['Choices']
            sheet_choices['A' + str(j)] = slug
            ch_keys = choices.keys()
            for key in ch_keys:
                sheet_choices['B' + str(j)] = key
                sheet_choices['C' + str(j)] = 'Drop down list'
                choice_letter = 'E'
                for ch_item in choices[key]:
                    sheet_choices[choice_letter + str(j)] = str(ch_item)
                    choice_letter = chr(ord(choice_letter) + 1)
                j += 1
        i += 1

    wb.save(filename = 'import.xlsx')