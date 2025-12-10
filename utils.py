import base64
import json
from typing import Any, Dict
from urllib.parse import urlencode


def build_web_app_url(base_url: str, payload: Dict[str, Any]) -> str:
    """Attach encoded payload to the Web App URL."""
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
    return f"{base_url}?{urlencode({'payload': encoded})}"

