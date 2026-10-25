"""Capa de almacenamiento. Backend: session_state + JSON en disco.

Para migrar a Supabase en el futuro, solo reemplazar la línea:
    _backend: StorageBackend = JSONBackend()
por:
    _backend = SupabaseBackend(supabase_client)

y la interfaz pública (load / save) no cambia en ningún módulo.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Interfaz abstracta
# ─────────────────────────────────────────────────────────────────────────────

@runtime_checkable
class StorageBackend(Protocol):
    """Contrato mínimo para cualquier backend de almacenamiento.

    Para implementar un nuevo backend (ej. Supabase) basta con cumplir
    esta interfaz y asignarlo a ``_backend`` al final de este módulo.
    """

    def load(self, collection: str, key: str, default: Any) -> Any: ...
    def save(self, collection: str, key: str, value: Any) -> bool: ...


# ─────────────────────────────────────────────────────────────────────────────
# Backend JSON (actual)
# ─────────────────────────────────────────────────────────────────────────────

class JSONBackend:
    """session_state (RAM, duración de la sesión) + JSON en disco (persistencia).

    Invariantes de compatibilidad con el código existente:
    - session_state key: ``{collection}_{key}``  (ej. ``portfolio_pato``)
    - Ruta en disco:     ``data/{subdir}/{key}.json``

    El mapeo ``_DIR_MAP`` cubre los casos donde el nombre de la colección
    difiere del subdirectorio en disco (ej. watchlist → data/watchlists/).
    """

    _DIR_MAP: dict[str, str] = {"watchlist": "watchlists"}

    def _ss_key(self, collection: str, key: str) -> str:
        return f"{collection}_{key}"

    def _path(self, collection: str, key: str) -> Path:
        subdir = self._DIR_MAP.get(collection, collection)
        return Path("data") / subdir / f"{key}.json"

    def load(self, collection: str, key: str, default: Any = None) -> Any:
        """Lee session_state → disco → default. Guarda en session_state al cargar."""
        ss_key = self._ss_key(collection, key)
        if ss_key in st.session_state:
            return st.session_state[ss_key]

        path = self._path(collection, key)
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                st.session_state[ss_key] = data
                return data
            except Exception:
                pass

        st.session_state[ss_key] = default
        return default

    def save(self, collection: str, key: str, value: Any) -> bool:
        """Escribe a session_state y, si el filesystem lo permite, a disco.

        Retorna True si el JSON se escribió; False si hubo error de disco
        (ej. Streamlit Cloud con filesystem read-only). La fuente de verdad
        de la sesión queda en session_state independientemente.
        """
        st.session_state[self._ss_key(collection, key)] = value
        try:
            path = self._path(collection, key)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(value, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────

# Swap esta línea para cambiar backend. Los módulos consumidores no cambian.
_backend: StorageBackend = JSONBackend()


def load(collection: str, key: str, default: Any = None) -> Any:
    """Carga {collection}/{key}. Flujo: session_state → disco → default.

    Args:
        collection: nombre del tipo de dato ("portfolio", "alertas", "watchlist").
        key:        identificador dentro de la colección (ej. nombre de usuario).
        default:    valor a devolver (y cachear) si no hay dato previo.
    """
    return _backend.load(collection, key, default)


def save(collection: str, key: str, value: Any) -> bool:
    """Guarda {collection}/{key} en session_state y en disco.

    Returns:
        True si se escribió a disco, False si el filesystem falló
        (en Streamlit Cloud puede ser read-only). session_state siempre se actualiza.
    """
    return _backend.save(collection, key, value)
