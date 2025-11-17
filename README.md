# EngiSensors

**Plataforma IoT de Monitoreo de Gas Combustible para Seguridad Residencial e Industrial**

[![Status](https://img.shields.io/badge/status-MVP%20in%20planning-yellow)]()
[![License](https://img.shields.io/badge/license-TBD-blue)]()

---

## 🎯 Resumen

EngiSensors es una plataforma de monitoreo en tiempo real para sensores de gas combustible desplegados en domicilios e industrias. El sistema recibe datos de sensores IoT vía MQTT y envía alertas inmediatas por email y SMS cuando detecta fugas de gas, ayudando a prevenir accidentes, explosiones e intoxicaciones.

### Características Principales

- 🚨 **Detección en Tiempo Real** - Monitoreo 24/7 de sensores de gas combustible
- 📱 **Alertas Multicanal** - Notificaciones por email y SMS en < 5 segundos
- 🏢 **Gestión Jerárquica** - Organización por Cliente → Edificio → Apartamento → Ubicación → Sensor
- 📊 **Dashboard en Vivo** - Interfaz web con actualizaciones en tiempo real
- 👥 **Multi-tenant** - Soporte para múltiples clientes con segregación de datos
- 🔐 **Seguro** - Autenticación JWT, encriptación, validación de inputs

---

## 📋 Estado del Proyecto

**Fase Actual:** Planificación MVP

- [x] Product Requirements Document (PRD)
- [x] Guías para AI Assistants (CLAUDE.md)
- [ ] Arquitectura técnica detallada
- [ ] Implementación backend
- [ ] Implementación frontend
- [ ] Sistema de notificaciones
- [ ] Integración MQTT
- [ ] Testing y QA
- [ ] Deployment

**Timeline MVP:** 13 semanas (ver [PRD.md](PRD.md) para plan detallado)

---

## 🏗️ Arquitectura

```
Sensores IoT (Gas) → MQTT Broker → Backend Services → Base de Datos
                                          ↓
                                   Notification Service
                                          ↓
                              Email / SMS Providers

                                    WebSocket
                                          ↓
                                   Web Dashboard
```

### Stack Tecnológico (Propuesto)

**Backend:**
- Python 3.11+ con FastAPI (o Node.js 20+ con NestJS)
- PostgreSQL 15+ con TimescaleDB
- Redis 7+ para cache
- MQTT (Mosquitto/EMQX)
- RabbitMQ para colas

**Frontend:**
- React 18+ o Vue 3+
- Socket.io para tiempo real
- Material UI / Tailwind CSS

**DevOps:**
- Docker + Docker Compose
- GitHub Actions CI/CD
- Prometheus + Grafana

---

## 📚 Documentación

### Para Desarrolladores
- **[PRD.md](PRD.md)** - Product Requirements Document completo
  - Casos de uso y requisitos funcionales
  - Arquitectura del sistema
  - Modelo de datos (schemas SQL incluidos)
  - Wireframes de UI
  - Plan de desarrollo MVP
  - Roadmap y métricas de éxito

### Para AI Assistants
- **[CLAUDE.md](CLAUDE.md)** - Guía completa para asistentes de IA
  - Convenciones de código
  - Patrones específicos de gas detection
  - Workflows de desarrollo
  - Testing guidelines
  - Troubleshooting común

---

## 🚀 Quick Start

*En desarrollo - instrucciones completas se agregarán durante la implementación*

### Requisitos Previos
```bash
# Versiones recomendadas
Python >= 3.11  o  Node.js >= 20
PostgreSQL >= 15
Redis >= 7
Docker >= 20.10
```

### Instalación (Futura)
```bash
# Clonar repositorio
git clone https://github.com/federicoarg00/engisensors_claudecode.git
cd engisensors_claudecode

# Backend setup
cd src/backend
pip install -r requirements.txt  # o npm install

# Base de datos setup
docker-compose up -d postgres redis mqtt

# Ejecutar migraciones
alembic upgrade head  # o npm run migrate

# Iniciar servicios
docker-compose up
```

---

## 🔧 Jerarquía de Datos

```
Cliente (Empresa/Persona)
└── Edificio (Propiedad física)
    └── Apartamento (Unidad habitacional)
        └── Ubicación (Cocina, Lavadero, Sala, Recámara, etc.)
            └── Sensor (Dispositivo IoT)
```

### Ejemplo MQTT Message

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

**Topic:** `engisensors/{client_id}/{building_id}/{apartment_id}/{sensor_id}/status`

---

## 🎨 Funcionalidades MVP

### Para Administradores
- ✅ Gestión de clientes, edificios, apartamentos y sensores
- ✅ Dashboard global con métricas del sistema
- ✅ Configuración de umbrales de alerta
- ✅ Monitoreo de salud del sistema

### Para Clientes
- ✅ Visualización de sensores organizados por edificio
- ✅ Monitoreo en tiempo real del estado de sensores
- ✅ Gestión de contactos para notificaciones
- ✅ Recepción de alertas por email y SMS
- ✅ Historial de eventos de detección

---

## 🔐 Seguridad

- **Autenticación:** JWT con refresh tokens
- **Autorización:** Role-based (admin/client) con segregación de datos
- **Encriptación:** HTTPS/TLS, MQTT over TLS
- **Validación:** Pydantic models, sanitización de inputs
- **Auditoría:** Logs de todas las acciones críticas
- **Cumplimiento:** Diseñado para GDPR/LGPD

---

## 📊 Métricas de Éxito

**Confiabilidad:**
- ⏱️ Tiempo de detección a notificación: < 5 segundos
- ✅ Tasa de entrega de notificaciones: > 99%
- 🔄 Uptime del sistema: > 99.9%

**Performance:**
- ⚡ Latencia API P95: < 200ms
- 📡 Procesamiento MQTT: < 1 segundo
- 🏃 Soporte: 1,000+ sensores simultáneos (MVP)

---

## 🤝 Contribuyendo

Este proyecto sigue estándares estrictos de calidad y seguridad. Antes de contribuir:

1. Lee [CLAUDE.md](CLAUDE.md) para convenciones de código
2. Revisa [PRD.md](PRD.md) para entender requisitos
3. Crea un branch desde `main`: `git checkout -b feature/descripcion`
4. Escribe tests (coverage > 80%)
5. Asegura que pasan todos los tests
6. Crea un Pull Request con descripción clara

### Commit Message Format
```
<type>(<scope>): <subject>

feat(sensors): add gas threshold configuration
fix(notifications): handle SMS delivery failures
docs(api): update endpoint documentation
```

---

## 📖 Recursos Adicionales

**Protocolo MQTT:**
- [MQTT Specification](https://mqtt.org/mqtt-specification/)
- [MQTT Essentials Guide](https://www.hivemq.com/mqtt-essentials/)

**Frameworks:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TimescaleDB Docs](https://docs.timescale.com/)

**Seguridad:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [IoT Security Best Practices](https://owasp.org/www-project-internet-of-things/)

---

## 📧 Contacto

**Project Owner:** [TBD]
**Tech Lead:** [TBD]
**Email:** [TBD]

---

## 📄 Licencia

*Licencia por determinar*

---

**⚠️ Nota de Seguridad:**
Este es un sistema de seguridad crítico. Toda contribución debe pasar por revisión rigurosa de código y testing exhaustivo antes de deployment.

**Last Updated:** 2025-11-17
