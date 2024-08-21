import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
# Write your code below this line 👇
#---------------------CREATE A .TXT FILE WITH THE MOVIE LIST STARTING FROM 1----------------------------#
#------------CONNECT TO THE WEBPAGE-----------#

response = requests.get(url=URL)
movie_page = response.text
# print(movie_page)

#-------------USE BEAUTIFULSOUP TO PARSE---------------------#
soup = BeautifulSoup(movie_page,"html.parser")
movies = soup.find_all(name = "h3", class_="title")
# print(movies) #prints <h3 class="title">100) Stand By Me</h3>.....
movie_list = [movie.getText() for movie in movies]
# print(movie_list) #prints ['100) Stand By Me', '99) Raging Bull', '98) Amelie', '97...]

#------------REORDER LIST FROM 1 TO 100---------------#
movie_list_reversed = movie_list[::-1]
# print(movie_list_reversed) #prints ['1) The Godfather', '2) The Empire Strikes Back', '3) The Dark Knight', '4...]

#-------------SAVE THE MOVIE LIST TO THE TEXT FILE---------------------#

with open("OrderedMovieList.txt", mode="w", encoding="utf-8")  as output_file: #append to file; writes if DNE
    for movie in movie_list_reversed:
        output_file.write(f"{movie}\n")
