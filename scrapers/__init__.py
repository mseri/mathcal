from scrapers.las import get_las
from scrapers.nts import get_nts
from scrapers.imp import get_sas, get_taktic, get_apde, get_ammp, get_fd, get_ftmp
from scrapers.impprob import get_icmp
from scrapers.impgeom import get_ipgas, get_ipltgs
from scrapers.gcal import get_gcal
from scrapers.helpers import CachedObject, expired, EMPTY_CACHE

getter = {
    'las': get_las,
    'nts': get_nts,
    'ic/sas': get_sas,
    'ic/taktic': get_taktic,
    'ic/apde': get_apde,
    'ic/ammp': get_ammp,
    'ic/fd': get_fd,
    'ic/ftmp': get_ftmp,
    'ic/icmp': get_icmp,
    'ic/ipgas': get_ipgas,
    'ic/ipltgs': get_ipltgs
}

_gcal_cache = {}


def gcal(gcal_id):
    cached = _gcal_cache.get(gcal_id, CachedObject())
    if expired(cached.last_update) or cached.cache == EMPTY_CACHE:
        cached.cache = get_gcal(gcal_id, cached.last_update)
        _gcal_cache[gcal_id] = cached

    return cached.cache


_cache = {}


def custom(path):
    cached = _cache.get(path, CachedObject())
    if expired(cached.last_update) or cached.cache == EMPTY_CACHE:
        if path in getter:
            cached.cache = getter[path](cached.last_update)
            _cache[path] = cached

    return cached.cache
