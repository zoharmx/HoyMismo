import os
import requests
from fastapi import FastAPI

app = FastAPI()

# Token de HubSpot (puedes definirlo directamente aquí o usar variables de entorno)
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")


# URL de HubSpot para consultar contactos
HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"

@app.get("/consultar-tramite")
def consultar_tramite(email: str, numero_guia: str):
    """
    Consulta en HubSpot el estado del trámite y otras propiedades basado en email y número de guía.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",  # 🔹 Corregido aquí
        "Content-Type": "application/json"
    }

    # Cuerpo de la solicitud para buscar el contacto por correo
    payload = {
        "filterGroups": [{
            "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
        }],
        "properties": [
            "estatus_tramite",
            "marca",
            "modelo",
            "numero_guia",
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

            # Validar si el número de guía coincide con el registrado
            if contacto.get("numero_guia", "").strip() == numero_guia.strip():
                return {
                    "estatus_tramite": contacto.get("estatus_tramite", "No disponible"),
                    "marca": contacto.get("marca", "No disponible"),
                    "modelo": contacto.get("modelo", "No disponible"),
                    "numero_guia": contacto.get("numero_guia", "No disponible"),
                    "seguimiento": contacto.get("seguimiento", "No disponible"),
                    "tipo_de_pedimento": contacto.get("tipo_de_pedimento", "No disponible"),
                    "vin": contacto.get("vin", "No disponible"),
                }
            else:
                return {"error": "Número de guía no coincide con el correo."}
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {"error": f"Error en la consulta a HubSpot: {response.text}"}

