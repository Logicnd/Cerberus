REGISTRY = {
    "translator": [],
    "analyzer": [],
    "decoder": [],
    "links": [],
}

def register(kind, fn):
    if kind in REGISTRY:
        REGISTRY[kind].append(fn)

def available(kind):
    return list(REGISTRY.get(kind, []))

def run(kind, *args, **kwargs):
    out = []
    for fn in REGISTRY.get(kind, []):
        try:
            out.append(fn(*args, **kwargs))
        except Exception:
            out.append(None)
    return out
