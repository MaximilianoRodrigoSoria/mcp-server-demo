# mcp-server-demo

Servidor **MCP (Model Context Protocol)** que expone herramientas propias para que un LLM las use de forma estandarizada: consultas a una base de datos y a una API externa, con validación de entrada y manejo de errores.

## Objetivo

Demostrar dominio del protocolo abierto que está estandarizando cómo los LLM acceden a herramientas y datos externos. En vez de acoplar tools a un framework concreto, se construye un servidor MCP reutilizable por cualquier cliente compatible (Claude Desktop, el sistema multi-agente de este portfolio, IDEs, etc.).

El servidor expone, como mínimo:

- **Tools** — acciones invocables: consultar una base de datos local (SQLite) y llamar a una API externa (ej. clima, tipo de cambio, o una API pública de datos).
- **Resources** — datos legibles por el modelo (ej. el esquema de la base, un catálogo).
- (Opcional) **Prompts** — plantillas de prompt reutilizables parametrizadas.

## Stack tecnológico sugerido

- **Opción A — Python:** SDK oficial `mcp` (con `FastMCP`) — recomendado por rapidez de desarrollo
- **Opción B — TypeScript:** `@modelcontextprotocol/sdk` — útil si se quiere mostrar versatilidad
- **Transporte:** `stdio` para uso local con clientes de escritorio; **Streamable HTTP** para exposición remota
- **Base de datos:** SQLite (con un dataset de ejemplo sembrado)
- **API externa:** una API pública sin fricción (ej. Open-Meteo para clima, o exchangerate.host)
- **Validación:** Pydantic (Python) o Zod (TS)
- **Cliente de prueba:** MCP Inspector (`npx @modelcontextprotocol/inspector`) y/o Claude Desktop
- **Testing / calidad:** pytest (o vitest), ruff/black (o eslint/prettier)

## Estructura de carpetas propuesta (variante Python)

```
mcp-server-demo/
├── README.md
├── pyproject.toml
├── .env.example
├── data/
│   ├── seed.sql             # Esquema + datos de ejemplo
│   └── demo.db              # SQLite generada (git-ignored)
├── src/
│   ├── server.py            # Entry point: instancia FastMCP y registra todo
│   ├── config.py
│   ├── tools/
│   │   ├── db_tools.py      # query_customers, get_order_by_id, etc.
│   │   └── api_tools.py     # get_weather, get_exchange_rate, etc.
│   ├── resources/
│   │   └── schema.py        # Expone el esquema de la DB como resource
│   └── db/
│       └── connection.py    # Conexión y helpers (queries parametrizadas)
├── scripts/
│   └── seed_db.py           # Crea demo.db desde seed.sql
├── examples/
│   └── claude_desktop_config.json  # Config de ejemplo para registrar el server
└── tests/
    ├── test_db_tools.py
    └── test_api_tools.py
```

## Checklist de implementación

### Fase 1 — Setup

- [ ] Inicializar el proyecto y elegir SDK (Python `mcp`/`FastMCP` o TypeScript).
- [ ] Definir `.env.example` (base URL de la API externa, API key si aplica).
- [ ] Crear `seed.sql` con un dominio simple (ej. clientes/pedidos) y el script `seed_db.py`.

### Fase 2 — Tools de base de datos

- [ ] Implementar la conexión con **queries parametrizadas** (evitar inyección SQL).
- [ ] Exponer al menos 2 tools de DB (ej. `search_customers`, `get_order_by_id`) con schema de entrada tipado y descripciones claras.
- [ ] Manejar el caso "sin resultados" y errores de forma explícita (mensajes útiles para el LLM).

### Fase 3 — Tools de API externa

- [ ] Implementar un cliente HTTP con timeout y reintentos.
- [ ] Exponer al menos 1 tool que llame a la API externa (ej. `get_weather(city)`).
- [ ] Normalizar la respuesta a un formato compacto y útil para el modelo.

### Fase 4 — Resources y prompts

- [ ] Exponer el **esquema de la DB** como resource para que el modelo sepa qué puede consultar.
- [ ] (Opcional) Añadir un prompt template reutilizable (ej. "analiza estos pedidos").

### Fase 5 — Robustez y seguridad

- [ ] Validar todas las entradas antes de tocar DB o API.
- [ ] Descripciones de tools precisas (el LLM decide cuándo usarlas según la descripción).
- [ ] No exponer secretos en respuestas ni logs; leer keys desde entorno.
- [ ] Logging básico de invocaciones (tool, args, latencia).

### Fase 6 — Integración y prueba

- [ ] Probar con **MCP Inspector**: listar tools/resources e invocarlos.
- [ ] Registrar el server en Claude Desktop con `examples/claude_desktop_config.json` y hacer una prueba real.
- [ ] (Opcional) Consumirlo desde `multi-agent-orchestration` para cerrar el portfolio.
- [ ] Variante Streamable HTTP para demostrar exposición remota.

### Fase 7 — Documentación

- [ ] README con cómo levantar el server (stdio y HTTP) y cómo registrarlo en un cliente.
- [ ] Tabla de tools/resources con descripción, parámetros y ejemplo.
- [ ] ADR breve: elección de transporte (stdio vs HTTP) y del SDK.

## Criterios de "terminado"

Un cliente MCP (Inspector o Claude Desktop) descubre las herramientas, un LLM las invoca correctamente contra la DB y la API externa, y las entradas están validadas y los errores manejados. El server funciona por stdio local y, opcionalmente, por HTTP remoto.
