from bs4 import BeautifulSoup

with open("kml_files/3G_mumbai_grid_WK18.kml") as fp:
    soup = BeautifulSoup(fp,"lxml")

placemarksoup = soup.find_all('LineStyle')
print(placemarksoup)
