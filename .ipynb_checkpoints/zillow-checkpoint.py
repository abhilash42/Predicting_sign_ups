
# coding: utf-8

import urllib.request
import sys
import xml.dom.minidom
import treepredict
from importlib import reload


zwskey="YOUR_API"


def getaddressdata(address,city):
    escad=address.replace(' ','+')
    #URL
    url='http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
    url+='zws-id=%s&address=%s&citystatezip=%s'%(zwskey,escad,city)
    print(url)
    #Parse XML
    doc=xml.dom.minidom.parseString(urllib.request.urlopen(url).read())
    code=doc.getElementsByTagName('code')[0].firstChild.data
    
    if code!='0':return None
    if 1:
        zipcode=doc.getElementsByTagName('zipcode')[0].firstChild.data
        use=doc.getElementsByTagName('useCode')[0].firstChild.data
        year=doc.getElementsByTagName('yearBuilt')[0].firstChild.data
        sqft=doc.getElementsByTagName('finishedSqFt')[0].firstChild.data
        bath=doc.getElementsByTagName('bathrooms')[0].firstChild.data
        bed=doc.getElementsByTagName('bedrooms')[0].firstChild.data
        rooms=1 #doc.getElementsByTagName('totalRooms')[0].firstChild.data
        price=doc.getElementsByTagName('amount')[0].firstChild.data
    else:
        return None
    print(doc)
    return (zipcode,use,int(year),float(bath),int(bed),int(rooms),price)
getaddressdata('21 Manassas','Cambridge,MA')


def getpricelist():
    l1=[]
    lines = open('addresslist.txt').read().split("\n")
    print(lines)
    cnt=0
    for address in lines:
        print(cnt)
        cnt=cnt+1
        try:
            data=getaddressdata(address,'Cambridge,MA')
            l1.append(data)
        except:
            continue
        #print(data)
    return l1
l1=getpricelist()

l1=list(filter(None.__ne__,l1))


housetree=treepredict.build_tree(l1,scoref=treepredict.variance)

treepredict.drawtree(housetree,'housetree.jpg')

