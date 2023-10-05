import pandas as pd
import warnings
import geopandas as gpd
import googlemaps
from datetime import datetime
warnings.filterwarnings("ignore")
import requests
import shutil
import re
from io import BytesIO, StringIO
import zipfile
from urllib.request import urlopen

#url = 'https://opendata.nationalrail.co.uk/authenticate'
#myobj = {'Raw payload': 'username=andrew.theanvoonkit@gmail.com&password=1qaz!QAZ1qaz'}
# data to be sent to api
#data = {'POST': "https://opendata.nationalrail.co.uk/authenticate HTTP/1.1",
#        'Content-Type': 'application/x-www-form-urlencoded',
#        "Accept" : 'application/json, text/plain, */*',
#        'Host': "opendata.nationalrail.co.uk",
 #       'username': 'andrew.theanvoonkit@gmail.com',
 #       'password' :'1qaz!QAZ1qaz'}

#x = requests.post(url, data = data)

# token = "andrew.theanvoonkit@gmail.com:1689865074000:G4QejldB1cuNMNvbPorQ9DTUgMHxGNHIBXl4iPIKH20="

# data = {
#     "GET": "https://opendata.nationalrail.co.uk/api/staticfeeds/2.0/fares HTTP/1.1",
#     "Content-Type": "application/json",
#     "Accept": "*/*",
#     "Host": "opendata.nationalrail.co.uk",
#     "X-Auth-Token": "andrew.theanvoonkit@gmail.com:1689865074000:G4QejldB1cuNMNvbPorQ9DTUgMHxGNHIBXl4iPIKH20="
# }

# url = "https://opendata.nationalrail.co.uk/api/staticfeeds/2.0/fares"

# r = requests.get(url, data = data, headers={'X-Auth-Token': token})


# def getFilename_fromCd(cd):
#     """
#     Get filename from content-disposition
#     """
#     if not cd:
#         return None
#     fname = re.findall('filename=(.+)', cd)
#     if len(fname) == 0:
#         return None
#     return fname[0]


# filename = getFilename_fromCd(r.headers.get('content-disposition'))
# z = zipfile.ZipFile(BytesIO(r.content))
# z.extractall("Data/Fares data")

flow_id = []
origin_code = []
destination_code = []
route_code = []
direction = []

with open('Data/Fares data/RJFAF726.FFL', 'r') as reader:
    # Read and print the entire file line by line
    for line in reader.readlines()[6:]:
        line_chars = list(line)
        if line_chars[1] == "!":
            pass
        elif line_chars[1] == "T":
            pass
        elif line == "":
            pass
        else:
            flow_id.append(line_chars[42]+line_chars[43]+line_chars[44]+line_chars[45]+line_chars[46]+line_chars[47]+line_chars[48])
            origin_code.append(line_chars[2] + line_chars[3] + line_chars[4] + line_chars[5])
            destination_code.append(line_chars[6] + line_chars[7] + line_chars[8] + line_chars[9])
            route_code.append(line_chars[10] + line_chars[11] + line_chars[12] + line_chars[13] + line_chars[14])
            direction.append(line_chars[19])


routes_df = pd.DataFrame(list(zip(flow_id, origin_code, destination_code, route_code, direction)),
               columns =["flow_id", 'origin_code', 'destination_code', "route_code", "direction"])

routes_df.to_csv("Data/Fares data/CSV/Flow_Routes.csv") 

flow_id = []
fare_pence = []
ticket_code = []
with open('Data/Fares data/RJFAF726.FFL', 'r') as reader:
    # Read and print the entire file line by line
    for line in reader.readlines()[6:]:
        line_chars = list(line)
        if line_chars[1] == "!":
            pass
        elif line_chars[1] == "F":
            pass
        elif line == "":
            pass
        else:
            flow_id.append(line_chars[2]+line_chars[3]+line_chars[4]+line_chars[5]+line_chars[6]+line_chars[7]+line_chars[8])
            fare_pence.append(line_chars[12]+line_chars[13]+line_chars[14]+line_chars[15]+line_chars[16]+line_chars[17]+line_chars[18]+line_chars[19])
            ticket_code.append(line_chars[9]+line_chars[10]+line_chars[11])
        

fares_df = pd.DataFrame(list(zip(flow_id, ticket_code,fare_pence)),
               columns =["flow_id", "ticket_code", 'fare_pence'])
fares_df.to_csv("Data/Fares data/CSV/Flow_Fares.csv")  


ticket_code = []
ticket_class = []
ticket_type = []
max_passengers = []
min_passengers = []
max_adults = []
min_adults = []
max_child =[]
min_child = []

with open('Data/Fares data/RJFAF726.TTY', 'r') as reader:
    # Read and print the entire file line by line
    for line in reader.readlines()[6:]:
        line_chars = list(line)
        if line_chars[1] == "!":
            pass
        elif line == "":
            pass
        else:
            ticket_code.append(line_chars[1]+line_chars[2]+line_chars[3])
            ticket_class.append(line_chars[43])
            ticket_type.append(line_chars[44])
            max_passengers.append(line_chars[54]+line_chars[55]+line_chars[56])
            min_passengers.append(line_chars[57]+line_chars[58]+line_chars[59])
            max_adults.append(line_chars[60]+line_chars[61]+line_chars[62])
            min_adults.append(line_chars[63]+line_chars[64]+line_chars[65])
            max_child.append(line_chars[66]+line_chars[67]+line_chars[68])
            min_child.append(line_chars[69]+line_chars[70]+line_chars[71])

types_df = pd.DataFrame(list(zip(ticket_code, ticket_class, ticket_type, max_passengers, min_passengers, max_adults, min_adults, max_child, min_child)),
               columns =["ticket_code", "ticket_class", "ticket_type", "max_passengers", "min_passengers", "max_adults", "min_adults", "max_child", "min_child"])
types_df.to_csv("Data/Fares data/CSV/ticket_types.csv")  


NLC_code = []
CRS_code = []
county = []
pte_code = []
zone_no = []
location_code = []

with open('Data/Fares data/RJFAF726.LOC', 'r') as reader:
    # Read and print the entire file line by line
    for line in reader.readlines()[6:]:
        line_chars = list(line)
        if line_chars[1] == "!":
            pass
        elif line == "":
            pass
        elif line_chars[1] == "R":
            pass
        elif line_chars[1] == "G":
            pass
        elif line_chars[1] == "M":
            pass
        elif line_chars[1] == "S":
            pass

        else:
            NLC_code.append(line_chars[36]+line_chars[37]+line_chars[38]+line_chars[39])
            CRS_code.append(line_chars[56]+line_chars[57]+line_chars[58])
            county.append(line_chars[75]+line_chars[76])
            pte_code.append(line_chars[77]+line_chars[78])
            zone_no.append(line_chars[79]+line_chars[80]+line_chars[81]+line_chars[82])
            location_code.append(line_chars[269] + line_chars[270] + line_chars[271])
        

locations_df = pd.DataFrame(list(zip(NLC_code, CRS_code,county,pte_code,zone_no, location_code)),
               columns =["NLC_code", "CRS_code","county","pte_code",'zone_no', "location_code"])
locations_df.to_csv("Data/Fares data/CSV/Locations.csv")  