# Product Requirements Document (PRD)
## EngiSensors - Plataforma de Monitoreo de Sensores de Gas Combustible

**Versión:** 1.0
**Fecha:** 2025-11-17
**Estado:** MVP en Planificación
**Autor:** Equipo EngiSensors

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Visión del Producto](#visión-del-producto)
3. [Objetivos y Metas](#objetivos-y-metas)
4. [Usuarios Objetivo](#usuarios-objetivo)
5. [Casos de Uso](#casos-de-uso)
6. [Requisitos Funcionales](#requisitos-funcionales)
7. [Requisitos No Funcionales](#requisitos-no-funcionales)
8. [Arquitectura del Sistema](#arquitectura-del-sistema)
9. [Modelo de Datos](#modelo-de-datos)
10. [Interfaces de Usuario](#interfaces-de-usuario)
11. [Plan de Desarrollo MVP](#plan-de-desarrollo-mvp)
12. [Roadmap](#roadmap)
13. [Métricas de Éxito](#métricas-de-éxito)
14. [Riesgos y Mitigación](#riesgos-y-mitigación)

---

## Resumen Ejecutivo

EngiSensors es una plataforma IoT de monitoreo y gestión de sensores de gas combustible para entornos residenciales e industriales. El sistema recibe datos en tiempo real de sensores distribuidos mediante protocolo MQTT y proporciona un sistema de alertas multicanal (email, SMS) para notificar fugas de gas potencialmente peligrosas.

### Problema
Las fugas de gas combustible representan un riesgo crítico de seguridad en viviendas e industrias. La detección temprana y la notificación rápida a las personas responsables puede prevenir accidentes, explosiones e intoxicaciones.

### Solución
Una plataforma centralizada que:
- Monitorea sensores IoT de gas combustible en tiempo real
- Organiza sensores por jerarquía: Cliente → Edificio → Apartamento → Ubicación
- Envía notificaciones inmediatas mediante email y SMS cuando se detectan fugas
- Proporciona una interfaz web para administración y monitoreo

### Alcance MVP
- Gestión de usuarios (administradores y clientes)
- Gestión jerárquica de sensores
- Recepción de datos vía MQTT
- Visualización de sensores por edificio
- Sistema de notificaciones por email y teléfono
- Panel de monitoreo en tiempo real

---

## Visión del Producto

**Ser la plataforma líder en monitoreo inteligente de seguridad para gas combustible en América Latina**, proporcionando tranquilidad a familias y empresas mediante tecnología IoT accesible y confiable.

### Propuesta de Valor

**Para Clientes Residenciales:**
- Tranquilidad 24/7 sobre la seguridad de su hogar
- Notificaciones inmediatas en caso de emergencia
- Monitoreo remoto de su propiedad

**Para Clientes Industriales:**
- Cumplimiento de normativas de seguridad
- Prevención de accidentes y pérdidas materiales
- Trazabilidad y reportes de seguridad

**Para Administradores de Edificios:**
- Gestión centralizada de seguridad
- Reducción de riesgos y responsabilidades
- Control total sobre instalaciones

---

## Objetivos y Metas

### Objetivos de Negocio
1. **Lanzar MVP en Q1 2026** con funcionalidades core
2. **Alcanzar 100 sensores activos** en los primeros 3 meses
3. **Lograr 99.9% uptime** del sistema de monitoreo
4. **Tiempo de notificación < 5 segundos** desde detección hasta alerta

### Objetivos de Usuario
1. Simplificar la gestión de sensores de gas
2. Garantizar notificaciones confiables y rápidas
3. Proporcionar visibilidad clara del estado de todos los sensores
4. Facilitar la configuración y mantenimiento

### Objetivos Técnicos
1. Arquitectura escalable para soportar 10,000+ sensores
2. Sistema de mensajería MQTT robusto y seguro
3. Base de datos optimizada para series temporales
4. APIs RESTful bien documentadas

---

## Usuarios Objetivo

### Administradores del Sistema
**Quiénes son:** Personal técnico encargado de la gestión de la plataforma

**Necesidades:**
- Crear y gestionar cuentas de clientes
- Configurar edificios, apartamentos y sensores
- Monitorear el estado general del sistema
- Generar reportes de actividad
- Gestionar usuarios administradores

**Permisos:**
- Acceso completo a todas las funcionalidades
- Gestión de todos los clientes y sensores
- Configuración del sistema

### Clientes
**Quiénes son:** Propietarios de edificios, gerentes de facilities, administradores de condominios

**Necesidades:**
- Visualizar sus edificios y sensores asociados
- Recibir notificaciones de fugas de gas
- Gestionar contactos para notificaciones
- Ver historial de eventos
- Configurar preferencias de notificación

**Permisos:**
- Ver solo sus propios edificios y sensores
- Gestionar sus propios contactos
- Recibir notificaciones

### Usuarios Finales (Futura Fase)
**Quiénes son:** Residentes de apartamentos, personal operativo

**Necesidades:**
- Ver estado de sensores en su apartamento
- Recibir notificaciones de su unidad
- Reportar problemas con sensores

---

## Casos de Uso

### CU-001: Detección y Notificación de Fuga de Gas

**Actor Principal:** Sistema, Cliente
**Precondición:** Sensor instalado y configurado, Cliente con contactos registrados
**Flujo Principal:**
1. Sensor detecta presencia de gas combustible
2. Sensor envía mensaje de alarma vía MQTT al servidor
3. Sistema recibe y procesa la alarma
4. Sistema identifica el sensor y su ubicación jerárquica
5. Sistema identifica los contactos del cliente asociado
6. Sistema envía notificación por email a todos los contactos registrados
7. Sistema envía notificación por SMS a todos los teléfonos registrados
8. Sistema registra el evento en la base de datos
9. Sistema actualiza el dashboard en tiempo real

**Flujo Alternativo 3a:** Error en procesamiento de alarma
- Sistema reintenta procesamiento (3 intentos)
- Sistema registra error en logs
- Sistema notifica a administradores del sistema

**Postcondición:** Contactos notificados, evento registrado, dashboard actualizado

---

### CU-002: Alta de Cliente

**Actor Principal:** Administrador
**Flujo Principal:**
1. Administrador accede a panel de gestión
2. Administrador selecciona "Crear Nuevo Cliente"
3. Sistema muestra formulario de cliente
4. Administrador ingresa datos:
   - Nombre de la empresa/persona
   - Información de contacto
   - Datos de facturación (opcional)
5. Administrador guarda la información
6. Sistema valida los datos
7. Sistema crea el cliente en la base de datos
8. Sistema muestra confirmación

**Postcondición:** Cliente creado y disponible para asignar edificios

---

### CU-003: Configuración de Sensor

**Actor Principal:** Administrador
**Precondición:** Cliente, Edificio, Apartamento y Ubicación creados
**Flujo Principal:**
1. Administrador selecciona ubicación donde instalar sensor
2. Administrador registra sensor con:
   - ID único del dispositivo
   - Modelo del sensor
   - Fecha de instalación
   - Estado inicial (activo/inactivo)
3. Sistema valida que el ID no esté duplicado
4. Sistema guarda el sensor
5. Sistema configura suscripción MQTT para ese sensor
6. Sistema confirma configuración exitosa

**Postcondición:** Sensor configurado y monitoreado

---

### CU-004: Visualización de Sensores por Edificio

**Actor Principal:** Cliente, Administrador
**Flujo Principal:**
1. Usuario accede al dashboard
2. Usuario selecciona un edificio
3. Sistema recupera todos los apartamentos del edificio
4. Sistema recupera todos los sensores de cada apartamento
5. Sistema muestra vista jerárquica:
   ```
   Edificio ABC
   ├── Apartamento 101
   │   ├── Cocina: Sensor S001 (✓ Normal)
   │   └── Lavadero: Sensor S002 (✓ Normal)
   ├── Apartamento 102
   │   ├── Cocina: Sensor S003 (⚠ Alerta)
   │   └── Sala: Sensor S004 (✓ Normal)
   ```
6. Sistema muestra estado actual de cada sensor
7. Sistema actualiza en tiempo real

**Postcondición:** Usuario visualiza todos los sensores organizados

---

### CU-005: Gestión de Contactos para Notificaciones

**Actor Principal:** Cliente
**Flujo Principal:**
1. Cliente accede a su perfil
2. Cliente selecciona "Gestionar Contactos"
3. Sistema muestra lista actual de contactos
4. Cliente puede:
   - Agregar nuevo contacto (email o teléfono)
   - Editar contacto existente
   - Eliminar contacto
   - Activar/desactivar notificaciones por contacto
5. Sistema valida formato de email/teléfono
6. Sistema guarda cambios
7. Sistema confirma actualización

**Postcondición:** Contactos actualizados para futuras notificaciones

---

## Requisitos Funcionales

### RF-001: Gestión de Usuarios

**Prioridad:** Alta (MVP)

**Descripción:** El sistema debe permitir crear y gestionar dos tipos de usuarios: Administradores y Clientes.

**Criterios de Aceptación:**
- [x] Registro de administradores con email y contraseña
- [x] Registro de clientes con datos completos
- [x] Login con autenticación segura (hash de contraseñas)
- [x] Recuperación de contraseña vía email
- [x] Gestión de sesiones con tokens JWT
- [x] Logout de usuarios
- [x] Diferentes permisos por tipo de usuario

---

### RF-002: Gestión Jerárquica de Ubicaciones

**Prioridad:** Alta (MVP)

**Descripción:** El sistema debe soportar una estructura jerárquica de 4 niveles para organizar sensores.

**Jerarquía:**
```
Cliente
└── Edificio
    └── Apartamento/Unidad
        └── Ubicación (Cocina, Lavadero, Sala, Recámara, etc.)
            └── Sensor
```

**Criterios de Aceptación:**
- [x] CRUD completo para Clientes
- [x] CRUD completo para Edificios (asociados a Cliente)
- [x] CRUD completo para Apartamentos (asociados a Edificio)
- [x] CRUD completo para Ubicaciones (asociadas a Apartamento)
- [x] Ubicaciones predefinidas: Cocina, Lavadero, Sala, Recámara, Baño, Garaje, Otro
- [x] Validación de integridad referencial
- [x] Soft delete para mantener historial

---

### RF-003: Gestión de Sensores

**Prioridad:** Alta (MVP)

**Descripción:** El sistema debe permitir registrar, configurar y monitorear sensores de gas.

**Criterios de Aceptación:**
- [x] Registro de sensor con ID único, modelo, ubicación
- [x] Asignación de sensor a ubicación específica
- [x] Activación/desactivación de sensores
- [x] Estado del sensor: Normal, Alerta, Desconectado, Mantenimiento
- [x] Fecha de instalación y último mantenimiento
- [x] Visualización de estado actual
- [x] Historial de cambios de estado

---

### RF-004: Recepción de Datos MQTT

**Prioridad:** Alta (MVP)

**Descripción:** El sistema debe recibir y procesar mensajes de sensores vía MQTT.

**Especificaciones Técnicas:**
- **Protocolo:** MQTT v3.1.1 o superior
- **QoS:** Nivel 1 (al menos una vez) o 2 (exactamente una vez) para alarmas
- **Estructura de Topics:** `engisensors/{client_id}/{building_id}/{apartment_id}/{sensor_id}/status`
- **Payload:** JSON con estructura definida

**Ejemplo de Mensaje:**
```json
{
  "sensor_id": "S001",
  "timestamp": "2025-11-17T10:30:45Z",
  "status": "alert",
  "gas_level": 850,
  "threshold": 800,
  "battery": 85,
  "signal_strength": -45
}
```

**Criterios de Aceptación:**
- [x] Broker MQTT configurado y seguro
- [x] Autenticación de sensores
- [x] Suscripción dinámica a topics por sensor
- [x] Procesamiento asíncrono de mensajes
- [x] Validación de estructura de mensajes
- [x] Manejo de reconexiones
- [x] Logging de todos los mensajes recibidos

---

### RF-005: Sistema de Notificaciones

**Prioridad:** Alta (MVP)

**Descripción:** El sistema debe enviar notificaciones inmediatas cuando un sensor detecte gas.

**Canales de Notificación:**
1. **Email**
   - Plantilla HTML profesional
   - Información detallada de la alerta
   - Mapa de ubicación (futuro)

2. **SMS**
   - Mensaje corto con información crítica
   - Link a dashboard para más detalles

**Criterios de Aceptación:**
- [x] Envío de email a todos los contactos del cliente
- [x] Envío de SMS a todos los teléfonos del cliente
- [x] Tiempo de envío < 5 segundos desde detección
- [x] Reintentos en caso de fallo (hasta 3 intentos)
- [x] Registro de notificaciones enviadas
- [x] Estado de entrega (enviado, fallido, pendiente)
- [x] No duplicar notificaciones por mismo evento
- [x] Throttling: máximo 1 notificación por sensor cada 5 minutos

---

### RF-006: Dashboard de Monitoreo

**Prioridad:** Alta (MVP)

**Descripción:** Interfaz web para visualizar sensores organizados por edificio.

**Criterios de Aceptación:**
- [x] Vista de lista de edificios del cliente
- [x] Vista expandible por edificio mostrando apartamentos
- [x] Vista expandible por apartamento mostrando ubicaciones y sensores
- [x] Indicadores visuales de estado:
  - Verde: Normal
  - Rojo: Alerta de gas
  - Gris: Desconectado
  - Amarillo: Mantenimiento
- [x] Actualización en tiempo real (WebSockets o polling)
- [x] Filtros por edificio, apartamento, estado
- [x] Búsqueda por ID de sensor
- [x] Responsive design (móvil y desktop)

---

### RF-007: Gestión de Contactos

**Prioridad:** Alta (MVP)

**Descripción:** Los clientes deben poder gestionar sus contactos para notificaciones.

**Criterios de Aceptación:**
- [x] Agregar múltiples emails
- [x] Agregar múltiples teléfonos
- [x] Validación de formato de email
- [x] Validación de formato de teléfono (internacional)
- [x] Activar/desactivar contactos sin eliminar
- [x] Etiquetar contactos (Gerente, Seguridad, Mantenimiento, etc.)
- [x] Contacto principal marcado
- [x] Límite de 10 contactos por cliente (configurable)

---

### RF-008: Historial de Eventos

**Prioridad:** Media (Post-MVP)

**Descripción:** Registro histórico de todas las alertas y eventos del sistema.

**Criterios de Aceptación:**
- [x] Registro de cada detección de gas
- [x] Registro de notificaciones enviadas
- [x] Registro de cambios de estado de sensores
- [x] Filtros por fecha, edificio, sensor, tipo de evento
- [x] Exportación a CSV/PDF
- [x] Retención de 2 años de datos
- [x] Paginación de resultados

---

### RF-009: Reportes

**Prioridad:** Baja (Post-MVP)

**Descripción:** Generación de reportes estadísticos y de cumplimiento.

**Tipos de Reportes:**
- Alertas por período
- Sensores con más incidencias
- Tiempo de respuesta promedio
- Estado de sensores por edificio
- Reporte de mantenimientos

---

### RF-010: Panel de Administración

**Prioridad:** Alta (MVP)

**Descripción:** Panel para administradores del sistema.

**Funcionalidades:**
- Dashboard con métricas globales
- Gestión de todos los clientes
- Configuración de sensores
- Monitoreo de salud del sistema
- Logs de sistema

---

## Requisitos No Funcionales

### RNF-001: Rendimiento

**Prioridad:** Alta

**Requisitos:**
- Tiempo de respuesta API: < 200ms para el 95% de requests
- Tiempo de procesamiento de alarma MQTT: < 1 segundo
- Tiempo de envío de notificación: < 5 segundos desde detección
- Dashboard actualización: < 2 segundos
- Soportar 1000 sensores simultáneos en MVP
- Soportar 100 usuarios concurrentes en MVP

---

### RNF-002: Disponibilidad

**Prioridad:** Crítica

**Requisitos:**
- Uptime: 99.9% (8.76 horas downtime/año máximo)
- Sistema de alertas debe funcionar 24/7/365
- Backup diario automático
- Recovery Time Objective (RTO): < 1 hora
- Recovery Point Objective (RPO): < 15 minutos

---

### RNF-003: Seguridad

**Prioridad:** Crítica

**Requisitos:**
- Autenticación JWT con refresh tokens
- Contraseñas hasheadas con bcrypt (cost factor 12+)
- HTTPS obligatorio para toda comunicación
- MQTT sobre TLS
- Validación de inputs en backend
- Rate limiting en APIs (100 req/min por IP)
- Logs de auditoría para acciones críticas
- Cumplimiento con GDPR/LGPD para datos personales
- Segregación de datos por cliente (multi-tenancy)
- Encriptación de datos sensibles en base de datos

---

### RNF-004: Escalabilidad

**Prioridad:** Alta

**Requisitos:**
- Arquitectura horizontal escalable
- Base de datos optimizada para crecimiento
- Broker MQTT distribuido (cluster)
- Cache distribuido (Redis)
- Cola de mensajes para notificaciones
- Diseño stateless de servicios
- Capacidad de crecer a 10,000+ sensores

---

### RNF-005: Mantenibilidad

**Prioridad:** Media

**Requisitos:**
- Código con cobertura de tests > 80%
- Documentación de APIs (OpenAPI/Swagger)
- Logs estructurados (JSON)
- Monitoreo con métricas (Prometheus/Grafana)
- Despliegue automatizado (CI/CD)
- Versionado semántico de APIs
- Código siguiendo convenciones de CLAUDE.md

---

### RNF-006: Usabilidad

**Prioridad:** Alta

**Requisitos:**
- Interfaz intuitiva (máximo 3 clics para acción común)
- Soporte para español e inglés
- Mensajes de error claros y accionables
- Ayuda contextual en formularios
- Responsive design (móvil, tablet, desktop)
- Compatibilidad con navegadores modernos (últimas 2 versiones)
- Tiempo de aprendizaje < 1 hora para usuario básico

---

### RNF-007: Observabilidad

**Prioridad:** Media

**Requisitos:**
- Logging centralizado
- Métricas de negocio y técnicas
- Alertas proactivas de sistema
- Trazabilidad de requests (correlation IDs)
- Health checks de servicios
- Dashboards de monitoreo

---

## Arquitectura del Sistema

### Stack Tecnológico Propuesto

#### Backend
- **Lenguaje:** Python 3.11+ o Node.js 20+
- **Framework:**
  - Python: FastAPI (async, alto rendimiento)
  - Node.js: NestJS (TypeScript, arquitectura escalable)
- **Base de Datos:**
  - PostgreSQL 15+ (datos relacionales)
  - TimescaleDB (extensión para series temporales)
- **Cache:** Redis 7+ (sesiones, cache, rate limiting)
- **Broker MQTT:**
  - Mosquitto (open source)
  - EMQX (escalable, enterprise-ready)
- **Cola de Mensajes:**
  - RabbitMQ o Redis Streams (notificaciones)

#### Frontend
- **Framework:** React 18+ o Vue 3+
- **UI Library:** Material UI, Ant Design, o Tailwind CSS
- **State Management:** Redux Toolkit, Zustand, o Pinia
- **Real-time:** Socket.io o WebSockets
- **Charts:** Chart.js, Recharts, o Apache ECharts

#### DevOps
- **Containerización:** Docker
- **Orquestación:** Docker Compose (MVP), Kubernetes (producción)
- **CI/CD:** GitHub Actions, GitLab CI, o Jenkins
- **Monitoreo:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Cloud:** AWS, Google Cloud, o Azure

#### Servicios Externos
- **Email:** SendGrid, AWS SES, o Mailgun
- **SMS:** Twilio, AWS SNS, o MessageBird
- **Autenticación (futuro):** Auth0, Firebase Auth

---

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         CAPA DE USUARIOS                         │
├─────────────────────────────────────────────────────────────────┤
│  Web Dashboard        │  Mobile App (futuro)  │  Admin Panel     │
│  (React/Vue)          │                       │  (React/Vue)     │
└────────────┬──────────┴───────────────────────┴──────────────────┘
             │
             │ HTTPS / WSS
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY / LOAD BALANCER                 │
│                         (Nginx / Traefik)                        │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CAPA DE APLICACIÓN                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │  API REST        │  │  WebSocket       │  │  MQTT Handler │ │
│  │  Service         │  │  Service         │  │  Service      │ │
│  │  (FastAPI/       │  │  (Socket.io)     │  │  (Paho/       │ │
│  │   NestJS)        │  │                  │  │   MQTT.js)    │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬───────┘ │
│           │                     │                    │          │
│           └─────────────────────┼────────────────────┘          │
│                                 │                                │
└─────────────────────────────────┼────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Redis      │         │ PostgreSQL + │         │  RabbitMQ    │
│   Cache      │         │  TimescaleDB │         │  Queue       │
│              │         │              │         │              │
└──────────────┘         └──────────────┘         └──────┬───────┘
                                                          │
                                                          ▼
                                                  ┌──────────────┐
                                                  │ Notification │
                                                  │  Service     │
                                                  │              │
                                                  └──────┬───────┘
                                                         │
                                        ┌────────────────┴────────────────┐
                                        │                                 │
                                        ▼                                 ▼
                                ┌──────────────┐                 ┌──────────────┐
                                │  Email API   │                 │   SMS API    │
                                │  (SendGrid)  │                 │   (Twilio)   │
                                └──────────────┘                 └──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE SENSORES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Sensor 1 │  │ Sensor 2 │  │ Sensor 3 │  │ Sensor N │        │
│  │  (MQTT)  │  │  (MQTT)  │  │  (MQTT)  │  │  (MQTT)  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       └─────────────┴─────────────┴─────────────┘               │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │
                           ▼
                  ┌──────────────┐
                  │ MQTT Broker  │
                  │  (Mosquitto/ │
                  │    EMQX)     │
                  └──────────────┘
```

---

### Flujo de Datos: Detección de Fuga

```
1. Sensor detecta gas
   │
   ▼
2. Sensor publica mensaje MQTT
   Topic: engisensors/client-001/building-01/apt-101/sensor-s001/alert
   Payload: {"status": "alert", "gas_level": 850, "timestamp": "..."}
   │
   ▼
3. MQTT Broker recibe mensaje
   │
   ▼
4. MQTT Handler Service (suscrito al topic) procesa mensaje
   - Valida estructura
   - Identifica sensor en base de datos
   - Registra evento
   │
   ▼
5. Event Handler detecta cambio de estado a "alert"
   - Publica mensaje en cola RabbitMQ (topic: notifications.alert)
   │
   ▼
6. Notification Service consume mensaje
   - Obtiene contactos del cliente
   - Genera contenido de email y SMS
   - Envía a proveedores externos
   - Registra notificaciones enviadas
   │
   ▼
7. WebSocket Service envía actualización a clientes conectados
   - Dashboard se actualiza en tiempo real
   │
   ▼
8. Cliente recibe notificaciones y visualiza alerta en dashboard
```

---

## Modelo de Datos

### Diagrama Entidad-Relación

```
┌──────────────┐
│ Users        │
├──────────────┤
│ id (PK)      │
│ email        │
│ password_hash│
│ role         │◄─┐
│ created_at   │  │
└──────────────┘  │
                  │
┌──────────────┐  │
│ Clients      │  │
├──────────────┤  │
│ id (PK)      │  │
│ user_id (FK) │──┘
│ company_name │
│ address      │
│ created_at   │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│ Buildings    │
├──────────────┤
│ id (PK)      │
│ client_id(FK)│
│ name         │
│ address      │
│ city         │
│ country      │
│ created_at   │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│ Apartments   │
├──────────────┤
│ id (PK)      │
│ building_id  │
│ number       │
│ floor        │
│ description  │
│ created_at   │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│ Locations    │
├──────────────┤
│ id (PK)      │
│ apartment_id │
│ location_type│ (cocina, lavadero, sala, recámara, etc.)
│ description  │
│ created_at   │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐         ┌──────────────┐
│ Sensors      │         │ Sensor       │
├──────────────┤         │ Events       │
│ id (PK)      │         ├──────────────┤
│ location_id  │         │ id (PK)      │
│ device_id    │◄────────│ sensor_id(FK)│
│ model        │       1:N│ event_type   │
│ status       │         │ gas_level    │
│ installed_at │         │ battery      │
│ last_seen    │         │ timestamp    │
└──────────────┘         └──────────────┘

┌──────────────┐         ┌──────────────┐
│ Contacts     │         │ Notifications│
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ client_id(FK)│◄────────│ contact_id   │
│ type         │       1:N│ event_id(FK) │
│ value        │         │ channel      │ (email/sms)
│ label        │         │ status       │ (sent/failed/pending)
│ is_active    │         │ sent_at      │
│ created_at   │         └──────────────┘
└──────────────┘
```

### Esquemas de Base de Datos

#### Tabla: users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'client')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

#### Tabla: clients
```sql
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    tax_id VARCHAR(50),
    address TEXT,
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_clients_user_id ON clients(user_id);
```

#### Tabla: buildings
```sql
CREATE TABLE buildings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_buildings_client_id ON buildings(client_id);
```

#### Tabla: apartments
```sql
CREATE TABLE apartments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    building_id UUID NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
    number VARCHAR(50) NOT NULL,
    floor INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(building_id, number)
);

CREATE INDEX idx_apartments_building_id ON apartments(building_id);
```

#### Tabla: locations
```sql
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apartment_id UUID NOT NULL REFERENCES apartments(id) ON DELETE CASCADE,
    location_type VARCHAR(50) NOT NULL CHECK (
        location_type IN (
            'cocina', 'lavadero', 'sala', 'recamara',
            'baño', 'garaje', 'bodega', 'pasillo', 'otro'
        )
    ),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_locations_apartment_id ON locations(apartment_id);
```

#### Tabla: sensors
```sql
CREATE TABLE sensors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    device_id VARCHAR(100) UNIQUE NOT NULL,
    model VARCHAR(100),
    firmware_version VARCHAR(50),
    status VARCHAR(50) NOT NULL DEFAULT 'active' CHECK (
        status IN ('active', 'inactive', 'alert', 'maintenance', 'disconnected')
    ),
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_maintenance TIMESTAMP,
    last_seen TIMESTAMP,
    battery_level INTEGER CHECK (battery_level BETWEEN 0 AND 100),
    signal_strength INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_sensors_location_id ON sensors(location_id);
CREATE INDEX idx_sensors_device_id ON sensors(device_id);
CREATE INDEX idx_sensors_status ON sensors(status);
```

#### Tabla: sensor_events (TimescaleDB)
```sql
CREATE TABLE sensor_events (
    id UUID DEFAULT gen_random_uuid(),
    sensor_id UUID NOT NULL REFERENCES sensors(id),
    event_type VARCHAR(50) NOT NULL CHECK (
        event_type IN ('normal', 'alert', 'warning', 'offline', 'online')
    ),
    gas_level INTEGER,
    threshold INTEGER,
    battery_level INTEGER,
    signal_strength INTEGER,
    raw_data JSONB,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, timestamp)
);

-- Convertir a hypertable de TimescaleDB
SELECT create_hypertable('sensor_events', 'timestamp');

CREATE INDEX idx_sensor_events_sensor_id ON sensor_events(sensor_id, timestamp DESC);
CREATE INDEX idx_sensor_events_type ON sensor_events(event_type, timestamp DESC);
```

#### Tabla: contacts
```sql
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('email', 'phone')),
    value VARCHAR(255) NOT NULL,
    label VARCHAR(100),
    is_primary BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contacts_client_id ON contacts(client_id);
CREATE INDEX idx_contacts_type ON contacts(type);
```

#### Tabla: notifications
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES sensor_events(id),
    contact_id UUID NOT NULL REFERENCES contacts(id),
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('email', 'sms')),
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (
        status IN ('pending', 'sent', 'failed', 'delivered')
    ),
    message_id VARCHAR(255),
    error_message TEXT,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_event_id ON notifications(event_id);
CREATE INDEX idx_notifications_contact_id ON notifications(contact_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
```

---

## Interfaces de Usuario

### Wireframes y Flujos

#### 1. Login
```
┌─────────────────────────────────────┐
│         EngiSensors Logo            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Email                         │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │ Contraseña                    │ │
│  └───────────────────────────────┘ │
│                                     │
│  [ ✓ Recordarme ]                  │
│                                     │
│  ┌───────────────────────────────┐ │
│  │       Iniciar Sesión          │ │
│  └───────────────────────────────┘ │
│                                     │
│  ¿Olvidaste tu contraseña?         │
└─────────────────────────────────────┘
```

#### 2. Dashboard Principal (Cliente)
```
┌────────────────────────────────────────────────────────────┐
│  EngiSensors │ [Edificios] [Sensores] [Historial] [Perfil] │ [Logout]
├────────────────────────────────────────────────────────────┤
│  Dashboard > Mis Edificios                                  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 🔍 Buscar edificio...              [+ Nuevo Edificio]│  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 🏢 Edificio Torre Central                            │  │
│  │ 📍 Av. Principal 123, CDMX                           │  │
│  │ ✓ 12 sensores normales  ⚠ 1 alerta  ⚫ 0 desconectados│  │
│  │                                                       │  │
│  │  [Ver Detalles]  [Ver Historial]                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 🏢 Residencial Las Palmas                            │  │
│  │ 📍 Calle Secundaria 456, CDMX                        │  │
│  │ ✓ 8 sensores normales  ⚠ 0 alertas  ⚫ 1 desconectado │  │
│  │                                                       │  │
│  │  [Ver Detalles]  [Ver Historial]                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

#### 3. Vista Detalle de Edificio
```
┌────────────────────────────────────────────────────────────┐
│  Dashboard > Torre Central                                  │
│                                                              │
│  🏢 Torre Central                        Última act: 10:45  │
│  📍 Av. Principal 123, CDMX                                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 📊 Resumen                                            │  │
│  │ ✓ Normal: 12    ⚠ Alerta: 1    ⚫ Offline: 0        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ▼ Apartamento 101                              Floor 1│  │
│  │   ├─ 🍳 Cocina: Sensor S001          ✓ Normal        │  │
│  │   ├─ 🧺 Lavadero: Sensor S002        ✓ Normal        │  │
│  │   └─ 🛋️ Sala: Sensor S003            ⚠ ALERTA       │  │
│  │      Gas detectado: 850 ppm                           │  │
│  │      Última lectura: 10:42                            │  │
│  │      [Ver detalles] [Silenciar]                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ▼ Apartamento 102                              Floor 1│  │
│  │   ├─ 🍳 Cocina: Sensor S004          ✓ Normal        │  │
│  │   └─ 🧺 Lavadero: Sensor S005        ✓ Normal        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

#### 4. Gestión de Contactos
```
┌────────────────────────────────────────────────────────────┐
│  Perfil > Contactos para Notificaciones                     │
│                                                              │
│  Estos contactos recibirán notificaciones de alertas       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 📧 Emails                            [+ Agregar Email]│  │
│  │                                                       │  │
│  │  ✓ gerencia@empresa.com    [Principal] [Editar] [❌] │  │
│  │  ✓ seguridad@empresa.com              [Editar] [❌]  │  │
│  │  ⚪ info@empresa.com (Desactivado)     [Editar] [❌]  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 📱 Teléfonos                      [+ Agregar Teléfono]│  │
│  │                                                       │  │
│  │  ✓ +52 55 1234 5678   [Principal] [Editar] [❌]      │  │
│  │  ✓ +52 55 8765 4321              [Editar] [❌]       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  💡 Consejo: Mantén al menos 2 contactos activos           │
└────────────────────────────────────────────────────────────┘
```

#### 5. Panel de Administración
```
┌────────────────────────────────────────────────────────────┐
│  Admin Panel > Dashboard                                    │
│                                                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐ │
│  │ Clientes   │ │ Edificios  │ │ Sensores   │ │ Alertas │ │
│  │    45      │ │    123     │ │    1,245   │ │   12    │ │
│  └────────────┘ └────────────┘ └────────────┘ └─────────┘ │
│                                                              │
│  📊 Alertas Últimas 24h                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ [Gráfico de barras]                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  🔴 Alertas Recientes                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 10:42 │ Torre Central - Apt 101 - Sala │ Cliente ABC │  │
│  │ 09:15 │ Residencial XYZ - Apt 205      │ Cliente DEF │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  [Ver Todos los Clientes] [Configuración del Sistema]      │
└────────────────────────────────────────────────────────────┘
```

---

## Plan de Desarrollo MVP

### Fase 1: Fundación (Semanas 1-2)

**Objetivos:** Configurar infraestructura básica y autenticación

**Tareas:**
- [ ] Configurar repositorio y CI/CD
- [ ] Setup base de datos PostgreSQL + TimescaleDB
- [ ] Setup Redis
- [ ] Implementar API base (FastAPI/NestJS)
- [ ] Sistema de autenticación JWT
- [ ] Crear modelos de datos
- [ ] Migraciones de base de datos
- [ ] Tests unitarios de autenticación
- [ ] Documentación OpenAPI

**Entregables:**
- API funcional con login/logout
- Base de datos configurada
- Tests pasando
- Documentación inicial

---

### Fase 2: Gestión de Datos (Semanas 3-4)

**Objetivos:** CRUD completo para jerarquía de ubicaciones

**Tareas:**
- [ ] Endpoints CRUD para Clientes
- [ ] Endpoints CRUD para Edificios
- [ ] Endpoints CRUD para Apartamentos
- [ ] Endpoints CRUD para Ubicaciones
- [ ] Endpoints CRUD para Sensores
- [ ] Endpoints CRUD para Contactos
- [ ] Validaciones de integridad
- [ ] Tests de integración
- [ ] Permisos por rol (admin vs cliente)

**Entregables:**
- APIs RESTful completas
- Validación de permisos
- Tests > 80% coverage
- Documentación actualizada

---

### Fase 3: Comunicación MQTT (Semanas 5-6)

**Objetivos:** Recepción y procesamiento de datos de sensores

**Tareas:**
- [ ] Configurar broker MQTT (Mosquitto/EMQX)
- [ ] Implementar MQTT Handler Service
- [ ] Definir estructura de topics
- [ ] Definir estructura de mensajes (JSON schema)
- [ ] Procesamiento de mensajes
- [ ] Registro de eventos en TimescaleDB
- [ ] Detección de cambios de estado
- [ ] Tests con sensores simulados
- [ ] Monitoreo de conexiones MQTT

**Entregables:**
- Broker MQTT funcionando
- Servicio procesando mensajes
- Eventos registrados en BD
- Simulador de sensores para testing

---

### Fase 4: Sistema de Notificaciones (Semana 7)

**Objetivos:** Envío de alertas por email y SMS

**Tareas:**
- [ ] Integrar SendGrid/SES para emails
- [ ] Integrar Twilio para SMS
- [ ] Crear plantillas de email
- [ ] Crear plantillas de SMS
- [ ] Implementar cola de notificaciones (RabbitMQ)
- [ ] Notification Service consumidor
- [ ] Lógica de throttling
- [ ] Registro de notificaciones enviadas
- [ ] Tests de envío
- [ ] Manejo de errores y reintentos

**Entregables:**
- Notificaciones funcionando
- Plantillas profesionales
- Sistema de reintentos
- Logs de notificaciones

---

### Fase 5: Frontend - Dashboard (Semanas 8-10)

**Objetivos:** Interfaz web funcional para clientes y administradores

**Tareas Cliente:**
- [ ] Setup proyecto React/Vue
- [ ] Sistema de autenticación
- [ ] Vista de lista de edificios
- [ ] Vista detalle de edificio con sensores
- [ ] Gestión de contactos
- [ ] Visualización de estados en tiempo real
- [ ] Responsive design
- [ ] Tests E2E (Cypress/Playwright)

**Tareas Admin:**
- [ ] Panel de administración
- [ ] CRUD de clientes
- [ ] CRUD de edificios/apartamentos
- [ ] CRUD de sensores
- [ ] Dashboard con métricas
- [ ] Vista de alertas recientes

**Entregables:**
- Dashboard funcional
- Responsive
- Integrado con backend
- Tests E2E pasando

---

### Fase 6: Real-time & WebSockets (Semana 11)

**Objetivos:** Actualización en tiempo real del dashboard

**Tareas:**
- [ ] Implementar WebSocket server
- [ ] Integrar Socket.io en frontend
- [ ] Publicar eventos de sensores a clientes conectados
- [ ] Actualización automática de dashboard
- [ ] Manejo de reconexiones
- [ ] Tests de comunicación real-time

**Entregables:**
- Dashboard actualizando en tiempo real
- Reconexión automática
- UX fluida

---

### Fase 7: Testing & Refinamiento (Semana 12)

**Objetivos:** Asegurar calidad y preparar para producción

**Tareas:**
- [ ] Tests de carga (JMeter/k6)
- [ ] Tests de seguridad (OWASP ZAP)
- [ ] Auditoría de código
- [ ] Optimización de queries
- [ ] Configurar monitoreo (Prometheus/Grafana)
- [ ] Configurar logging centralizado
- [ ] Documentación completa
- [ ] Video demo
- [ ] Plan de deployment

**Entregables:**
- Sistema probado y optimizado
- Documentación completa
- Ready para producción

---

### Fase 8: Deployment & Launch (Semana 13)

**Objetivos:** Lanzamiento del MVP

**Tareas:**
- [ ] Setup entorno de producción (AWS/GCP/Azure)
- [ ] Configurar dominio y SSL
- [ ] Deploy de servicios
- [ ] Configurar backups automáticos
- [ ] Configurar alertas de sistema
- [ ] Onboarding de primeros clientes piloto
- [ ] Monitoreo 24/7
- [ ] Hotfixes si necesario

**Entregables:**
- Sistema en producción
- Primeros clientes activos
- Monitoreo activo

---

## Roadmap

### Post-MVP (3-6 meses)

**Funcionalidades Planeadas:**
- [ ] App móvil nativa (iOS/Android)
- [ ] Mapas interactivos con ubicación de sensores
- [ ] Gráficos históricos de lecturas
- [ ] Exportación de reportes PDF
- [ ] Integración con sistemas de emergencia (bomberos, 911)
- [ ] Alertas por WhatsApp
- [ ] Dashboard predictivo con ML (detección de patrones)
- [ ] Multi-idioma completo
- [ ] API pública para integraciones

### Mejoras Técnicas
- [ ] Kubernetes para orquestación
- [ ] Multi-región para alta disponibilidad
- [ ] CDN para assets estáticos
- [ ] WebRTC para comunicación de emergencia
- [ ] Blockchain para trazabilidad de eventos críticos

---

## Métricas de Éxito

### Métricas de Producto

**Adopción:**
- Número de clientes activos
- Número de sensores monitoreados
- Número de edificios gestionados
- Usuarios activos mensuales (MAU)

**Engagement:**
- Frecuencia de login
- Tiempo promedio en plataforma
- Acciones por sesión

**Confiabilidad:**
- Tiempo de detección a notificación (target: < 5s)
- Tasa de entrega de notificaciones (target: > 99%)
- Uptime del sistema (target: > 99.9%)

**Satisfacción:**
- NPS (Net Promoter Score)
- CSAT (Customer Satisfaction)
- Tasa de retención

### Métricas Técnicas

**Performance:**
- Latencia API P95 < 200ms
- Tiempo de procesamiento MQTT < 1s
- Throughput: mensajes procesados/segundo

**Disponibilidad:**
- Uptime mensual
- Mean Time To Recovery (MTTR)
- Mean Time Between Failures (MTBF)

**Calidad:**
- Code coverage > 80%
- Bugs críticos en producción (target: 0)
- Vulnerabilidades de seguridad (target: 0)

---

## Riesgos y Mitigación

### Riesgos Técnicos

**Riesgo: Pérdida de mensajes MQTT**
- **Impacto:** Alto - alertas críticas no llegarían
- **Probabilidad:** Media
- **Mitigación:**
  - Usar QoS 2 (exactly once) para mensajes de alerta
  - Implementar acknowledgments
  - Logging exhaustivo
  - Monitoreo de mensajes perdidos
  - Fallback: sensores reenvían si no reciben ACK

**Riesgo: Fallas en envío de notificaciones**
- **Impacto:** Crítico
- **Probabilidad:** Media
- **Mitigación:**
  - Sistema de reintentos (hasta 3 intentos)
  - Múltiples proveedores (fallback)
  - Queue persistente
  - Alertas a administradores si falla
  - Monitoreo de tasa de entrega

**Riesgo: Escalabilidad - demasiados sensores**
- **Impacto:** Alto
- **Probabilidad:** Baja en MVP, Alta en crecimiento
- **Mitigación:**
  - Arquitectura stateless horizontal
  - Load balancing
  - Sharding de base de datos
  - Cache agresivo
  - Tests de carga desde el principio

**Riesgo: Seguridad - acceso no autorizado**
- **Impacto:** Crítico
- **Probabilidad:** Media
- **Mitigación:**
  - Autenticación robusta (JWT)
  - Rate limiting
  - Auditoría de accesos
  - Penetration testing
  - Cumplimiento OWASP

### Riesgos de Negocio

**Riesgo: Baja adopción**
- **Impacto:** Alto
- **Mitigación:**
  - Programa piloto con clientes clave
  - Onboarding simplificado
  - Soporte 24/7 inicial
  - Pricing competitivo

**Riesgo: Competencia**
- **Impacto:** Medio
- **Mitigación:**
  - Diferenciación por UX
  - Pricing flexible
  - Integración con ecosistemas locales
  - Innovación continua

**Riesgo: Regulatorio**
- **Impacto:** Alto
- **Mitigación:**
  - Consultoría legal
  - Cumplimiento de normativas locales
  - Certificaciones de seguridad
  - GDPR/LGPD compliance

---

## Apéndices

### Glosario

- **Cliente:** Organización o individuo que posee edificios con sensores
- **Edificio:** Propiedad donde se instalan sensores
- **Apartamento:** Unidad dentro de un edificio
- **Ubicación:** Espacio específico dentro de un apartamento
- **Sensor:** Dispositivo IoT que detecta gas combustible
- **Alerta:** Notificación generada cuando un sensor detecta gas
- **MQTT:** Protocolo de mensajería ligero para IoT
- **QoS:** Quality of Service en MQTT
- **Threshold:** Valor umbral de gas para disparar alerta

### Referencias

- [MQTT Specification](https://mqtt.org/mqtt-specification/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [TimescaleDB Documentation](https://docs.timescale.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Best Practices](https://react.dev/)

### Contacto

**Product Owner:** [Nombre]
**Tech Lead:** [Nombre]
**Email:** [email]

---

**Última Actualización:** 2025-11-17
**Próxima Revisión:** Cada 2 semanas durante desarrollo MVP
