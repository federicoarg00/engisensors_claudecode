# EngiSensors Quick Start Guide

Guía rápida para comenzar a desarrollar con EngiSensors.

## 🚀 Inicio Rápido (5 minutos)

### 1. Clonar y Configurar

```bash
# Clonar repositorio
git clone https://github.com/federicoarg00/engisensors_claudecode.git
cd engisensors_claudecode

# Crear archivo de configuración
cp .env.example .env

# Editar .env con tus valores
nano .env  # o tu editor preferido
```

### 2. Configurar Variables de Entorno

Edita `.env` y configura al menos estas variables:

```bash
# Obligatorias
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-jwt-secret-aqui
MQTT_BROKER_HOST=www.trustcapsupes.com
MQTT_BROKER_PORT=1883

# Opcional (si el broker MQTT requiere autenticación)
MQTT_BROKER_USERNAME=tu-usuario
MQTT_BROKER_PASSWORD=tu-password
```

### 3. Iniciar con Docker

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs del backend
docker-compose logs -f backend

# Verificar que todo está funcionando
curl http://localhost:8000/health
curl http://localhost:8000/health/mqtt
```

### 4. Acceder a la Aplicación

- **API Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **MQTT Status:** http://localhost:8000/health/mqtt
- **pgAdmin (opcional):** http://localhost:5050

## 📡 Probar Conexión MQTT

### Verificar Recepción de Mensajes

1. **Observar logs del backend:**
   ```bash
   docker-compose logs -f backend
   ```

2. **Enviar mensaje de prueba** desde otro terminal:
   ```bash
   mosquitto_pub -h www.trustcapsupes.com -p 1883 \
     -t "engisensors/test/building1/apt101/S001/status" \
     -m '{"sensor_id":"S001","timestamp":"2025-11-17T10:30:00Z","status":"normal","gas_level":100,"threshold":800,"battery":95,"signal_strength":-40}'
   ```

3. **Verificar en logs** que el mensaje fue recibido y procesado.

### Enviar Alerta de Prueba

```bash
mosquitto_pub -h www.trustcapsupes.com -p 1883 \
  -t "engisensors/test/building1/apt101/S001/status" \
  -m '{"sensor_id":"S001","timestamp":"2025-11-17T10:35:00Z","status":"alert","gas_level":950,"threshold":800,"battery":95,"signal_strength":-40}'
```

Deberías ver en los logs:
```
🚨 GAS ALERT! Sensor S001 detected 950 PPM (threshold: 800)
```

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar un servicio específico
docker-compose restart backend

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Reconstruir imágenes
docker-compose build

# Limpiar todo (⚠️ elimina volúmenes)
docker-compose down -v
```

### Desarrollo Local (Sin Docker)

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
cd src/backend
pip install -r requirements.txt

# Ejecutar aplicación
python -m app.main

# O con uvicorn y hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Base de Datos

```bash
# Conectar a PostgreSQL
docker-compose exec postgres psql -U engisensors -d engisensors

# Backup
docker-compose exec postgres pg_dump -U engisensors engisensors > backup.sql

# Restore
cat backup.sql | docker-compose exec -T postgres psql -U engisensors engisensors
```

## 📂 Estructura del Proyecto

```
engisensors_claudecode/
├── src/
│   └── backend/           # ✅ Backend API (FastAPI)
│       ├── app/
│       │   ├── main.py    # ✅ Punto de entrada
│       │   ├── config.py  # ✅ Configuración
│       │   └── services/
│       │       └── mqtt_handler.py  # ✅ Servicio MQTT
│       ├── requirements.txt  # ✅ Dependencias Python
│       └── Dockerfile     # ✅ Imagen Docker
├── docker-compose.yml     # ✅ Orquestación servicios
├── .env.example          # ✅ Plantilla configuración
├── PRD.md                # ✅ Especificación producto
├── CLAUDE.md             # ✅ Guía desarrollo
└── README.md             # ✅ Documentación principal
```

## ✅ Estado Actual

### Implementado
- ✅ Estructura del proyecto
- ✅ Configuración FastAPI
- ✅ Servicio MQTT conectado a www.trustcapsupes.com
- ✅ Validación de mensajes de sensores
- ✅ Logging estructurado
- ✅ Docker Compose para desarrollo
- ✅ Dockerfile para producción (Coolify)
- ✅ Health checks

### Pendiente
- ⏳ Modelos de base de datos
- ⏳ Migraciones con Alembic
- ⏳ APIs REST (auth, clientes, sensores, etc.)
- ⏳ Sistema de notificaciones (email/SMS)
- ⏳ WebSocket para tiempo real
- ⏳ Frontend
- ⏳ Tests automatizados

## 🐛 Troubleshooting

### MQTT no conecta

**Síntoma:** Logs muestran "Failed to connect to MQTT broker"

**Solución:**
1. Verificar que www.trustcapsupes.com es accesible:
   ```bash
   ping www.trustcapsupes.com
   telnet www.trustcapsupes.com 1883
   ```

2. Verificar credenciales en `.env` si el broker requiere autenticación

3. Revisar firewall/VPN

### Base de datos no conecta

**Síntoma:** Backend no puede conectar a PostgreSQL

**Solución:**
1. Verificar PostgreSQL está corriendo:
   ```bash
   docker-compose ps postgres
   ```

2. Verificar DATABASE_URL en `.env`

3. Reiniciar servicios:
   ```bash
   docker-compose restart postgres backend
   ```

### Puerto 8000 ya en uso

**Síntoma:** "Error: Port 8000 is already in use"

**Solución:**
```bash
# Encontrar proceso usando puerto 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Matar proceso o cambiar puerto en docker-compose.yml
```

## 📚 Siguientes Pasos

1. **Leer documentación:**
   - [PRD.md](PRD.md) - Especificación completa del producto
   - [CLAUDE.md](CLAUDE.md) - Guías de desarrollo
   - [src/backend/README.md](src/backend/README.md) - Documentación del backend

2. **Implementar base de datos:**
   - Crear modelos SQLAlchemy
   - Configurar Alembic
   - Ejecutar migraciones

3. **Implementar APIs:**
   - Autenticación (JWT)
   - CRUD de clientes, edificios, sensores
   - Gestión de contactos

4. **Configurar notificaciones:**
   - Integrar SendGrid (email)
   - Integrar Twilio (SMS)
   - Implementar sistema de alertas

5. **Deploy a Coolify:**
   - Configurar proyecto en Coolify
   - Agregar variables de entorno
   - Deployar a producción

## 📞 Soporte

- **Issues:** GitHub Issues
- **Documentación:** Ver archivos .md en el repositorio
- **Logs:** `docker-compose logs -f`

---

**Happy Coding! 🚀**
