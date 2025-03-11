import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes reemplazar "*" con un dominio específico para mayor seguridad.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clave de API desde variable de entorno
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

# URL de HubSpot para la consulta de contactos
HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"

@app.get("/consultar-tramite")
def consultar_tramite(email: str):
    """
    Consulta en HubSpot el estado actual del trámite y otras propiedades basado en el email.
    Devuelve información en formato JSON.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "email", "operator": "EQ", "value": email}
            ]
        }],
        "properties": [
            "estatus_actual",
            "folio",
            "vehicle_color",
            "vehicle_make",
            "modelo",
            "tipo_pedimento",
            "vin_number",
            "firstname",
            "phone",
            "email",
            "start_date",
            "address"
        ]
    }

    response = requests.post(HUBSPOT_SEARCH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            contacto = data["results"][0]["properties"]

            return {
                "estatus_actual": contacto.get("estatus_actual", "No disponible"),
                "folio": contacto.get("folio", "No disponible"),
                "color_vehiculo": contacto.get("vehicle_color", "No disponible"),
                "marca": contacto.get("vehicle_make", "No disponible"),
                "modelo": contacto.get("modelo", "No disponible"),
                "tipo_pedimento": contacto.get("tipo_pedimento", "No disponible"),
                "vin": contacto.get("vin_number", "No disponible"),
                "nombre": contacto.get("firstname", "No disponible"),
                "telefono": contacto.get("phone", "No disponible"),
                "email": contacto.get("email", "No disponible"),
                "fecha_inicio": contacto.get("start_date", "No disponible"),
                "direccion": contacto.get("address", "No disponible")
            }
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {"error": f"Error en la consulta a HubSpot: {response.status_code} - {response.text}"}