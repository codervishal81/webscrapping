import requests
from bs4 import BeautifulSoup
import pandas

base_url = "https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
data_list = []

for pg_no in range(0, 30, 10): #TODO: scrap last page number from the page itself because total pages can change with time as well as with different search criteria
    print(base_url + str(pg_no) + ".html")
    r = requests.get(base_url + str(pg_no) + ".html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class":"propertyRow"})
    
    for item in all:
        d = {}

        d["Address"] = item.find_all("span", {"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"] = item.find_all("span", {"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
            
        d["Price"] = item.find("h4", {"class":"propPrice"}).text.strip()

        try:
            d["Beds"] = item.find("span", {"class":"infoBed"}).find("b").text
        except:
            d["Beds"] = None

        try:
            d["Area"] = item.find("span", {"class":"infoSqFt"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Full Baths"] = item.find("span", {"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = None

        try:
            d["Half Baths"] = item.find("span", {"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None

        d["Lot Size"] = None
        for col_group in item.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(col_group.find_all("span", {"class":"featureGroup"}), col_group.find_all("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        data_list.append(d)
    
df=pandas.DataFrame(data_list)
print(df)
df.to_csv("output.csv")

