# Dashboard Design - EngiSensors

## Vista Principal del Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🛡️ EngiSensors                                           👤 admin@test.com │
│  Monitoreo en Tiempo Real de Sensores de Gas Combustible           [Logout] │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 Dashboard  │  🏢 Edificios  │  📡 Sensores  │  📞 Contactos  │  ⚙️ Config │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  🚨 ¡ALERTA DE GAS DETECTADA!                                               │
│  Torre Central - Apartamento 203 - Cocina                                   │
│  Nivel: 950 PPM (Umbral: 800 PPM) | Hace 2 minutos                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌─────────────┐
│ ✅  24           │ │ 🚨  1            │ │ ⚠️   2           │ │ 🏢  3       │
│ Sensores         │ │ Alertas          │ │ Batería          │ │ Edificios   │
│ Normales         │ │ Activas          │ │ Baja             │ │ Activos     │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏢 Torre Central                                  📍 Av. Reforma 2350, CDMX │
│ ✅ 8 Normal    🚨 1 Alerta    ⚫ 0 Desconectados                       [▼]   │
├─────────────────────────────────────────────────────────────────────────────┤
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Apartamento 101                                            Piso 1   │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐   │   │
│   │  │ 🍳 Cocina        │ │ 🧺 Lavadero      │ │ 🛋️ Sala          │   │   │
│   │  │ ✅ Normal        │ │ ✅ Normal        │ │ ✅ Normal        │   │   │
│   │  ├──────────────────┤ ├──────────────────┤ ├──────────────────┤   │   │
│   │  │ Gas:    120 PPM  │ │ Gas:     95 PPM  │ │ Gas:    102 PPM  │   │   │
│   │  │ Umbral: 800 PPM  │ │ Umbral: 800 PPM  │ │ Umbral: 800 PPM  │   │   │
│   │  │ Batería:    95%  │ │ Batería:    88%  │ │ Batería:    15% ⚠│   │   │
│   │  │ Señal:  -45 dBm  │ │ Señal:  -52 dBm  │ │ Señal:  -48 dBm  │   │   │
│   │  │                  │ │                  │ │                  │   │   │
│   │  │ S-TC-101-001     │ │ S-TC-101-002     │ │ S-TC-101-003     │   │   │
│   │  │ Hace 30 seg      │ │ Hace 25 seg      │ │ Hace 15 seg      │   │   │
│   │  └──────────────────┘ └──────────────────┘ └──────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Apartamento 203  🚨                                        Piso 2   │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │  ┌──────────────────┐ ┌──────────────────┐                         │   │
│   │  │ 🍳 Cocina        │ │ 🧺 Lavadero      │                         │   │
│   │  │ 🚨 ALERTA        │ │ ✅ Normal        │                         │   │
│   │  ├──────────────────┤ ├──────────────────┤                         │   │
│   │  │ Gas:    950 PPM⚠ │ │ Gas:    110 PPM  │                         │   │
│   │  │ Umbral: 800 PPM  │ │ Umbral: 800 PPM  │                         │   │
│   │  │ Batería:    92%  │ │ Batería:    78%  │                         │   │
│   │  │ Señal:  -41 dBm  │ │ Señal:  -50 dBm  │                         │   │
│   │  │                  │ │                  │                         │   │
│   │  │ S-TC-203-001     │ │ S-TC-203-002     │                         │   │
│   │  │ ⚠️ HACE 2 MIN    │ │ Hace 45 seg      │                         │   │
│   │  └──────────────────┘ └──────────────────┘                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏢 Residencial Las Palmas                    📍 Av. Universidad 1250, GDL   │
│ ✅ 12 Normal   🚨 0 Alertas   ⚫ 0 Desconectados                       [▶]   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏢 Edificio Industrial Norte                📍 Parque Industrial, MTY       │
│ ✅ 4 Normal    🚨 0 Alertas   ⚫ 0 Desconectados                       [▶]   │
└─────────────────────────────────────────────────────────────────────────────┘

        🔄 Actualización automática cada 30 segundos
        Última actualización: 17 Nov 2025, 10:45:30
```

## Diseño de Colores

### Estados de Sensores

**Normal (Verde)**
- Fondo: `#f1f9f3`
- Borde: `#28a745`
- Texto estado: `#155724`

**Alerta (Rojo)**
- Fondo: `#fef5f6` → `#ffe0e3` (animación pulsante)
- Borde: `#dc3545`
- Texto estado: `#721c24`
- Animación: Parpadeo cada 1.5 segundos

**Desconectado (Gris)**
- Fondo: `#f5f6f7`
- Borde: `#6c757d`
- Texto estado: `#383d41`

**Batería Baja (Amarillo)**
- Icono: `⚠️`
- Color: `#ffc107`

### Esquema de Color Principal

- **Primario:** Gradiente morado `#667eea` → `#764ba2`
- **Fondo:** `#f5f7fa`
- **Texto principal:** `#2c3e50`
- **Texto secundario:** `#7f8c8d`
- **Blanco:** `#ffffff`

