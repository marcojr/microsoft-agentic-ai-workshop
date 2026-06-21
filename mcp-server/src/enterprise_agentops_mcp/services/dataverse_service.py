from __future__ import annotations

from typing import Any

import httpx
import msal

from enterprise_agentops_mcp.config import (
    DATAVERSE_SP_CLIENT_ID,
    DATAVERSE_SP_CLIENT_SECRET,
    DATAVERSE_SP_TENANT_ID,
    DATAVERSE_URL,
)

_TOKEN_CACHE: dict[str, str] = {}


def _require_dataverse_settings() -> None:
    missing = [
        name
        for name, value in (
            ("DATAVERSE_URL", DATAVERSE_URL),
            ("DATAVERSE_SP_CLIENT_ID", DATAVERSE_SP_CLIENT_ID),
            ("DATAVERSE_SP_CLIENT_SECRET", DATAVERSE_SP_CLIENT_SECRET),
            ("DATAVERSE_SP_TENANT_ID", DATAVERSE_SP_TENANT_ID),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            f"Missing required Dataverse settings: {', '.join(missing)}"
        )


def _get_token() -> str:
    _require_dataverse_settings()

    cache_key = "|".join(
        (
            DATAVERSE_URL,
            DATAVERSE_SP_CLIENT_ID,
            DATAVERSE_SP_TENANT_ID,
        )
    )
    cached_token = _TOKEN_CACHE.get(cache_key)
    if cached_token:
        return cached_token

    app = msal.ConfidentialClientApplication(
        client_id=DATAVERSE_SP_CLIENT_ID,
        client_credential=DATAVERSE_SP_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{DATAVERSE_SP_TENANT_ID}",
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    token = result.get("access_token")
    if not token:
        raise RuntimeError(
            f"Failed to acquire Dataverse token: {result.get('error_description', result)}"
        )

    _TOKEN_CACHE[cache_key] = token
    return token


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_token()}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def escape_odata_string(value: str) -> str:
    return value.replace("'", "''")


def dv_get(
    entity_set: str,
    *,
    filter_query: str | None = None,
    select: str | None = None,
    orderby: str | None = None,
    top: int | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {}
    if filter_query:
        params["$filter"] = filter_query
    if select:
        params["$select"] = select
    if orderby:
        params["$orderby"] = orderby
    if top is not None:
        params["$top"] = top

    response = httpx.get(
        f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}",
        headers=_headers(),
        params=params,
        timeout=30,
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Dataverse GET failed for '{entity_set}' with status {response.status_code}: {response.text}"
        ) from exc
    payload = response.json()
    return payload.get("value", [])


def dv_post(entity_set: str, data: dict[str, Any]) -> dict[str, Any]:
    response = httpx.post(
        f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}",
        json=data,
        headers=_headers(),
        timeout=30,
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Dataverse POST failed for '{entity_set}' with status {response.status_code}: {response.text}"
        ) from exc
    if response.content:
        return response.json()
    return {"status": "created"}


def dv_patch(entity_set: str, row_id: str, data: dict[str, Any]) -> dict[str, Any]:
    response = httpx.patch(
        f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}({row_id})",
        json=data,
        headers=_headers(),
        timeout=30,
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Dataverse PATCH failed for '{entity_set}({row_id})' with status {response.status_code}: {response.text}"
        ) from exc
    if response.content:
        return response.json()
    return {"status": "updated"}
