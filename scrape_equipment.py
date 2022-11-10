import requests
from bs4 import BeautifulSoup
import json

product_list = []

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
    p = Product()
    # ...........................
    
    # get name
    # ...........................
    p.name = soup.find(id="firstHeading").text.strip()
    # ...........................

    # get img
    # ...........................
    err = 0
    try:
        img = soup.find("img", class_="pi-image-thumbnail")
        p.img_url = get_img_url(img)
        print(p.name + " : " + p.img_url)
    except Exception as ex: 
        err += 1
    if(len(p.img_url) == 0):
        try:
            img = soup.find("img", class_="thumbimage")
            p.img_url = get_img_url(img)
            print(p.name + " : " + p.img_url)
        except Exception as ex:
            err += 1
    if(err == 2):
        print("Could not find image for " + p.name)
    # ...........................

    # get specializations table
    # ...........................
    try:
        headers = []
        table = soup.find("table", class_="article-table")
        header_items = table.find_all("th")
        for i in header_items:
            headers.append(i.text.strip())
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        for row in rows:
            dic = {}
            cols = row.find_all("td")
            for i in range(len(cols)):
                dic[headers[i]] = [cols[i].text.strip()]
            if bool(dic):
                print(dic)
                p.specifications.append(dic)
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
            p.descr = i.text.strip()
            break
    print("DESC: " + p.descr)
    print("NAME: " + p.name)
    
    d = {}
    d['name'] = p.name
    d['img_url'] = p.img_url
    d['descr'] = p.descr
    d['spec'] = p.specifications
    product_list.append(d)

    # ...........................

if __name__ == "__main__":
    URL = "https://elite-dangerous.fandom.com/wiki/Category:Equipment"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    products = soup.find_all("a", class_="category-page__member-link")
    
    for e in products:
        p = Product()
        parse_product_page(e["href"])
    pr_json = json.dumps(product_list, indent=2)
    f = open("out.json", 'w')
    f.write(pr_json)
    f.close()
    