## Características de Interactividad

### 1. Actualización en Tiempo Real
- **WebSocket** conectado al backend
- Actualización automática cada 30 segundos (fallback)
- Animaciones suaves al actualizar datos
- Indicador visual de "conectado/desconectado"

### 2. Estados de Alerta
- **Banner rojo** aparece cuando hay alertas activas
- **Animación de pulso** en tarjetas de sensores con alerta
- **Sonido de notificación** (opcional, configurable)
- **Contador en tiempo real** desde la detección

### 3. Expansión de Edificios
- Click en header del edificio para expandir/colapsar
- Icono de flecha rota al expandir
- Animación suave de apertura
- Estado persistente en sesión

### 4. Indicadores Visuales
- **Batería:** Barra visual con colores (verde >50%, amarillo 20-50%, rojo <20%)
- **Señal:** Valor en dBm (mejor entre -30 y -50)
- **Último contacto:** Tiempo relativo ("Hace 30 seg", "Hace 2 min")

## Responsive Design

### Desktop (> 1200px)
- Tarjetas de sensores en grid de 3 columnas
- Estadísticas en 4 columnas
- Navegación horizontal completa

### Tablet (768px - 1200px)
- Tarjetas de sensores en grid de 2 columnas
- Estadísticas en 2 columnas
- Navegación compacta

### Mobile (< 768px)
- Tarjetas de sensores en 1 columna
- Estadísticas en 1 columna
- Menú hamburguesa
- Cards más compactas

## Notificaciones Push

```
┌────────────────────────────────────────┐
│  🚨 EngiSensors                    [x] │
├────────────────────────────────────────┤
│  ¡Alerta de Gas Detectada!             │
│                                        │
│  Torre Central - Apt 203               │
│  Cocina: 950 PPM                       │
│                                        │
│  Hace 30 segundos                      │
│                                        │
│  [Ver Detalles]  [Silenciar]          │
└────────────────────────────────────────┘
```

## Filtros y Búsqueda

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 Buscar sensor, edificio, apartamento...                     │
└─────────────────────────────────────────────────────────────────┘

Filtros:
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Todos    │ │ Normal   │ │ Alerta   │ │ Offline  │
│   27  ✓  │ │   24     │ │   1      │ │   0      │
└──────────┘ └──────────┘ └──────────┘ └──────────┘

Ordenar por:
• Última actividad
• Nivel de gas
• Nombre
• Estado
```

## Vista de Historial

```
┌─────────────────────────────────────────────────────────────────┐
│  Historial de Eventos - Torre Central                          │
│  📅 17 Nov 2025                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  10:43  🚨  Apt 203 - Cocina      Gas: 950 PPM  [Ver detalles] │
│  09:15  ✅  Apt 101 - Lavadero    Gas: 95 PPM                  │
│  08:30  ⚠️   Apt 305 - Sala       Batería baja: 12%            │
│  07:00  ✅  Apt 101 - Cocina      Gas: 105 PPM                 │
│                                                                 │
│  [Cargar más...]                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Panel de Configuración

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚙️ Configuración de Alertas                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Umbral de Gas:  [800] PPM                                      │
│                                                                 │
│  Frecuencia de alertas:                                         │
│  ○ Inmediata (cada detección)                                   │
│  ● Máximo 1 cada 5 minutos                                      │
│  ○ Máximo 1 cada 30 minutos                                     │
│                                                                 │
│  Canales de notificación:                                       │
│  ☑ Email                                                        │
│  ☑ SMS                                                          │
│  ☐ Push (navegador)                                             │
│  ☐ Webhook                                                      │
│                                                                 │
│  Silenciar alertas:                                             │
│  Desde: [--:--]  Hasta: [--:--]  ☐ Activar                      │
│                                                                 │
│  [Guardar configuración]                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Iconografía

### Ubicaciones
- 🍳 Cocina
- 🧺 Lavadero
- 🛋️ Sala
- 🛏️ Recámara
- 🚿 Baño
- 🚗 Garaje
- 📦 Bodega
- 🚪 Pasillo

### Estados
- ✅ Normal
- 🚨 Alerta
- ⚠️ Advertencia
- ⚫ Desconectado
- 🔧 Mantenimiento

### Métricas
- 📊 Gas level
- 🔋 Batería
- 📡 Señal
- ⏰ Tiempo

## Accesibilidad

- Contraste AA WCAG 2.1
- Navegación por teclado completa
- Screen reader friendly
- Textos alternativos en iconos
- Colores no como único indicador (iconos + texto)

## Performance

- Lazy loading de edificios (solo mostrar expandidos bajo demanda)
- Virtual scrolling para listas largas (>100 sensores)
- Optimización de re-renders (React.memo, useMemo)
- Compresión de imágenes
- Service Worker para offline mode
