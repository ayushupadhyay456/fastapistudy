import core
from stores import FileStore

NOW_MS = 1_000_000_000
END_MS = NOW_MS - core.INGESTION_DELAY_SECONDS * 1000


class FakeStore:
    def __init__(self, value=None):
        self.value = value
        self.saved = []

    def get(self):
        return self.value

    def set(self, timestamp_ms):
        self.saved.append(timestamp_ms)


def run(store, fetch=None, process=None, groups=("/demo",)):
    calls = []

    def default_fetch(group, start, end):
        calls.append((group, start, end))
        return []

    result = core.run_once(
        store,
        list(groups),
        fetch_fn=fetch or default_fetch,
        process_fn=process or (lambda errors: None),
        now_ms=NOW_MS,
    )
    return result, calls


def test_first_run_uses_lookback_window():
    store = FakeStore(None)
    _, calls = run(store)
    start = END_MS - core.FIRST_RUN_LOOKBACK_MINUTES * 60 * 1000
    assert calls == [("/demo", start, END_MS)]
    assert store.saved == [END_MS]


def test_next_run_starts_right_after_checkpoint():
    checkpoint = NOW_MS - 600_000
    store = FakeStore(checkpoint)
    _, calls = run(store)
    assert calls[0][1] == checkpoint + 1
    assert store.saved == [END_MS]


def test_checkpoint_not_moved_when_fetch_fails():
    store = FakeStore(NOW_MS - 600_000)

    def boom(group, start, end):
        raise RuntimeError("CloudWatch is down")

    try:
        run(store, fetch=boom)
        assert False, "should have raised"
    except RuntimeError:
        pass
    assert store.saved == []


def test_checkpoint_not_moved_when_processing_fails():
    store = FakeStore(NOW_MS - 600_000)

    def boom(errors):
        raise RuntimeError("Slack is down")

    try:
        run(store, process=boom)
        assert False, "should have raised"
    except RuntimeError:
        pass
    assert store.saved == []


def test_empty_window_is_skipped():
    store = FakeStore(NOW_MS)  # checkpoint is "now"
    result, calls = run(store)
    assert result["status"] == "skipped"
    assert calls == []
    assert store.saved == []


def test_errors_from_all_groups_reach_processing():
    received = []

    def fetch(group, start, end):
        return [{"log_group": group, "message": "ERROR x", "timestamp": 1}]

    result, _ = run(FakeStore(None), fetch=fetch, process=received.extend, groups=("/a", "/b"))
    assert result["error_count"] == 2
    assert [e["log_group"] for e in received] == ["/a", "/b"]


def test_file_store_round_trip(tmp_path):
    store = FileStore(str(tmp_path / "cp.json"))
    assert store.get() is None  # no file yet
    store.set(12345)
    assert store.get() == 12345


def test_parse_groups():
    assert core.parse_groups(" /a , /b ,, ") == ["/a", "/b"]
    assert core.parse_groups("") == []
    assert core.parse_groups(None) == []
