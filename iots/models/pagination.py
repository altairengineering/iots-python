from dataclasses import dataclass, field


@dataclass
class _PaginationHelper:
    supported: bool = False
    results_attribute: str = ''
    results: list = None
    iter_idx: int = 0
    iter_func: callable = None


@dataclass
class Paginator:
    """
    This class allows to paginate the results of an API response instance.
    """
    _pagination: _PaginationHelper = field(default_factory=_PaginationHelper,
                                           compare=False)

    def __iter__(self):
        self._pagination.iter_idx = 0
        return self

    def __next__(self) -> bool:
        results = self._pagination.results
        if self._pagination.iter_idx >= len(results):
            if self._pagination.iter_func:
                current_data = getattr(self, self._pagination.results_attribute)
                next_results = self._pagination.iter_func()
                self._pagination.iter_func = next_results._pagination.iter_func
                current_data.extend(getattr(next_results, self._pagination.results_attribute))

        if self._pagination.iter_idx >= len(results):
            raise StopIteration

        i = self._pagination.iter_idx
        self._pagination.iter_idx = self._pagination.iter_idx + 1
        return results[i]
