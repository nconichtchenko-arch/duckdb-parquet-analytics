# DuckDB + Parquet Analytics

Мини-проект по аналитике данных **без развёртывания СУБД** (Data Lake / Analytics on Files).

## 🎯 Что сделано

1. **Чтение CSV через DuckDB.** Файл `online_retail.csv` (45,5 МБ) прочитан напрямую через DuckDB без ETL.
2. **Аналитический запрос.** Выполнен запрос: топ-5 стран по выручке. Результаты совпали с данными из PostgreSQL.
3. **Конвертация в Parquet.** CSV конвертирован в колоночный формат Parquet.
4. **Сравнение размеров.** CSV — 45,5 МБ, Parquet — 3,8 МБ (сжатие в **11,4 раза**).
5. **Повторный запрос к Parquet.** Через DuckDB подтверждена идентичность данных.

## 🛠 Стек

- **DuckDB** (2.0.0)
- **Python** (Pandas)
- **Parquet** (колоночный формат)
- **SQL**

## 📊 Результаты

| Формат | Размер | Сжатие |
|---|---|---|
| CSV | 45,5 МБ | — |
| Parquet | 3,8 МБ | **11,4x** |

## 🚀 Как запустить

Установка зависимостей:

    pip install duckdb pandas pyarrow

Код:

    import duckdb

    # Чтение CSV и агрегация
    result = duckdb.sql("""
        SELECT Country, SUM(UnitPrice * Quantity) as revenue
        FROM read_csv_auto('online_retail.csv', header=True)
        GROUP BY Country ORDER BY revenue DESC LIMIT 5
    """).fetchall()

    # Конвертация в Parquet
    duckdb.sql("""
        COPY (SELECT * FROM read_csv_auto('online_retail.csv', header=True))
        TO 'retail.parquet' (FORMAT PARQUET)
    """)
