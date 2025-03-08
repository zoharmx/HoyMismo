import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔹 Configuración de CORS para permitir solicitudes desde cualquier dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por dominios específicos si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            "vehicle_color",
            "status",
            "vehicle_make",
            "modelo",
            "tracking_id",
            "tracking_number",
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
                "color_vehiculo": contacto.get("vehicle_color", "No disponible"),
                "estatus": contacto.get("status", "No disponible"),
                "marca": contacto.get("vehicle_make", "No disponible"),
                "modelo": contacto.get("modelo", "No disponible"),
                "tracking_id": contacto.get("tracking_id", "No disponible"),
                "numero_guia": contacto.get("tracking_number", "No disponible"),
                "tipo_pedimento": contacto.get("tipo_pedimento", "No disponible"),
                "vin": contacto.get("vin_number", "No disponible"),
                "nombre": contacto.get("firstname", "No disponible"),
                "telefono": contacto.get("phone", "No disponible"),
                "email": contacto.get("email", "No disponible"),
                "fecha_inicio": contacto.get("start_date", "No disponible"),
                "direccion": contacto.get("address", "No disponible")
            }
        else:
            return {"error": "No se encontró el trámite con ese correo."}
    else:
        return {"error": f"Error en la consulta a HubSpot: {response.status_code} - {response.text}"}
