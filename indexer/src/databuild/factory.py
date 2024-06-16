
from .protocol import DatabuildProtocol
from .builder_search_basic import SearchBasicBuilder

class DataBuilderFactory:
    def create(self, index: str) -> DatabuildProtocol:
        if index == "search-basic":
            return SearchBasicBuilder()
        else:
            raise ValueError(f"Unknown data type: {index}")