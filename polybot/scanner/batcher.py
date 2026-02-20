from typing import List, Any

def chunk_list(data: List[Any], size: int) -> List[List[Any]]:
    """Split a list into chunks of a specific size."""
    return [data[i:i + size] for i in range(0, len(data), size)]
