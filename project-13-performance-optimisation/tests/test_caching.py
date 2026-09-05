from performance.caching import FileCache


def test_cache_set_and_get(tmp_path):
    cache = FileCache(str(tmp_path))

    cache.set("test-key", {"value": 123})

    assert cache.get("test-key") == {"value": 123}


def test_cache_computes_only_once(tmp_path):
    cache = FileCache(str(tmp_path))
    calls = {"count": 0}

    def compute():
        calls["count"] += 1
        return {"result": "computed"}

    first = cache.get_or_compute("key", compute)
    second = cache.get_or_compute("key", compute)

    assert first == second
    assert calls["count"] == 1
