import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

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


@app.get("/consultar-tramite-html", response_class=HTMLResponse)
def consultar_tramite_html(email: str):
    """
    Devuelve la información en formato HTML para mostrar en Hostinger.
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

            html_content = f"""
            <html>
            <head>
                <title>Detalle del Trámite</title>
                <meta charset="utf-8"/>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }}
                    table {{
                        border-collapse: collapse;
                        margin-top: 20px;
                        width: 100%;
                    }}
                    th, td {{
                        border: 1px solid #ccc;
                        padding: 8px 12px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                </style>
            </head>
            <body>
                <h1>Detalle del Trámite</h1>
                <p><strong>Email consultado:</strong> {email}</p>
                <table>
                    <tr><th>Estatus Actual</th><td>{contacto.get("estatus_actual", "No disponible")}</td></tr>
                    <tr><th>Folio</th><td>{contacto.get("folio", "No disponible")}</td></tr>
                    <tr><th>Color del Vehículo</th><td>{contacto.get("vehicle_color", "No disponible")}</td></tr>
                    <tr><th>Marca del Vehículo</th><td>{contacto.get("vehicle_make", "No disponible")}</td></tr>
                    <tr><th>Modelo</th><td>{contacto.get("modelo", "No disponible")}</td></tr>
                    <tr><th>Tipo de Pedimento</th><td>{contacto.get("tipo_pedimento", "No disponible")}</td></tr>
                    <tr><th>VIN</th><td>{contacto.get("vin_number", "No disponible")}</td></tr>
                    <tr><th>Nombre</th><td>{contacto.get("firstname", "No disponible")}</td></tr>
                    <tr><th>Teléfono</th><td>{contacto.get("phone", "No disponible")}</td></tr>
                    <tr><th>Email</th><td>{contacto.get("email", "No disponible")}</td></tr>
                    <tr><th>Fecha de Inicio</th><td>{contacto.get("start_date", "No disponible")}</td></tr>
                    <tr><th>Dirección</th><td>{contacto.get("address", "No disponible")}</td></tr>
                </table>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=200)
        else:
            return HTMLResponse("<h2>No se encontró el contacto con ese correo.</h2>", status_code=404)
    else:
        return HTMLResponse(
            f"<h2>Error en la consulta a HubSpot: {response.status_code} - {response.text}</h2>",
            status_code=500
        )