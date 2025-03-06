import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"


@app.get("/consultar-tramite")
def consultar_tramite(email: str):
    """
    Consulta en HubSpot el estado del trámite basado en el email.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email
            }]
        }],
        "properties": [
            "estatus",
            "marca",
            "modelo",
            "numero_guia",
            "seguimiento",
            "tipo_pedimento",
            "vin",
            "firstname",
            "phone",
            "hs_whatsapp_phone_number",
            "email"
        ]
    }

    response = requests.post(HUBSPOT_SEARCH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            contacto = data["results"][0]["properties"]

            return {
                "estatus": contacto.get("estatus", "No disponible"),
                "marca": contacto.get("marca", "No disponible"),
                "modelo": contacto.get("modelo", "No disponible"),
                "numero_guia": contacto.get("numero_guia", "No disponible"),
                "seguimiento": contacto.get("seguimiento", "No disponible"),
                "tipo_pedimento": contacto.get("tipo_pedimento", "No disponible"),
                "vin": contacto.get("vin", "No disponible"),
                "nombre": contacto.get("firstname", "No disponible"),
                "telefono": contacto.get("phone", "No disponible"),
                "whatsapp": contacto.get("hs_whatsapp_phone_number", "No disponible"),
                "email": contacto.get("email", "No disponible")
            }
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {"error": f"Error en la consulta a HubSpot: {response.status_code} - {response.text}"}
