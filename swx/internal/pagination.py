from copy import deepcopy


def handle_next_pagination(function, resp, **kwargs):
    """
    Prepare an API response object that supports pagination to make the
    request to fetch the next results.

    :param function: The function that will be called to get the next results
                     page.
    :param resp:     The API response object that will be updated to support
                     pagination.
    """
    if resp.paging.next_cursor:
        kwargs2 = deepcopy(kwargs)
        if 'params' not in kwargs2:
            kwargs2['params'] = {}
        kwargs2['params']['next_cursor'] = resp.paging.next_cursor
        resp._iter_func = lambda: function(**kwargs2)
    else:
        resp._iter_func = None
