#creating the pixela app
import requests
from datetime import datetime

PIXELA_ENDPOINT ="https://pixe.la/v1/users"
USERNAME = "kiernan"
TOKEN = "nci3294gnw3sa23"
GRAPH_ID = "graph1"
headers = {
    "X-USER-TOKEN": TOKEN
}
# --------------------- create a new user---------------------#
user_params ={
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}

# response = requests.post(url=PIXELA_ENDPOINT,json=user_params)
# print(response.text)


#--------------------- Create a blank graph ---------------------#
graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

graph_config = {
    "id":"graph1",
    "name":"Cycling Graph",
    "unit":"Km",
    "type": "float",
    "color": "ajisai",
}

#created the graph image
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)
## in web browser, view graph at: https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}.html
## https://pixe.la/v1/users/kiernan/graphs/graph1.html


# ----------------------- Post a pixel to the graph ---------------------#
pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"
now = datetime.today()

pixel_add={
    "date": now.strftime("%Y%m%d"), #string as 20240813
    "quantity":"1.24" #string as intensity of the actual pixel
}
# response = requests.post(url=pixel_endpoint,json=pixel_add,headers=headers)
# print(response.text)

# ----------------------- PUT(update) a pixel to the graph ---------------------#
date_to_update = "20240812"
pixel_update_endpoint = f"{pixel_endpoint}/{date_to_update}"

pixel_update ={
    "quantity":"10.24"
}

# update_response = requests.put(url=pixel_update_endpoint,json=pixel_update,headers=headers)
# print(update_response.text)

# ----------------------- DELETE a pixel from the graph ---------------------#
date_to_delete = "20240813"
pixel_delete_endpoint = f"{pixel_endpoint}/{date_to_delete}"

# delete_response = requests.delete(url = pixel_delete_endpoint, headers=headers)
# print(delete_response.text)