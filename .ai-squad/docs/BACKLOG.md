# 📋 BACKLOG

## Sprint #0 — Setup & Definition

### Objective
Configurar el proyecto, completar la fase de definición (ADRs, UX, diseño, specs) y dejar todo listo para la fase de construcción.

### Orchestrator Tasks
- [x] Copiar framework AI-SQUAD v7.1 al proyecto
- [x] Configurar CONFIG.md con datos del proyecto
- [x] Crear VISION.md
- [x] Crear Discovery Form
- [ ] Inicializar git repo
- [ ] Ejecutar Fase 0.5: Research
- [ ] Ejecutar Fase 0.7: Architecture (ADRs)
- [ ] Ejecutar Fase 1: UX
- [ ] Ejecutar Fase 1.5: Design + A11y
- [ ] Ejecutar Fase 2: Spec
- [ ] Ejecutar Fase 3: Plan
- [ ] 🚦 HITL #1: Owner valida definición completa

### Researcher Tasks
- [ ] Investigar esquemas JSON óptimos para datos de juego relacionales
- [ ] Investigar patrones de SPA vanilla JS con hash routing
- [ ] Investigar opciones de búsqueda/filtrado en cliente

### Architect Tasks
- [ ] ADR-001: Estructura de datos JSON
- [ ] ADR-002: Organización del proyecto (carpetas, naming)
- [ ] ADR-003: Routing SPA (hash routing)
- [ ] ADR-004: Motor de búsqueda y filtros
- [ ] ADR-005: Despliegue (GitHub Pages)

### UX Architect Tasks
- [ ] Proponer flujos de navegación
- [ ] Definir layout mobile-first

### Designer Tasks
- [ ] Proponer 2-3 direcciones visuales Vault-Tec premium
- [ ] Crear DESIGN.md con tokens

### A11y Auditor Tasks
- [ ] Auditar DESIGN.md WCAG 2.2 AA

### Specifier Tasks
- [ ] Escribir specs para componente de navegación
- [ ] Escribir specs para buscador/filtros
- [ ] Escribir specs para visualización de datos
- [ ] Escribir specs para creador de personajes

### Dependencies
- Research → Architecture → UX → Design → A11y → Spec → Plan → Build

### Notes
- Proyecto 100% frontend vanilla, sin backend
- Todos los datos en JSON estáticos
- Prioridad máxima: datos de equipo (armas, mods, armaduras, consumibles)
