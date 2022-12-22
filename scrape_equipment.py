import requests
from bs4 import BeautifulSoup
import json
from PIL import Image

product_list = []
spec_headers_all = []

class Product:
    name = ""
    img_url = ""
    descr = ""
    specifications = []

def get_img_url(imgtag):
    img_split = imgtag['src'].split('/')[:8]
    img_url = img_split[0] + "//"
    for i in range(2, len(img_split)):
        img_url += img_split[i] + "/"
    return img_url

def parse_product_page(link):
    if(link.find("Category") != -1):
        return
    url = "https://elite-dangerous.fandom.com" + link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    p = {}
    
    p['name'] = ""
    p['img_url'] = ""
    p['img_name'] = ""
    p['descr'] = ""
    p['specifications'] = []

    # ...........................
    
    # get name
    # ...........................
    p['name'] = soup.find(id="firstHeading").text.strip()
    # ...........................

    # get img
    # ...........................
    err = 0
    try:
        img = soup.find("img", class_="pi-image-thumbnail")
        p['img_url'] = get_img_url(img)
        print(p['name'] + " : " + p['img_url'])
    except Exception as ex: 
        err += 1
    if(len(p['img_url']) == 0):
        try:
            img = soup.find("img", class_="thumbimage")
            p['img_url'] = get_img_url(img)
            print(p['name'] + " : " + p['img_url'])
        except Exception as ex:
            err += 1
    if(err == 2):
        print("Could not find image for " + p['name'])
    else:    
        if(p['img_url'][-1] == '/'):
            p['img_url'] = p['img_url'][:-1]
        p['img_name'] = p['img_url'].split('/')[-1]
    # ...........................

    # get specializations table
    # ...........................
    try:
        headers = []
        table = soup.find("table", class_="article-table")
        header_items = table.find_all("th")
        for i in header_items:
            headers.append(i.text.strip())
            if(i.text.strip() not in spec_headers_all):
                spec_headers_all.append(i.text.strip())
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        for row in rows:
            dic = {}
            cols = row.find_all("td")
            for i in range(len(cols)):
                dic[headers[i]] = [cols[i].text.strip()]
            if bool(dic):
                print(dic)
                p['specifications'].append(dic)
    except Exception:
        print("Could not get specification table for item")
    # ...........................

    # get description
    # ...........................
    ps = soup.find_all("p")
    for i in ps:
        if(i.text.find("Information") != -1):
            continue
        if(i.find("b")):
            p['descr'] = i.text.strip()
            break
    product_list.append(p)

    # ...........................

def download_image(e):
    url = e['img_url']
    img_name = e['img_name']
    if(url and img_name and img_name.find('.') != -1):
        print('Trying to download image: ' + img_name)
        img = Image.open(requests.get(url, stream = True).raw)
        img.save('./images/' + img_name)
        print('Image successfully downloaded to: ' + 'images/' + img_name)



if __name__ == "__main__":
    URL = "http://elite-dangerous.fandom.com/wiki/Category:Equipment"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    products = soup.find_all("a", class_="category-page__member-link") 

    for e in products:
        parse_product_page(e["href"])
    for p in product_list:
        print('img_name: ' + p['img_name'])
        download_image(p)
    pr_json = json.dumps(product_list, indent=2)
    f = open("out.json", 'w')
    f.write(pr_json)
    f.close()
    print("ALL HEADERS:")
    print(spec_headers_all)
    

