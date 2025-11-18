# 🎨 Dashboard Demo - EngiSensors

## Vista Previa del Dashboard

He creado una representación visual completa del dashboard de EngiSensors que puedes abrir directamente en tu navegador.

## 🚀 Cómo Ver el Demo

### Opción 1: Abrir Directamente en Navegador

```bash
# Desde la raíz del proyecto
open demo-dashboard.html

# O en Linux
xdg-open demo-dashboard.html

# O en Windows
start demo-dashboard.html
```

### Opción 2: Con un Servidor Local

Si quieres servir el archivo con un servidor HTTP:

```bash
# Python
python -m http.server 8080

# Node.js (si tienes http-server instalado)
npx http-server -p 8080

# Luego abre: http://localhost:8080/demo-dashboard.html
```

## 📱 Vista Previa

El demo incluye:

### 1. **Header & Navegación**
- Logo y título de EngiSensors
- Navegación principal (Dashboard, Edificios, Sensores, Contactos, Reportes, Configuración)
- Gradiente morado distintivo

### 2. **Banner de Alerta**
- Se muestra cuando hay alertas activas
- Fondo rojo con animación
- Información de la alerta en tiempo real
- Icono animado de alerta

### 3. **Estadísticas Generales**
- 4 tarjetas con métricas clave:
  - ✅ Sensores normales
  - 🚨 Alertas activas
  - ⚠️ Batería baja
  - 🏢 Edificios activos

### 4. **Tarjetas de Edificios**
- Vista expandible/colapsable
- Estadísticas por edificio
- Dirección y ubicación

### 5. **Vista de Apartamentos**
- Organización por apartamentos
- Número de apartamento y piso

### 6. **Tarjetas de Sensores**
Cada sensor muestra:
- 📍 **Ubicación:** Cocina, Lavadero, Sala, etc. con iconos
- 🎯 **Estado:** Normal, Alerta, Offline
- 📊 **Nivel de Gas:** En PPM (parts per million)
- ⚙️ **Umbral:** Configurado por sensor
- 🔋 **Batería:** Con indicador visual
- 📡 **Señal:** Fuerza de la señal en dBm
- 🆔 **ID del sensor**
- ⏰ **Última actualización:** Tiempo relativo

### 7. **Características Interactivas**
- **Animaciones de alerta:** Parpadeo en sensores con alerta
- **Colores por estado:** Verde (normal), Rojo (alerta), Gris (offline)
- **Indicador de batería:** Barra visual con colores
- **Expansión de edificios:** Click para ver detalles
- **Actualización automática:** Cada 30 segundos (simulado)

## 🎨 Paleta de Colores

### Estados
- **Normal:** Verde `#28a745`
- **Alerta:** Rojo `#dc3545` con animación
- **Offline:** Gris `#6c757d`
- **Warning:** Amarillo `#ffc107`

### Principales
- **Primario:** Gradiente morado `#667eea` → `#764ba2`
- **Fondo:** `#f5f7fa`
- **Texto:** `#2c3e50`

## 📊 Datos de Ejemplo Incluidos

El demo muestra:

### Torre Central (Av. Reforma 2350, CDMX)
- **Apartamento 101:** 3 sensores normales (1 con batería baja)
- **Apartamento 203:** 1 sensor en ALERTA (950 PPM) + 1 normal

### Residencial Las Palmas (Guadalajara)
- 12 sensores normales (colapsado)

### Edificio Industrial Norte (Monterrey)
- 4 sensores normales (colapsado)

### Escenario de Alerta Activa
El demo incluye una **alerta real activa** en:
- 🏢 Torre Central
- 🏠 Apartamento 203
- 🍳 Cocina
- 🚨 950 PPM (excede umbral de 800 PPM)

## 🔧 Características Técnicas

### HTML/CSS
- 100% HTML puro + CSS3
- Sin dependencias externas
- Diseño responsive
- Animaciones CSS

