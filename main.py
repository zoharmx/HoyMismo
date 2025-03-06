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

    # Aquí definimos las propiedades que deseas extraer
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
            contacto = data["results"][0].get("properties", {})

            # Retornamos las propiedades con las nuevas claves
            return {
                "vehicle_color": contacto.get("vehicle_color", "No disponible"),
                "status": contacto.get("status", "No disponible"),
                "vehicle_make": contacto.get("vehicle_make", "No disponible"),
                "modelo": contacto.get("modelo", "No disponible"),
                "tracking_id": contacto.get("tracking_id", "No disponible"),
                "tracking_number": contacto.get("tracking_number", "No disponible"),
                "tipo_pedimento": contacto.get("tipo_pedimento", "No disponible"),
                "vin_number": contacto.get("vin_number", "No disponible"),
                "firstname": contacto.get("firstname", "No disponible"),
                "phone": contacto.get("phone", "No disponible"),
                "email": contacto.get("email", "No disponible"),
                "start_date": contacto.get("start_date", "No disponible"),
                "address": contacto.get("address", "No disponible")
            }
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {
            "error": f"Error en la consulta a HubSpot: {response.status_code} - {response.text}"
        }

# (Opcional) Si deseas un endpoint HTML, podrías crearlo:
@app.get("/consultar-tramite-html", response_class=HTMLResponse)
def consultar_tramite_html(email: str):
    """
    Versión HTML opcional que muestra datos en tabla.
    """
    data = consultar_tramite(email)
    if "error" in data:
        return f"<h1>Error: {data['error']}</h1>"

    html = "<html><head><title>Trámite - Info</title></head><body>"
    html += "<h1>Detalle del Trámite</h1><table border='1'>"
    for key, val in data.items():
        html += f"<tr><th>{key}</th><td>{val}</td></tr>"
    html += "</table></body></html>"
    return html

