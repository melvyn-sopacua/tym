from importlib import import_module

__all__ = (
    'SUPPORTED_CACHES',
    'get_cache',
)

SUPPORTED_CACHES = {
    'django': 'services.cache.django.DjangoCache',
}


def _import_class(dotted_path: str):
    module_path, classname = dotted_path.rsplit('.', 1)
    module = import_module(module_path)
    try:
        return getattr(module, classname)
    except AttributeError:
        raise ImportError('Unable to import class {:s}'.format(dotted_path))


def get_cache(name, **init_kwargs):
    if name not in SUPPORTED_CACHES:
        raise KeyError('No such cache supported: {:s}'.format(name))

    klass = _import_class(SUPPORTED_CACHES[name])
    return klass(**init_kwargs)

