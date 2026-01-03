from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Tuple

ALLOWED_CHARS = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?")

def normalize_text(text: str) -> str:
    text = text.lower()
    return "".join(ch for ch in text if ch in ALLOWED_CHARS)

def iter_corpus_files(corpus_dir: Path):
    for path in corpus_dir.glob("*.txt"):
        with path.open("r", encoding="utf-8") as f:
            yield f.read()

def collect_statistics(corpus_dir: Path, max_order: int = 13):
    overall_counter = Counter()
    conditional_counters: Dict[int, Dict[str, Counter]] = {
        n: defaultdict(Counter) for n in range(1, max_order + 1)
    }

    for raw in iter_corpus_files(corpus_dir):
        text = normalize_text(raw)
        if not text:
            continue

        overall_counter.update(text)

        for i in range(len(text)):
            for n in range(1, max_order + 1):
                if i < n:
                    break
                context = text[i - n:i]
                symbol = text[i]
                conditional_counters[n][context][symbol] += 1

    return overall_counter, conditional_counters

def compute_probabilities(overall_counter: Counter,
                          conditional_counters: Dict[int, Dict[str, Counter]]
                          ) -> Tuple[dict, dict]:
    total = sum(overall_counter.values())
    overall_stats = {
        sym: (cnt, cnt / total) for sym, cnt in overall_counter.items()
    }

    conditional_stats = {}
    for n, ctx_dict in conditional_counters.items():
        conditional_stats[n] = {}
        for context, cnts in ctx_dict.items():
            s = sum(cnts.values())
            conditional_stats[n][context] = {
                sym: (cnt, cnt / s) for sym, cnt in cnts.items()
            }
    return overall_stats, conditional_stats
