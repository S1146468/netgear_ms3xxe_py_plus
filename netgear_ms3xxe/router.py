# netgear_ms3xxe/router.py
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from .exceptions import NetgearAPIError


class Router:
    """
    Single choke-point for API semantics:
      - correct encoding (plain-text JSON string vs normal JSON)
      - consistent JSON parsing
      - consistent errCode handling
      - clear errors when the switch returns HTML or non-JSON
    """

    def __init__(self, transport, auth=None):
        self.transport = transport
        self.auth = auth  # optional (future: ensure_login / refresh)

    # ---------- public helpers ----------

    def get(self, path: str) -> Dict[str, Any]:
        return self._request_json("GET", path)

    def post_textjson(self, path: str, obj: Any | None) -> Dict[str, Any]:
        """
        Sends body as a JSON string with Content-Type: text/plain;charset=UTF-8.
        Use this for endpoints like /api/login_session on MS308E family.
        """
        return self._request_json("POST", path, text_json_body=obj)

    def patch_textjson(self, path: str, obj: Any | None) -> Dict[str, Any]:
        """
        Sends body as a JSON string with Content-Type: text/plain;charset=UTF-8.
        Use this for endpoints like /api/system/login on MS308E family.
        """
        return self._request_json("PATCH", path, text_json_body=obj)

    def post_json(self, path: str, obj: Any | None) -> Dict[str, Any]:
        """Normal JSON body (application/json). Only use if confirmed by HAR."""
        return self._request_json("POST", path, json_body=obj)

    def patch_json(self, path: str, obj: Any | None) -> Dict[str, Any]:
        """Normal JSON body (application/json). Only use if confirmed by HAR."""
        return self._request_json("PATCH", path, json_body=obj)

    # ---------- core request/parse ----------

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        text_json_body: Any | None = None,
        json_body: Any | None = None,
    ) -> Dict[str, Any]:
        headers: Dict[str, str] = {}
        data: Optional[str] = None

        if text_json_body is not None and json_body is not None:
            raise ValueError("Provide only one of text_json_body or json_body")

        if text_json_body is not None:
            headers["Content-Type"] = "text/plain;charset=UTF-8"
            data = json.dumps(text_json_body, separators=(",", ":"))
        elif json_body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(json_body, separators=(",", ":"))

        r = self.transport.request(method, path, headers=headers or None, data=data)

        # If you want “retry once on 401”, add it here later.
        if r.status_code == 401:
            raise NetgearAPIError("Unauthorized (401)")

        # 4xx/5xx -> raise with context
        try:
            r.raise_for_status()
        except Exception as e:
            snippet = (r.text or "")[:300].replace("\n", " ")
            raise NetgearAPIError(f"HTTP {r.status_code} for {method} {path}: {snippet}") from e

        # Guard: API should return JSON; HTML means wrong route / SPA fallback.
        ctype = (r.headers.get("content-type") or "").lower()
        if "application/json" not in ctype:
            snippet = (r.text or "")[:300].replace("\n", " ")
            raise NetgearAPIError(
                f"Non-JSON response for {method} {path} (content-type={ctype}): {snippet}"
            )

        try:
            j = r.json()
        except Exception as e:
            snippet = (r.text or "")[:300].replace("\n", " ")
            raise NetgearAPIError(f"Invalid JSON for {method} {path}: {snippet}") from e

        # NETGEAR-style error envelope
        if isinstance(j, dict) and "errCode" in j and j["errCode"] not in (0, None):
            raise NetgearAPIError(f"API error for {method} {path}: {j}")

        return j
