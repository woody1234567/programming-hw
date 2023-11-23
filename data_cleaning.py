import pandas as pd
def data_cleaner(hotel_info):
    hotel_info=hotel_info.drop_duplicates().dropna()
    hotel_info=hotel_info.reset_index().drop(columns=["index"])
    
    hotel_info["distance_numeric"]=0

    # distance
    for i in range(hotel_info.shape[0]):
        slice=hotel_info["distance"][i].find("km")
        if slice!=-1:
            distance_temp=float(hotel_info["distance"][i][0:slice-1])
            hotel_info.loc[i, "distance_numeric"]=distance_temp
        else:
            slice_temp=hotel_info["distance"][i].find("m")
            distance_temp=float(hotel_info["distance"][i][0:slice_temp-1])/1000
            hotel_info.loc[i, "distance_numeric"]=distance_temp
            

    hotel_info["price_numeric"]=0

    # price
    for i in range(hotel_info.shape[0]):
        slice=hotel_info["price"][i].find("TWD")
        if slice!=-1:
            price_temp=int(hotel_info["price"][i][slice+4:].replace(",",""))
            hotel_info.loc[i, "price_numeric"]=price_temp
        else:
            continue
    #rating 
    hotel_info["rating"]=hotel_info["rating"].astype("float")

    #comment
    hotel_info["comments"]=hotel_info["comments"].astype("str")

    return hotel_info
    