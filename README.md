<p align="center">
<a href="https://www.linkedin.com/in/soriamaximilianorodrigo/" target="_blank" rel="noopener noreferrer">
<img width="100%" height="100%" src="docs/img/banner.gif" alt="mcp-server-demo"></a>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/MCP-Model_Context_Protocol-14B8A6?logo=anthropic&logoColor=white&style=flat-square" alt="MCP"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python_%2F_TypeScript-FastMCP-3776AB?style=flat-square" alt="SDK"></a>
  <a href="#"><img src="https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white&style=flat-square" alt="SQLite"></a>
  <a href="#"><img src="https://img.shields.io/badge/Transporte-stdio_%7C_HTTP-22D3EE?style=flat-square" alt="Transporte"></a>
</p>

<p align="center">
  <a href="https://github.com/DietrichGebert/ponytail"><img src="https://img.shields.io/badge/built_with-ponytail-111111?style=flat-square" alt="ponytail"></a>
  <img src="https://img.shields.io/badge/layout-src%2Fpackage-14B8A6?style=flat-square" alt="src layout">
  <img src="https://img.shields.io/badge/license-MIT-success?style=flat-square" alt="MIT">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=1DE9B6&center=true&vCenter=true&width=820&lines=Model+Context+Protocol%3A+tools+para+tu+LLM;SQLite+%2B+API+externa+expuestas+como+tools;stdio+local+o+HTTP+remoto" alt="typing SVG">
</p>

<!-- dynamic-badges -->
<p align="center">
  <a href="https://github.com/MaximilianoRodrigoSoria/mcp-server-demo/actions"><img src="https://img.shields.io/github/actions/workflow/status/MaximilianoRodrigoSoria/mcp-server-demo/ci.yml?style=flat-square&logo=githubactions&logoColor=white&label=CI&labelColor=1A1C1F&color=06C69C" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/MaximilianoRodrigoSoria/mcp-server-demo?style=flat-square&labelColor=1A1C1F&color=06C69C" alt="License"></a>
  <img src="https://img.shields.io/github/last-commit/MaximilianoRodrigoSoria/mcp-server-demo?style=flat-square&labelColor=1A1C1F&color=06C69C" alt="Last commit">
  <img src="https://img.shields.io/github/repo-size/MaximilianoRodrigoSoria/mcp-server-demo?style=flat-square&labelColor=1A1C1F&color=06C69C" alt="Repo size">
  <a href="https://maximilianorodrigosoria.github.io/mcp-server-demo/"><img src="https://img.shields.io/badge/GitHub_Pages-online-02ECB6?style=flat-square&logo=githubpages&logoColor=white&labelColor=1A1C1F" alt="Pages"></a>
  <img src="https://img.shields.io/badge/Python-3.12-06C69C?style=flat-square&logo=python&logoColor=white&labelColor=1A1C1F" alt="Python">
</p>

<hr/>

<h1 align="center">mcp-server-demo</h1>

<p align="center">
Servidor <b>MCP (Model Context Protocol)</b> que expone herramientas propias
(consultas a una base SQLite y a una API externa) para que un LLM las use de forma estandarizada.
</p>

## Objetivo

Demostrar dominio del protocolo abierto que está estandarizando cómo los LLM acceden a herramientas y datos externos. En vez de acoplar tools a un framework concreto, se construye un servidor MCP reutilizable por cualquier cliente compatible (Claude Desktop, el sistema multi-agente de este portfolio, IDEs, etc.).

El servidor expone, como mínimo:

- **Tools** — acciones invocables: consultar una base de datos local (SQLite) y llamar a una API externa (ej. clima, tipo de cambio, o una API pública de datos).
- **Resources** — datos legibles por el modelo (ej. el esquema de la base, un catálogo).
- (Opcional) **Prompts** — plantillas de prompt reutilizables parametrizadas.

## Stack tecnológico

- **Opción A — Python:** SDK oficial `mcp` (con `FastMCP`) — recomendado por rapidez de desarrollo
- **Opción B — TypeScript:** `@modelcontextprotocol/sdk` — útil si se quiere mostrar versatilidad
- **Transporte:** `stdio` para uso local con clientes de escritorio; **Streamable HTTP** para exposición remota
- **Base de datos:** SQLite (con un dataset de ejemplo sembrado)
- **API externa:** una API pública sin fricción (ej. Open-Meteo para clima, o exchangerate.host)
- **Validación:** Pydantic (Python) o Zod (TS)
- **Cliente de prueba:** MCP Inspector (`npx @modelcontextprotocol/inspector`) y/o Claude Desktop
- **Testing / calidad:** pytest (o vitest), ruff/black (o eslint/prettier)

## Estructura de carpetas (variante Python)

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

---

<!-- diagrama-mermaid -->
## 📊 Diagrama

```mermaid
flowchart LR
    client["Cliente MCP<br/>Claude Desktop · IDE · agentes"] -->|stdio| server["Servidor MCP · FastMCP"]
    server --> db["Tool SQLite<br/>search_customers · get_order_by_id"]
    server --> api["Tool clima<br/>get_weather · Open-Meteo"]
    server --> res["Resource<br/>esquema de la base"]
```
