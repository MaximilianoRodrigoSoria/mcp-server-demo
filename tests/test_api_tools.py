"""Test de la tool de clima con las llamadas HTTP mockeadas (sin red)."""

from __future__ import annotations

from mcp_server_demo.tools import api_tools


def test_get_weather_ok(monkeypatch):
    monkeypatch.setattr(
        api_tools, "_geocode",
        lambda city: {"name": "Rosario", "country": "Argentina", "latitude": -32.9, "longitude": -60.6},
    )
    monkeypatch.setattr(api_tools, "_forecast", lambda lat, lon: {"current": {"temperature_2m": 21.5}})
    out = api_tools.get_weather("Rosario")
    assert out == {"city": "Rosario", "country": "Argentina", "temperature_c": 21.5}


def test_get_weather_ciudad_vacia():
    assert "error" in api_tools.get_weather("")


def test_get_weather_no_encontrada(monkeypatch):
    monkeypatch.setattr(api_tools, "_geocode", lambda city: None)
    assert "error" in api_tools.get_weather("Ciudad Inexistente XYZ")
