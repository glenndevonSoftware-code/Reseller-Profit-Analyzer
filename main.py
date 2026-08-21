import csv
from pathlib import Path

sales_file = Path("sales_history.csv")

def get_number(prompt, must_be_positive=False):

    def show_summary():
      if not sales_file.exists():
        print("No saved sales found.")
        return

    total_revenue = 0
    total_costs = 0
    total_fees = 0
    total_profit = 0
    total_margin = 0
    sale_count = 0

    with sales_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_revenue += float(row["Sale Price"])
            total_costs += float(row["Item Cost"])
            total_costs += float(row["Shipping"])
            total_fees += float(row["Platform Fee"])
            total_profit += float(row["Net Profit"])
            total_margin += float(row["Profit Margin"])
            sale_count += 1

    if sale_count == 0:
        print("No saved sales found.")
        return

    average_margin = total_margin / sale_count

    print("\n===== SALES SUMMARY =====")
    print(f"Number of sales: {sale_count}")
    print(f"Total revenue: ${total_revenue:.2f}")
    print(f"Total costs: ${total_costs:.2f}")
    print(f"Total platform fees: ${total_fees:.2f}")
    print(f"Total profit: ${total_profit:.2f}")
    print(f"Average profit margin: {average_margin:.1f}%")

    while True:
        try:
            number = float(input(prompt))

            if number < 0:
                print("Please enter zero or a positive number.")
                continue

            if must_be_positive and number == 0:
                print("Please enter a number greater than zero.")
                continue

            return number

        except ValueError:
            print("Invalid entry. Please enter a number.")

while True:
    print("\nReseller Profit Analyzer")
    item_name = input("Item name: ")

    sale_price = get_number("Sale price: $", must_be_positive=True)
    item_cost = get_number("Item cost: $")
    shipping_cost = get_number("Shipping cost: $")
    fee_percent = get_number("Platform fee percentage: ")

    platform_fee = sale_price * (fee_percent / 100)
    net_profit = sale_price - item_cost - shipping_cost - platform_fee
    profit_margin = (net_profit / sale_price) * 100

    print("\n--- Results ---")
    print(f"Item: {item_name}")
    print(f"Platform fee: ${platform_fee:.2f}")
    print(f"Net profit: ${net_profit:.2f}")
    print(f"Profit margin: {profit_margin:.1f}%")

    new_file = not sales_file.exists()

    with sales_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if new_file:
            writer.writerow([
                "Item", "Sale Price", "Item Cost", "Shipping",
                "Fee Percent", "Platform Fee", "Net Profit",
                "Profit Margin"
            ])

        writer.writerow([
            item_name, sale_price, item_cost, shipping_cost,
            fee_percent, platform_fee, net_profit, profit_margin
        ])

    print("Sale saved to sales_history.csv")

    again = input("\nAnalyze another sale? (yes/no): ")

    if again.lower() != "yes":
        print("Program closed.")
        break

    show_summary()