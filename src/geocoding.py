"""Geocoding via Google Maps API com cache persistente."""

from __future__ import annotations

import json
import time
from pathlib import Path

import googlemaps

from src.config import GOOGLE_MAPS_API_KEY, CACHE_JSON


class Geocoder:
    """Geocodifica endereços usando Google Maps e mantém cache local."""

    def __init__(self):
        if not GOOGLE_MAPS_API_KEY:
            raise RuntimeError("GOOGLE_MAPS_API_KEY não configurada no .env")
        self.client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        self.cache = self._load_cache()
        self.stats = {"cache": 0, "api": 0, "falha": 0}

    # -- Cache --

    def _load_cache(self) -> dict:
        if CACHE_JSON.exists():
            return json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        return {}

    def _save_cache(self):
        CACHE_JSON.parent.mkdir(parents=True, exist_ok=True)
        CACHE_JSON.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # -- Geocoding --

    def geocode(self, endereco: str, cidade: str = "", estado: str = "SP") -> tuple[float, float]:
        """Retorna (lat, lng) para um endereço. Usa cache quando disponível."""
        query = self._build_query(endereco, cidade, estado)
        key = query.lower().strip()

        # Cache hit
        if key in self.cache:
            self.stats["cache"] += 1
            return tuple(self.cache[key])

        # API call
        try:
            result = self.client.geocode(query, language="pt-BR", region="br")
            if result:
                loc = result[0]["geometry"]["location"]
                lat, lng = loc["lat"], loc["lng"]
                self.cache[key] = [lat, lng]
                self._save_cache()
                self.stats["api"] += 1
                return (lat, lng)

            # Fallback: tenta só cidade
            if cidade:
                fallback = f"{cidade}, {estado}, Brasil"
                result = self.client.geocode(fallback, language="pt-BR", region="br")
                if result:
                    loc = result[0]["geometry"]["location"]
                    lat, lng = loc["lat"], loc["lng"]
                    self.stats["api"] += 1
                    return (lat, lng)

            self.stats["falha"] += 1
            return (-23.5505, -46.6333)  # Centro de SP

        except Exception:
            self.stats["falha"] += 1
            return (-23.5505, -46.6333)

    def _build_query(self, endereco: str, cidade: str, estado: str) -> str:
        parts = [p for p in [endereco, cidade, estado, "Brasil"] if p]
        return ", ".join(parts)

    def print_stats(self):
        total = sum(self.stats.values())
        print(f"  Cache: {self.stats['cache']} | API: {self.stats['api']} | Falhas: {self.stats['falha']} | Total: {total}")
        if total:
            print(f"  Taxa de cache: {self.stats['cache']/total*100:.0f}%")
