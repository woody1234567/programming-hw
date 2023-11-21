from bs4 import BeautifulSoup
import requests 
import pandas as pd
import random
import sys

def booking_crawler(location:str,checkin:str,checkout:str):

    #picking a random header to avoid the block.
    headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
    user_agent = random.choice(headerlist)
    fake_headers = {'User-Agent': user_agent}
    #Remark:I find out that different fake agent will create different searrch result.

    page_n=25
    hotel_info=pd.DataFrame(columns=["name","location","price","rating","distance","comments"])
    offset=0
    while hotel_info.shape[0]<200:
        booking_url="https://www.booking.com/searchresults.html"
        my_params={"ss":location,"checkin":checkin,"checkout":checkout,"offset":offset}
        r=requests.get(booking_url , params=my_params,headers=fake_headers)
        if r.status_code == requests.codes.ok:
            print("Ok")
            soup=BeautifulSoup(r.text,"html.parser")

        #finding hotel name
        hotel_name=soup.find_all(class_="f6431b446c a15b38c233")
        hotel_name_Series=pd.Series(len(hotel_name))
        for i in range(len(hotel_name)):
            hotel_name_Series[offset+i]=hotel_name[offset+i].string
        hotel_info["name"]=hotel_name_Series

        #finding hotel location
        hotel_location=soup.find_all(attrs={"data-testid": "address"},class_="aee5343fdb def9bc142a")
        hotel_location_Series=pd.Series(len(hotel_location))
        for i in range(len(hotel_location)):
            hotel_location_Series[offset+i]=hotel_location[offset+i].string
        hotel_info["location"]=hotel_location_Series

        #finding hotel price
        hotel_price=soup.find_all(attrs={"data-testid": "price-and-discounted-price"},class_="f6431b446c fbfd7c1165 e84eb96b1f")
        hotel_price_Series=pd.Series(len(hotel_price))
        for i in range(len(hotel_price)):
            hotel_price_Series[offset+i]=hotel_price[offset+i].string
        hotel_info["price"]=hotel_price_Series

        #finding hotel score
        #remark: some results have no score since the hotel is new to booking. However, for some of the newcomers, booking.com provide a external score.
        #treatment: it is not pretty fair to compare the external score with booking.com internal score, so there I treat all the newcomers without internal score as nan.  
        from math import nan #in order to assign nana value to the hotel with no internal score
        hotel_score=soup.find_all(class_="aca0ade214 ebac6e22e9 cd2e7d62b0 a0ff1335a1")
        hotel_score_Series=pd.Series(len(hotel_score))
        for i in range(len(hotel_score)):
            sub_soup = BeautifulSoup(str(hotel_score[offset+i]),'html.parser')
            try:
                hotel_score_Series[offset+i]=sub_soup.find(class_="a3b8729ab1 d86cee9b25").text
            except:
                hotel_score_Series[offset+i]= nan

        #common class for both types
        #with score
        #aca0ade214 ebac6e22e9 cd2e7d62b0 a0ff1335a1
        #without score
        #aca0ade214 ebac6e22e9 cd2e7d62b0 a0ff1335a1
        hotel_info["rating"]=hotel_score_Series

        #finding hotel distance
        hotel_distance=soup.find_all(attrs={"data-testid": "distance"})
        hotel_distance_Series=pd.Series(len(hotel_distance))
        for i in range(len(hotel_distance)):
            hotel_distance_Series[offset+i]=hotel_distance[offset+i].string
        hotel_info["distance"]=hotel_distance_Series

        #finding hotel comments
        #remark: some results have no comments since the hotel is new to booking. However, for some of the newcomers, booking.com provide a external comments.
        #treatment: it is not pretty fair to compare the external comments with booking.com internal comments, so there I treat all the newcomers without internal comments as nan.  
        hotel_comments=soup.find_all(class_="aca0ade214 ebac6e22e9 cd2e7d62b0 a0ff1335a1")
        hotel_comments_Series=pd.Series(len(hotel_comments))
        for i in range(len(hotel_comments)):
            sub_soup = BeautifulSoup(str(hotel_comments[offset+i]),'html.parser')
            try:
                hotel_comments_Series[offset+i]=sub_soup.find(class_="a3b8729ab1 e6208ee469 cb2cbb3ccb").text
            except:
                hotel_comments_Series[offset+i]= nan
        hotel_info["comments"]=hotel_comments_Series
        offset+=page_n

    return hotel_info


