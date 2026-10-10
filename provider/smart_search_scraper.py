from typing import Any

from dify_plugin import ToolProvider


class SmartSearchScraperProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # This provider needs no credentials; it reads public search result
        # pages directly (Bing / DuckDuckGo HTML) instead of calling a
        # search API.
        return None
