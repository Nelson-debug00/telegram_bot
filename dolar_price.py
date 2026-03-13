import requests
from bs4 import BeautifulSoup
import urllib3

def get_price():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = "https://www.bcv.org.ve/"
    page = requests.get(url, verify=False)


    content = BeautifulSoup(page.content, "html.parser")
    results = content.find_all("div", class_="col-sm-6 col-xs-6 centrado")
    date = content.find("span", class_="date-display-single")

    # print(date.text)

    euro = ""
    dolar = ""
    contador = 0

    for price in results[:5]:
        if contador == 0:
            euro = price.text
        
        elif contador == 4:
            dolar = price.text
        
        contador += 1

    euro = f"EUR: {float(euro.replace("'", "").replace(",", "."))}"
    dolar = f"USD: {float(dolar.replace("'", "").replace(",", "."))}"

    resultado = f"""
    
    {euro}
    {dolar}

    Fecha: {date.text}"""
    
    return resultado

# while True:
#     input("\nPresiona Enter para salir...")
#     break

if __name__ == "__main__":
    get_price()
