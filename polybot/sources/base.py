from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseSource(ABC):
    @abstractmethod
    async def fetch_data(self, query: str) -> Optional[Dict[str, Any]]:
        """Fetch data from the external source."""
        pass
