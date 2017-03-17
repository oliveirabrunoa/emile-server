from flask import abort
import settings


def get_paginated_list(results, url, start, page_size=settings.PAGINATION_SIZE):
    # check if page exists
    count = len(results)
    # make response
    obj = {}
    obj['start'] = start
    obj['page_size'] = page_size
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - page_size)
        page_size_copy = start - 1
        obj['previous'] = url + '?start=%d' % (start_copy)
    # make next url
    if start + page_size > count:
        obj['next'] = ''
    else:
        start_copy = start + page_size
        obj['next'] = url + '?start=%d' % (start_copy)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + page_size)]
    return obj
