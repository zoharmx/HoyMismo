# HoyMismo - Rastreo de Paquetes (Integración con HubSpot)

Este proyecto ejemplifica cómo consultar (vía API de HubSpot) las propiedades 
de un contacto relacionadas con el envío/paquete de HoyMismo.

## Características

- Endpoint `/consultar-envio` que recibe el parámetro `email` (Query Param).
- Busca en HubSpot un contacto con dicho email.
- Retorna en JSON las propiedades del paquete: estatus, destino, tracking_id, etc.

## Requisitos y Ejecución

1. Clonar este repositorio.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt

