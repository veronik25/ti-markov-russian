from pathlib import Path
from db import init_schema, get_connection
from statistics import collect_statistics, compute_probabilities

def main():
    corpus_dir = Path("corpus")
    max_order = 13

    init_schema()

    overall_counter, conditional_counters = collect_statistics(corpus_dir, max_order)
    overall_stats, conditional_stats = compute_probabilities(overall_counter,
                                                             conditional_counters)

    conn = get_connection()
    cur = conn.cursor()

    cur.executemany(
        "INSERT INTO freq_overall(symbol, count, probability) VALUES (?, ?, ?)",
        [(sym, cnt, prob) for sym, (cnt, prob) in overall_stats.items()]
    )

    for n, ctx_dict in conditional_stats.items():
        rows = []
        for context, sym_dict in ctx_dict.items():
            for sym, (cnt, prob) in sym_dict.items():
                rows.append((n, context, sym, cnt, prob))
        cur.executemany(
            "INSERT INTO freq_conditional(order_n, context, symbol, count, probability) "
            "VALUES (?, ?, ?, ?, ?)",
            rows
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
