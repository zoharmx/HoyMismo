import os
import requests
from fastapi import FastAPI

app = FastAPI()

# Obtener el token de HubSpot desde variables de entorno
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

# URL de HubSpot para consultar contactos
HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"

@app.get("/consultar-tramite")
def consultar_tramite(email: str):
    """
    Consulta en HubSpot el estado del trámite y otras propiedades basado solo en el email.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Búsqueda del contacto por email
    payload = {
        "filterGroups": [{
            "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
        }],
        "properties": [
            "estatus_tramite",
            "marca",
            "modelo",
            "seguimiento",
            "tipo_de_pedimento",
            "vin"
        ]
    }

    response = requests.post(HUBSPOT_SEARCH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            contacto = data["results"][0]["properties"]

            # Devuelve la información del contacto sin validar el número de guía
            return {
                "estatus_tramite": contacto.get("estatus_tramite", "No disponible"),
                "marca": contacto.get("marca", "No disponible"),
                "modelo": contacto.get("modelo", "No disponible"),
                "seguimiento": contacto.get("seguimiento", "No disponible"),
                "tipo_de_pedimento": contacto.get("tipo_de_pedimento", "No disponible"),
                "vin": contacto.get("vin", "No disponible"),
            }
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {"error": f"Error en la consulta a HubSpot: {response.text}"}


