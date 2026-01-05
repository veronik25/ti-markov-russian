from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Tuple

ALLOWED_CHARS = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?")

def normalize_text(text: str) -> str:
    text = text.lower()
    return "".join(ch for ch in text if ch in ALLOWED_CHARS)

def collect_statistics(corpus_dir: Path, max_order: int = 13):
    overall_counter = Counter()
    conditional_counters: Dict[int, Dict[str, Counter]] = {
        n: defaultdict(Counter) for n in range(1, max_order + 1)
    }

    total_chars = 0
    for path in corpus_dir.glob("*.txt"):
        print(f"Обрабатываем {path.name}...")
        with path.open("r", encoding="utf-8") as f:
            raw = f.read()

        text = normalize_text(raw)
        if not text:
            continue

        print(f"  Символов после фильтра: {len(text):,}")
        overall_counter.update(text)
        total_chars += len(text)

        for i in range(len(text)):
            symbol = text[i]
            for n in range(1, min(max_order, i) + 1):
                context = text[i - n:i]
                conditional_counters[n][context][symbol] += 1

        print(f"  Файл готов. Контекстов 1-3: {[len(conditional_counters[n]) for n in [1,2,3]]}")

    print(f"Обработано {total_chars:,} символов")
    return overall_counter, conditional_counters

def compute_probabilities(overall_counter: Counter,
                          conditional_counters: Dict[int, Dict[str, Counter]]) -> Tuple[dict, dict]:
    total = sum(overall_counter.values())
    overall_stats = {sym: (cnt, cnt / total) for sym, cnt in overall_counter.items()}

    conditional_stats = {}
    for n, ctx_dict in conditional_counters.items():
        conditional_stats[n] = {}
        for context, cnts in ctx_dict.items():
            s = sum(cnts.values())
            conditional_stats[n][context] = {sym: (cnt, cnt / s) for sym, cnt in cnts.items()}
    return overall_stats, conditional_stats
