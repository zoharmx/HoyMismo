import os
import requests
from fastapi import FastAPI

app = FastAPI()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

# URL de HubSpot para consultar contactos (endpoint de búsqueda)
HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"

@app.get("/consultar-envio")
def consultar_envio(email: str):
    """
    Consulta en HubSpot las propiedades del contacto relacionadas
    al envío/paquete, basándose en el email.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Búsqueda del contacto por email
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email
            }]
        }],
        "properties": [
            "firstname",
            "estatus",
            "destino",
            "tracking_id",
            "fecha_de_recoleccion",
            "nombre_del_reseptor",
            "tamano_de_la_caja",
            "peso_del_paquete",
            "phone",
            "hs_whatsapp_phone_number",
            "address"
        ]
    }

    response = requests.post(HUBSPOT_SEARCH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            contacto = data["results"][0]["properties"]
            return {
                "estatus": contacto.get("estatus", "No disponible"),
                "nombre": contacto.get("firstname", "No disponible"),
                "destino": contacto.get("destino", "No disponible"),
                "numero_guia": contacto.get("tracking_id", "No disponible"),
                "fecha_de_recoleccion": contacto.get("fecha_de_recoleccion", "No disponible"),
                "nombre_del_receptor": contacto.get("nombre_del_reseptor", "No disponible"),
                "tamano_de_la_caja": contacto.get("tamano_de_la_caja", "No disponible"),
                "peso_del_paquete": contacto.get("peso_del_paquete", "No disponible"),
                "telefono": contacto.get("phone", "No disponible"),
                "whatsapp": contacto.get("hs_whatsapp_phone_number", "No disponible"),
                "direccion": contacto.get("address", "No disponible")
            }
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {
            "error": f"Error en la consulta a HubSpot: {response.status_code} - {response.text}"
        }



