from pathlib import Path
import random
from typing import Dict, List, Tuple
from db import get_connection

def load_model(order: int) -> Dict[str, List[Tuple[str, float]]]:
    """Загружаем из БД вероятности для одного порядка."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT context, symbol, probability 
        FROM freq_conditional 
        WHERE order_n = ? 
        ORDER BY context
    """, (order,))
    model: Dict[str, List[Tuple[str, float]]] = {}
    for context, symbol, prob in cur.fetchall():
        model.setdefault(context, []).append((symbol, prob))
    conn.close()
    return model

def generate_text(seed: str, order: int, length: int = 300) -> str:
    """Генерирует текст по начальному фрагменту seed."""
    seed = seed.lower()
    seed = ''.join(c for c in seed if c in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?")
    if len(seed) < order:
        return "Seed слишком короткий"
    
    model = load_model(order)
    text = seed
    context = seed[-order:]
    
    for _ in range(length):
        if context not in model:
            break
        symbols_probs = model[context]
        next_char = random.choices(
            [s for s, p in symbols_probs], 
            [p for s, p in symbols_probs]
        )[0]
        text += next_char
        context = (context + next_char)[-order:]
    
    return text.capitalize()

if __name__ == "__main__":
    print("=== Генератор текста на цепях Маркова ===\n")
    seed = input("Начало текста: ")
    order = int(input("Порядок цепи (1-13): "))
    print(f"\nРезультат (порядок {order}):\n")
    print(generate_text(seed, order))
    input("\nНажмите Enter для выхода...")
