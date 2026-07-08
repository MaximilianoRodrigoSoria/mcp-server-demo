"""Tool de API externa: clima actual vía Open-Meteo (sin API key)."""

from __future__ import annotations

import httpx

from mcp_server_demo.config import get_settings


def _geocode(city: str) -> dict | None:
    s = get_settings()
    r = httpx.get(
        s.geocode_url, params={"name": city, "count": 1}, timeout=s.http_timeout
    )
    r.raise_for_status()
    results = r.json().get("results") or []
    return results[0] if results else None


def _forecast(lat: float, lon: float) -> dict:
    s = get_settings()
    r = httpx.get(
        s.forecast_url,
        params={"latitude": lat, "longitude": lon, "current": "temperature_2m"},
        timeout=s.http_timeout,
    )
    r.raise_for_status()
    return r.json()


def get_weather(city: str) -> dict:
    """Clima actual de una ciudad. Devuelve ciudad, país y temperatura (°C)."""
    city = (city or "").strip()
    if not city:
        return {"error": "Indicá una ciudad."}
    place = _geocode(city)
    if not place:
        return {"error": f"No encontré la ciudad '{city}'."}
    data = _forecast(place["latitude"], place["longitude"])
    temp = data.get("current", {}).get("temperature_2m")
    return {
        "city": place.get("name"),
        "country": place.get("country"),
        "temperature_c": temp,
    }
