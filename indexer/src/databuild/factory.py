
from .protocol import DatabuildProtocol
from .builder_search_basic import SearchBasicBuilder
from .builder_search_knn import SearchKnnBuilder

class DataBuilderFactory:
    def create(self, index: str) -> DatabuildProtocol:
        if index == "search-basic":
            return SearchBasicBuilder()
        elif index == "search-knn":
            return SearchKnnBuilder()
        else:
            raise ValueError(f"Unknown data type: {index}")