import requests
from bs4 import BeautifulSoup
#import pandas as pd
#import argparse
import sqlite3
import connect
#parser=argparse.ArgumentParser()
#parser.add_argument("--n",help="Enter number of pages=",type=int)
#args=parser.parse_args()
oyo_url='https://www.oyorooms.com/hotels-in-bangalore/?page='
headers={'User-Agent':'Chrome/23.0.1271.64 Safari/537.11'}

dbname=input("Enter database file name=")
n=int(input("Enter page number="))
info_list=[]
connect.connect(dbname)
for page in range(1,n):
    req=requests.get(oyo_url+str(page),headers=headers)
    content=req.content
    soup=BeautifulSoup(content,'html.parser')
    all_hotels=soup.find_all("div",{"class": "hotelCardListing"})
    for hotel in all_hotels:
        hotel_dict={}
        hotel_dict['Name']=hotel.find("h3",{"class": "listingHotelDescription__hotelName"}).text
        hotel_dict['Address']=hotel.find("span",{"itemprop":"streetAddress"}).text
        hotel_dict['Price']=hotel.find("span",{"class":"listingPrice__finalPrice"}).text
        try:
            hotel_dict['Rating']=hotel.find("span",{"class":"hotelRating__ratingSummary"}).text
        except AttributeError:
            hotel_dict['Rating']=""

        parent_amenities=hotel.find("div",{"class":"amenityWrapper"})
        amenities=[]
        try:
            for amenity in parent_amenities.find_all("div",{"class":"amenityWrapper__amenity"}):
                amenities.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())
        except AttributeError:
            pass
        hotel_dict['Amenities']=', '.join(amenities[:-1])
        info_list.append(hotel_dict)
        connect.insert_values(dbname,tuple(hotel_dict.values()))

#dataframe=pd.DataFrame(info_list)
#dataframe.to_csv("C:/Users/Shrinivas/Desktop/oyo.csv")
connect.get_info(dbname)
