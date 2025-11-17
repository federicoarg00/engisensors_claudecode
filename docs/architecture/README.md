# EngiSensors Architecture Documentation

## Overview

This directory contains architectural documentation for the EngiSensors platform.

## Documents

- **system-architecture.md** - High-level system architecture and component interactions
- **data-model.md** - Database schema and data relationships (see also PRD.md)
- **mqtt-protocol.md** - MQTT topic structure and message formats
- **notification-flow.md** - Alert notification pipeline architecture
- **security-model.md** - Authentication, authorization, and security measures

## Quick Reference

### System Components

1. **MQTT Broker** - Receives sensor data
2. **MQTT Handler Service** - Processes incoming sensor messages
3. **API Service** - RESTful APIs for CRUD operations
4. **WebSocket Service** - Real-time dashboard updates
5. **Notification Service** - Multi-channel alert delivery
6. **Web Dashboard** - Client and admin interfaces

### Data Flow: Gas Detection

```
Sensor → MQTT Broker → MQTT Handler → Event Processing → Notification Queue
                                              ↓                    ↓
                                        Database Event      Notification Service
                                              ↓                    ↓
                                      WebSocket Update      Email/SMS Delivery
```

### Technology Decisions

*To be updated as decisions are made*

- [ ] Backend language/framework
- [ ] Frontend framework
- [ ] MQTT broker choice
- [ ] Cloud provider
- [ ] CI/CD pipeline

---

**Last Updated:** 2025-11-17
