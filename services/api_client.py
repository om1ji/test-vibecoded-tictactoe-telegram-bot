from __future__ import annotations

from typing import Any, Dict, List

import httpx


class PromoAPIError(Exception):
    """Raised when the Promo API request fails."""


class PromoAPIClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout)

    async def close(self) -> None:
        await self._client.aclose()

    async def health(self) -> Dict[str, Any]:
        try:
            response = await self._client.get("/health")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:  # pragma: no cover - network only
            raise PromoAPIError("Promo API health check failed") from exc

    async def promo_history(self, telegram_id: int) -> List[Dict[str, Any]]:
        try:
            response = await self._client.get(f"/api/v1/promo/{telegram_id}")
            response.raise_for_status()
            body = response.json()
            return body.get("promos", [])
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return []
            raise PromoAPIError("Promo API request failed") from exc
        except httpx.HTTPError as exc:
            raise PromoAPIError("Promo API request failed") from exc
