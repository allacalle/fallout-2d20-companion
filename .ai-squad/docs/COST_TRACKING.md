# Cost Tracking — AI-SQUAD v7.1

Registro de qué modelo se usó en cada fase de cada sprint.

## Formato

```markdown
## Sprint: [Nombre/Fecha]

| Fase | Agente | Modelo Asignado | Modelo Real | Coste | Desviación |
|------|--------|----------------|-------------|-------|------------|
| 0.5  | Researcher | Qwen3.5 Plus | Qwen3.5 Plus | bajo | ✅ |
| 0.7  | Architect | Kimi K2.6 | Kimi K2.6 | alto | ✅ |
| 4    | QA | DeepSeek V4 Flash | DeepSeek V4 Flash | muy bajo | ✅ |
| 4    | Frontend | MiniMax M2.7 | DeepSeek V4 Pro | medio | ⚠️ (Kimi no disponible) |

## Resumen de costes
- Total fases: 8
- Desviaciones: 1 (justificada)
- Modelo más usado: Qwen3.5 Plus (3 fases)
- Coste estimado total: $X.XX
```

## Reglas

1. Registrar DESPUÉS de cada fase (el agente que ejecutó debe reportar qué modelo usó)
2. Marcar desviaciones con ⚠️ y razón
3. Si hay desviación sin justificación → el Process Auditor debe bloquear