### Interactividad
- JavaScript vanilla para:
  - Actualización del reloj
  - Toggle de edificios expandidos
  - Simulación de actualizaciones

### Compatibilidad
- Chrome, Firefox, Safari, Edge (últimas versiones)
- Funciona offline
- No requiere backend

## 📝 Wireframes y Documentación

Además del demo interactivo, consulta:

**`docs/DASHBOARD_DESIGN.md`** - Diseño completo con:
- Wireframes ASCII
- Especificaciones de colores
- Características de interactividad
- Diseño responsive
- Sistema de notificaciones
- Vistas adicionales (historial, configuración)

## 🎯 Próximos Pasos

Para implementar este dashboard con datos reales:

1. **Frontend Framework:** React o Vue.js
2. **WebSocket:** Para actualizaciones en tiempo real
3. **State Management:** Redux o Vuex
4. **API Integration:** Conectar a `http://localhost:8000/api/v1`
5. **Autenticación:** JWT tokens
6. **Charts:** Para visualizaciones de tendencias
7. **Mapas:** Para ubicación geográfica de edificios

## 🖼️ Capturas Conceptuales

### Vista General
```
┌─────────────────────────────────────────────┐
│ 🛡️ EngiSensors                      [Admin] │
├─────────────────────────────────────────────┤
│ [Dashboard] [Edificios] [Sensores] [Config] │
├─────────────────────────────────────────────┤
│ 🚨 ¡ALERTA! Apt 203 - Cocina - 950 PPM      │
├─────────────────────────────────────────────┤
│ [24 Normal] [1 Alerta] [2 Batería] [3 Edif]│
├─────────────────────────────────────────────┤
│ 🏢 Torre Central              ✅8 🚨1 ⚫0  │
│   ├─ Apt 101                                │
│   │  ├─ 🍳 Cocina      ✅ 120 PPM           │
│   │  ├─ 🧺 Lavadero    ✅ 95 PPM            │
│   │  └─ 🛋️ Sala        ✅ 102 PPM  ⚠️Bat   │
│   └─ Apt 203                                │
│      ├─ 🍳 Cocina      🚨 950 PPM ⚠️        │
│      └─ 🧺 Lavadero    ✅ 110 PPM           │
├─────────────────────────────────────────────┤
│ 🏢 Residencial Las Palmas     ✅12 🚨0 ⚫0 │
│ 🏢 Industrial Norte           ✅4  🚨0 ⚫0 │
└─────────────────────────────────────────────┘
```

### Tarjeta de Sensor en Alerta
```
┌────────────────────────────┐
│ 🍳 Cocina      🚨 ALERTA   │  ← Parpadeo rojo
├────────────────────────────┤
│ Gas:     950 PPM ⚠️         │  ← Texto rojo
│ Umbral:  800 PPM           │
│ Batería:  92% [████████░] │
│ Señal:   -41 dBm           │
├────────────────────────────┤
│ S-TC-203-001               │
│ ⚠️ HACE 2 MINUTOS          │
└────────────────────────────┘
```

## 💡 Personalización

Puedes modificar el demo editando `demo-dashboard.html`:

### Cambiar Datos
Busca en el HTML y modifica:
```html
<!-- Ejemplo: Cambiar nivel de gas -->
<div class="metric-value danger">950 PPM ⚠️</div>
```

### Cambiar Colores
Modifica el `<style>`:
```css
.sensor.alert {
    border-color: #dc3545;  /* Color del borde */
    background: #fef5f6;     /* Color de fondo */
}
```

### Agregar Más Edificios
Copia y pega una sección de `.building-card` y modifica los datos.

## 📞 Feedback

Este es un demo visual. Para la implementación real, necesitaremos:
- ✅ Backend API (ya implementado)
- ⏳ Frontend React/Vue
- ⏳ WebSocket para tiempo real
- ⏳ Sistema de autenticación
- ⏳ Integración con base de datos

---

**¿Te gusta el diseño? ¿Hay algo que quieras cambiar o agregar?**
