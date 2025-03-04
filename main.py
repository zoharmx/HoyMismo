from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Lee la clave de HubSpot de una variable de entorno
HUBSPOT_API_KEY = os.environ.get("HUBSPOT_API_KEY")

HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"

@app.get("/consultar-tramite")
def consultar_tramite(email: str, numero_guia: str):
    """
    Consulta el estado del trámite en HubSpot basado en el email y número de guía.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
        }],
        "properties": ["estatus_tramite", "numero_guia"]
    }

    response = requests.post(HUBSPOT_SEARCH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            contacto = data["results"][0]
            estatus = contacto["properties"].get("estatus_tramite", "No disponible")
            guia = contacto["properties"].get("numero_guia", "No disponible")

            if guia == numero_guia:
                return {"estatus_tramite": estatus, "numero_guia": guia}
            else:
                return {"error": "Número de guía no coincide con el correo."}
        else:
            return {"error": "No se encontró el contacto con ese correo."}
    else:
        return {"error": "Error en la consulta a HubSpot."}