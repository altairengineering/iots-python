from pydantic import BaseModel, PrivateAttr


class Paginator(BaseModel):
    """
    This class allows to paginate the results of an API response instance.
    """
    _iter_idx: int = PrivateAttr(0)
    _iter_func = PrivateAttr()

    def __iter__(self):
        self._iter_idx = 0
        return self

    def __next__(self) -> bool:
        data = self.__getattribute__('data')
        if self._iter_idx >= len(data):
            if self._iter_func:
                next_results = self._iter_func()
                self._iter_func = next_results._iter_func
                data.extend(next_results.data)
                self.paging = next_results.paging

        if self._iter_idx >= len(data):
            raise StopIteration

        i = self._iter_idx
        self._iter_idx += 1
        return data[i]

    def has_more(self):
        return self._iter_func is not None
