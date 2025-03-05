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
    Consulta en HubSpot el estado del trámite y otras propiedades basado en el email.
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
            "status",
            "firstname",
            "phone",
            "hs_whatsapp_phone_number",
            "email",
            "vehicle_color",
            "vehicle_make",
            "tracking_id",
            "tipo_pedimento",
            "vin_number"
        ]
    }

    response = requests.post(HUBSPOT_SEARCH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            contacto = data["results"][0]["properties"]

            # Devuelve la información del contacto
            return {
                "estatus_tramite": contacto.get("status", "No disponible"),
                "nombre": contacto.get("firstname", "No disponible"),
                "telefono": contacto.get("phone", "No disponible"),
                "whatsapp": contacto.get("hs_whatsapp_phone_number", "No disponible"),
                "email": contacto.get("email", "No disponible"),
                "color_vehiculo": contacto.get("vehicle_color", "No disponible"),
                "marca_vehiculo": contacto.get("vehicle_make", "No disponible"),
                "numero_guia": contacto.get("tracking_id", "No disponible"),
                "tipo_pedimento": contacto.get("tipo_pedimento", "No disponible"),
                "vin": contacto.get("vin_number", "No disponible"),
            }
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {"error": f"Error en la consulta a HubSpot: {response.text}"}


