import requests
import pandas as pd
from bs4 import BeautifulSoup #Importē bibliotēkas


url = "https://www.imdb.com/title/tt6084202/" #Nosaka URL un apstrādā tajā esošo informāciju
res=requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")


top = soup.find_all(class_="sc-11eed019-9 gRPuwU") 
actors = soup.find_all(class_="sc-11eed019-1 jFeBIw") #Meklē cauri klasēm nepieciešamo informāciju
for name in actors:
  print(name.text) 
characters = soup.find_all(class_="sc-11eed019-4 esZWnh") #Meklē cauri klasēm nepieciešamo informāciju
for role in characters:
  print(role.text)

df=pd.DataFrame(list(zip(actors,characters)),columns=["Name","Role"]) #Izveido dataframe
df.index = range(1, df.shape[0] + 1) #Nobīda dataframe, lai numerācija sāktos ar 1
print(df) #izprintē dataframe