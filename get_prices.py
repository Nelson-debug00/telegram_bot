import requests
from database import SessionLocal
from models.precios import PrecioDolar, PrecioEuro, PrecioUsdt
from sqlalchemy import func
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib3
import pytz

# Configuración de caché global
cache_precios = None
cache_tiempo = None
CACHE_DURACION_MINUTOS = 10

def get_dolar_prices():
    global cache_precios, cache_tiempo
    
    # Verificar si el caché es válido
    ahora = datetime.now()
    if cache_precios and cache_tiempo and (ahora - cache_tiempo).total_seconds() < CACHE_DURACION_MINUTOS * 60:
        print("⚡ Usando precios desde el caché.")
        return cache_precios

    print("🌐 Consultando precios actualizados...")
    # Inicialización de seguridad para evitar UnboundLocalError
    dolar, euro, usdt = 0.0, 0.0, 0.0
    fecha_bcv_str = "Fecha no disponible"
    fecha_bcv_db = datetime.now().strftime("%d-%m-%Y")
    fecha_usdt_str = "Fecha no disponible"
    fecha_usdt_db = datetime.now().strftime("%d-%m-%Y")

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        url = "https://www.bcv.org.ve/"
        page = requests.get(url, verify=False)
        content = BeautifulSoup(page.content, "html.parser")
        date = content.find("span", class_="date-display-single")
        
        if date:
            fecha_bcv_str = date.text.strip()
            parts = fecha_bcv_str.replace(",", "").split()
            if len(parts) >= 4:
                dia = parts[1].zfill(2)
                mes_nombre = parts[2].lower()
                anio = parts[3]

                meses_dict = {
                    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
                    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
                    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
                }
                mes_num = meses_dict.get(mes_nombre, "01")
                fecha_bcv_db = f"{anio}-{mes_num}-{dia}"

    except Exception as e:
        print(f"Error al obtener la fecha BCV: {e}")

    # Obtener Dolar y Euro (API)
    try:
        response = requests.get("https://ve.dolarapi.com/v1/cotizaciones")

        # Dolar y Euro
        if response.status_code == 200:  # Código 200 significa éxito
            data = response.json() 

            for price in data:
                if price["nombre"] == "Dólar":
                    dolar = price["promedio"]
                elif price["nombre"] == "Euro":
                    euro = price["promedio"]
    except Exception as e:
        print(f"Error BCV API: {e}")

    # Obtener USDT (API)
    try:
        response2 = requests.get("https://ve.dolarapi.com/v1/dolares/paralelo")

        # USDT
        if response2.status_code == 200:  
            data2 = response2.json() 
            usdt = data2['promedio']
            fecha_api = data2['fechaActualizacion']
            fecha_usdt = fecha_api[:10]
            fecha_usdt = datetime.strptime(fecha_usdt, "%Y-%m-%d")

            meses = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
            5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
            9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
            }

            dia = str(fecha_usdt.day).zfill(2)
            mes_str = meses[fecha_usdt.month]
            mes_db = str(fecha_usdt.month).zfill(2)
            anio = fecha_usdt.year

            fecha_usdt_str = f"{dia} de {mes_str} de {anio}"
            fecha_usdt_db = f"{anio}-{mes_db}-{dia}"

        else:
            print(f"Error Paralelo: {response2.status_code}")
    except Exception as e:
        print(f"Error USDT API: {e}")

    # Guardar en la Base de Datos y eliminar antiguos con más de 10 días
    db = SessionLocal()
    try:
        fecha_limite = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        db.query(PrecioDolar).filter(PrecioDolar.date < fecha_limite).delete()
        db.query(PrecioEuro).filter(PrecioEuro.date < fecha_limite).delete()
        db.query(PrecioUsdt).filter(PrecioUsdt.date < fecha_limite).delete()
        
        # Creamos los registros para cada moneda si el valor es mayor a 0
        if dolar > 0:
            db.add(PrecioDolar(value=dolar, date=fecha_bcv_db))
        if euro > 0:
            db.add(PrecioEuro(value=euro, date=fecha_bcv_db))
        if usdt > 0:
            db.add(PrecioUsdt(value=usdt, date=fecha_usdt_db))
        
        db.commit()
        print("💾 Precios guardados en la base de datos.")
    except Exception as e:
        db.rollback() # Si hay error, deshacemos cambios
        print(f"⚠️ Error al guardar en BD: {e}")
    finally:
        db.close()

    # Actualizar caché
    cache_precios = (dolar, euro, usdt, fecha_bcv_str, fecha_usdt_str)
    cache_tiempo = datetime.now()

    return dolar, euro, usdt, fecha_bcv_str, fecha_usdt_str

def get_last_price():
    db = SessionLocal()
    try:
        # 1. Obtenemos la fecha más reciente grabada para cada moneda
        fecha_reciente_d = db.query(func.max(PrecioDolar.date)).scalar()
        fecha_reciente_e = db.query(func.max(PrecioEuro.date)).scalar()
        fecha_reciente_u = db.query(func.max(PrecioUsdt.date)).scalar()

        # 2. Buscamos el registro más reciente que sea ESTRICTAMENTE ANTERIOR a esa fecha máxima
        tasa_dolar = db.query(PrecioDolar).filter(PrecioDolar.date < fecha_reciente_d).order_by(PrecioDolar.date.desc()).first()

        tasa_euro = db.query(PrecioEuro).filter(PrecioEuro.date < fecha_reciente_e).order_by(PrecioEuro.date.desc()).first()

        tasa_usdt = db.query(PrecioUsdt).filter(PrecioUsdt.date < fecha_reciente_u).order_by(PrecioUsdt.date.desc()).first()

        # Evitar AttributeError si la base de datos está vacía
        val_dolar = tasa_dolar.value if tasa_dolar else 0.0
        val_euro = tasa_euro.value if tasa_euro else 0.0
        val_usdt = tasa_usdt.value if tasa_usdt else 0.0
        
        fecha_bcv_ant = tasa_dolar.date
        fecha_usdt_ant = tasa_usdt.date
        return val_dolar, val_euro, val_usdt, fecha_bcv_ant, fecha_usdt_ant
        
    except Exception as e:
        print(f"Error al obtener el último precio: {e}")
    finally:
        db.close()