"""이미 발송된 공고 URL을 추적해 중복 발송을 방지한다."""
import json
from pathlib import Path

_PATH = Path("./logs/sent_jobs.json")


def _load() -> set:
    if _PATH.exists():
        return set(json.loads(_PATH.read_text(encoding="utf-8")))
    return set()


def _save(sent: set) -> None:
    _PATH.parent.mkdir(exist_ok=True)
    _PATH.write_text(json.dumps(sorted(sent), ensure_ascii=False, indent=2), encoding="utf-8")


def filter_new(jobs: list[dict]) -> list[dict]:
    sent = _load()
    return [j for j in jobs if j.get("url", j.get("title", "")) not in sent]


def mark_sent(jobs: list[dict]) -> None:
    sent = _load()
    for j in jobs:
        key = j.get("url", j.get("title", ""))
        if key:
            sent.add(key)
    _save(sent)
