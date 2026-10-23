import duckdb
import os

# Путь к исходному CSV (подставь свой, если файл лежит в другой папке)
CSV_PATH = "online_retail.csv"
PARQUET_PATH = "retail.parquet"

def main():
    print("=" * 60)
    print("DuckDB + Parquet Analytics")
    print("=" * 60)

    # Шаг 1: Проверка, что CSV существует
    if not os.path.exists(CSV_PATH):
        print(f"Ошибка: файл {CSV_PATH} не найден.")
        return

    # Шаг 2: Чтение CSV и агрегация (топ-5 стран по выручке)
    print("\n--- Шаг 1: Аналитика CSV через DuckDB ---")
    result = duckdb.sql(f"""
        SELECT 
            Country, 
            COUNT(*) as orders,
            SUM(Quantity) as total_quantity,
            ROUND(SUM(UnitPrice * Quantity), 2) as revenue
        FROM read_csv_auto('{CSV_PATH}', header=True)
        GROUP BY Country
        ORDER BY revenue DESC
        LIMIT 5
    """).fetchall()

    print("Топ-5 стран по выручке (из CSV):")
    for row in result:
        print(f"  {row[0]}: заказов={row[1]}, количество={row[2]}, выручка={row[3]}")

    # Шаг 3: Конвертация CSV в Parquet
    print("\n--- Шаг 2: Конвертация CSV в Parquet ---")
    duckdb.sql(f"""
        COPY (
            SELECT * FROM read_csv_auto('{CSV_PATH}', header=True)
        ) TO '{PARQUET_PATH}' (FORMAT PARQUET)
    """)
    print(f"Parquet-файл создан: {PARQUET_PATH}")

    # Шаг 4: Сравнение размеров
    print("\n--- Шаг 3: Сравнение размеров ---")
    csv_size = os.path.getsize(CSV_PATH) / (1024 * 1024)
    parquet_size = os.path.getsize(PARQUET_PATH) / (1024 * 1024)
    print(f"CSV:     {csv_size:.1f} МБ")
    print(f"Parquet: {parquet_size:.1f} МБ")
    print(f"Сжатие:  {csv_size / parquet_size:.1f}x")

    # Шаг 5: Повторный запрос к Parquet (проверка идентичности)
    print("\n--- Шаг 4: Проверка Parquet ---")
    result_parquet = duckdb.sql(f"""
        SELECT 
            Country, 
            COUNT(*) as orders,
            SUM(Quantity) as total_quantity,
            ROUND(SUM(UnitPrice * Quantity), 2) as revenue
        FROM read_parquet('{PARQUET_PATH}')
        GROUP BY Country
        ORDER BY revenue DESC
        LIMIT 5
    """).fetchall()

    print("Топ-5 стран по выручке (из Parquet):")
    for row in result_parquet:
        print(f"  {row[0]}: заказов={row[1]}, количество={row[2]}, выручка={row[3]}")

    # Шаг 6: Сравнение результатов
    if result == result_parquet:
        print("\n✅ Данные из CSV и Parquet идентичны!")
    else:
        print("\n⚠️ Данные различаются (проверь CSV и Parquet).")

if __name__ == "__main__":
    main()
