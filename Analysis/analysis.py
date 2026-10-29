import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Аналіз постачань препаратів")
    parser.add_argument("csv", help="Шлях до CSV-файлу з постачаннями")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    prices = df["price_per_unit"].to_numpy()
    quantities = df["quantity"].to_numpy()

    mean_price = np.mean(prices)
    median_quantity = np.median(quantities)
    std_price = np.std(prices, ddof=0)

    df["total_price"] = df["quantity"] * df["price_per_unit"]

    supplier_totals = df.groupby("supplier")["total_price"].sum()
    top_supplier = supplier_totals.idxmax()
    top_supplier_total = supplier_totals.loc[top_supplier]

    by_category = df.groupby("category")["quantity"].sum()

    low_supply = df[df["quantity"] < 100]
    low_supply.to_csv(
        "low_supply.csv", index=False, encoding="utf-8", float_format="%.2f"
    )

    top_three = df.sort_values("total_price", ascending=False).head(3)

    print("Сумарна кількість препаратів за категоріями:")
    print(by_category.to_string())
    print("\nТри постачання з найбільшою загальною вартістю:")
    print(top_three.to_string(index=False))

    with open("report.txt", "w", encoding="utf-8") as report:
        report.write("Аналіз постачань препаратів\n\n")
        report.write(f"Середня ціна всіх препаратів: {mean_price:.2f}\n")
        report.write(f"Медіана кількості препаратів: {median_quantity:.2f}\n")
        report.write(f"Стандартне відхилення ціни (ddof=0): {std_price:.2f}\n")
        report.write(f"Постачальник із найбільшим загальним прибутком: {top_supplier}\n")
        report.write(
            f"Прибуток за формулою quantity * price_per_unit: {top_supplier_total:.2f}\n"
        )
        report.write("Файл із дефіцитними постачаннями: low_supply.csv\n")
        report.write(f"Кількість записів із quantity < 100: {len(low_supply)}\n")
        report.write("\nСумарна кількість препаратів за категоріями:\n")
        report.write(by_category.to_string() + "\n")
        report.write("\nТри постачання з найбільшою загальною вартістю:\n")
        report.write(top_three.to_string(index=False) + "\n")
        report.write("\nГрафік: by_category.png\n")

    ax = by_category.plot(kind="bar", figsize=(8, 5), color="steelblue", rot=0)
    ax.set_title("Кількість препаратів за категоріями")
    ax.set_xlabel("Категорія")
    ax.set_ylabel("Кількість, од.")
    ax.bar_label(ax.containers[0], fmt="%d", padding=3)
    ax.set_ylim(0, by_category.max() * 1.15)
    plt.tight_layout()
    plt.savefig("by_category.png", dpi=150)
    plt.close()

    print("\nСтворено: low_supply.csv, report.txt, by_category.png")


if __name__ == "__main__":
    main()
