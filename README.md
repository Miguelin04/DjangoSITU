# Django SITU (Sistema Integrado de Transporte Urbano)

Este es un proyecto web desarrollado con **Django** que simula y administra un Sistema Integrado de Transporte Urbano (SITU). El sistema permite llevar el control de pasajeros, tarjetas de pago, unidades de transporte (buses) y los viajes realizados, gestionando automáticamente el cobro y descuento de saldo cuando se paga con tarjeta.

## Características Principales

*   **Gestión de Pasajeros:** Registro de usuarios con sus datos personales e imágenes.
*   **Gestión de Tarjetas:** Asignación de tarjetas de pago a los pasajeros y control de saldo.
*   **Gestión de Buses:** Registro de las unidades de transporte y cooperativas.
*   **Registro de Viajes:** Control detallado de los viajes realizados, incluyendo la fecha, confort, cantidad de pasajes y el método de pago.
*   **Cobro Automático:** Si el viaje se paga con tarjeta, el sistema valida el saldo y lo descuenta automáticamente del monto disponible de la tarjeta del pasajero (Costo por defecto: $0.30).
*   **API REST Básica:** El sistema expone endpoints JSON (`/api/...`) para poder integrarse con otras aplicaciones o interfaces (CRUD completo de Pasajeros, Tarjetas, Buses y Viajes).

## Requisitos Previos

*   Python 3
*   Entorno virtual configurado (el script `start.sh` espera que exista en `./env/`)

## Estructura del Proyecto

El código fuente de la aplicación Django se encuentra dentro del directorio `src/ProyectoSITU/`:
*   `appSITUweb/`: Es la aplicación principal de Django que contiene los modelos (`models.py`), vistas y controladores (`views.py`), y formularios (`forms.py`).
*   `ProyectoSITU/`: Configuración general de Django (`settings.py`, `urls.py`).

## ¿Cómo ejecutar el proyecto?

El proyecto incluye un script de bash que automatiza la ejecución del servidor, verifica puertos disponibles y aplica migraciones de la base de datos (SQLite) automáticamente.

Para iniciarlo, simplemente ejecuta en la raíz del proyecto:

```bash
./start.sh
```

El script realizará las siguientes acciones:
1. Buscará un puerto libre (por defecto `8000`). Si está ocupado, buscará el siguiente disponible.
2. Comprobará la integridad del proyecto de Django (`manage.py check`).
3. Aplicará cualquier migración pendiente en la base de datos (`manage.py migrate`).
4. Iniciará el servidor de desarrollo, el cual estará disponible en `http://127.0.0.1:8000` (o el puerto que se haya asignado).

## Endpoints de la API

El proyecto incluye rutas API para manipular los datos en formato JSON:

*   `/api/pasajeros/`: GET, POST
*   `/api/pasajeros/<id>/`: GET, PUT, PATCH, DELETE
*   `/api/tarjetas/`: GET, POST
*   `/api/tarjetas/<id>/`: GET, PUT, PATCH, DELETE
*   `/api/buses/`: GET, POST
*   `/api/buses/<id>/`: GET, PUT, PATCH, DELETE
*   `/api/viajes/`: GET, POST
*   `/api/viajes/<id>/`: GET, PUT, PATCH, DELETE
