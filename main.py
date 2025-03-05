import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

HUBSPOT_SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search"

@app.get("/consultar-envio")
def consultar_envio(email: str):
    """
    Devuelve información en JSON (como ya tenías).
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
        return {"error": f"Error en la consulta a HubSpot: {response.status_code} - {response.text}"}


@app.get("/consultar-envio-html", response_class=HTMLResponse)
def consultar_envio_html(email: str):
    """
    Devuelve la información en formato HTML.
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
            
            # Desglose de campos
            estatus = contacto.get("estatus", "No disponible")
            nombre = contacto.get("firstname", "No disponible")
            destino = contacto.get("destino", "No disponible")
            numero_guia = contacto.get("tracking_id", "No disponible")
            fecha_rec = contacto.get("fecha_de_recoleccion", "No disponible")
            receptor = contacto.get("nombre_del_reseptor", "No disponible")
            tamano_caja = contacto.get("tamano_de_la_caja", "No disponible")
            peso = contacto.get("peso_del_paquete", "No disponible")
            tel = contacto.get("phone", "No disponible")
            whatsapp = contacto.get("hs_whatsapp_phone_number", "No disponible")
            direccion = contacto.get("address", "No disponible")

            # Construimos HTML
            html_content = f"""
            <html>
            <head>
                <title>Detalles del Envío</title>
                <meta charset="utf-8"/>
                <style>
                    body {{
                        font-family: Arial, sans-serif; 
                        margin: 20px; 
                        padding: 0;
                    }}
                    table {{
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        border: 1px solid #ccc;
                        padding: 8px 12px;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                </style>
            </head>
            <body>
                <h1>Detalle de Envío</h1>
                <p><strong>Email consultado:</strong> {email}</p>
                <table>
                    <tr><th>Estatus</th><td>{estatus}</td></tr>
                    <tr><th>Nombre</th><td>{nombre}</td></tr>
                    <tr><th>Destino</th><td>{destino}</td></tr>
                    <tr><th>Número de Guía</th><td>{numero_guia}</td></tr>
                    <tr><th>Fecha de Recolección</th><td>{fecha_rec}</td></tr>
                    <tr><th>Nombre del Receptor</th><td>{receptor}</td></tr>
                    <tr><th>Tamaño de la Caja</th><td>{tamano_caja}</td></tr>
                    <tr><th>Peso del Paquete</th><td>{peso}</td></tr>
                    <tr><th>Teléfono</th><td>{tel}</td></tr>
                    <tr><th>WhatsApp</th><td>{whatsapp}</td></tr>
                    <tr><th>Dirección</th><td>{direccion}</td></tr>
                </table>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=200)
        else:
            return HTMLResponse("<h2>No se encontró el contacto con ese correo.</h2>", status_code=404)
    else:
        return HTMLResponse(f"<h2>Error en la consulta a HubSpot ({response.status_code}): {response.text}</h2>", status_code=500)


