import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load CSV files
orders_df = pd.read_csv("orders_qu.csv")
orderlines_df = pd.read_csv("orderlines_qu.csv")
products_df = pd.read_csv("products_qu.csv")

# Define price baskets in € (Euros)
def categorize_price(price):
    if price <= 50:
        return "Basket 1: €0 - €50 (Low-cost)"
    elif 50 < price <= 100:
        return "Basket 2: €50 - €100 (Affordable)"
    elif 100 < price <= 200:
        return "Basket 3: €100 - €200 (Mid-range)"
    elif 200 < price <= 500:
        return "Basket 4: €200 - €500 (Upper mid-range)"
    elif 500 < price <= 1000:
        return "Basket 5: €500 - €1000 (Premium)"
    elif 1000 < price <= 3000:
        return "Basket 6: €1000 - €3000 (High-end)"
    else:
        return "Basket 7: €3000+ (Luxury)"

products_df["price_basket"] = products_df["price"].apply(categorize_price)

# Filter completed orders only
completed_orders = orders_df[orders_df["state"] == "Completed"]

# Merge data
completed_orderlines = orderlines_df.merge(
    completed_orders[["order_id"]],
    left_on="id_order",
    right_on="order_id",
    how="inner"
)
completed_merged = completed_orderlines.merge(
    products_df[["sku", "price", "price_basket"]],
    on="sku",
    how="left"
)

# Calculate revenue per line
completed_merged["revenue"] = completed_merged["unit_price"] * completed_merged["product_quantity"]

# Define basket order
basket_order = [
    "Basket 1: €0 - €50 (Low-cost)",
    "Basket 2: €50 - €100 (Affordable)",
    "Basket 3: €100 - €200 (Mid-range)",
    "Basket 4: €200 - €500 (Upper mid-range)",
    "Basket 5: €500 - €1000 (Premium)",
    "Basket 6: €1000 - €3000 (High-end)",
    "Basket 7: €3000+ (Luxury)"
]


# Grouping
summary_completed = completed_merged.groupby("price_basket").agg({
    "product_quantity": "sum",
    "revenue": "sum"
}).reset_index().rename(columns={
    "product_quantity": "Total Units Sold",
    "revenue": "Total Revenue"
})

# Ensure order
summary_completed["price_basket"] = pd.Categorical(
    summary_completed["price_basket"],
    categories=basket_order,
    ordered=True
)
summary_completed = summary_completed.sort_values("price_basket")

# Style
bar_color = "#006978"

# Plot
plt.figure(figsize=(16, 7))
sns.barplot(data=summary_completed, x="price_basket", y="Total Revenue", color=bar_color)
plt.title("Total_Revenue_per_Price_Basket", fontsize=18, fontweight='bold')
plt.xlabel("Price Basket", fontsize=14, fontweight='bold')
plt.ylabel("Total Revenue (€)", fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1_000_000:.1f} mil' if x >= 1_000_000 else f'{x:,.0f}'))
plt.tight_layout()
plt.savefig("total_revenue_flat_color.png", dpi=300)
plt.show()


# Add discount flags and % to the dataset
completed_merged["is_discounted"] = completed_merged["unit_price"] < completed_merged["price"]
completed_merged["discount_pct"] = (
    (completed_merged["price"] - completed_merged["unit_price"]) / completed_merged["price"]
).round(2)

# Filter only discounted orderlines
discounted_only = completed_merged[completed_merged["is_discounted"]]

# Calculate average discount % by price basket
avg_discount_by_basket = discounted_only.groupby("price_basket")["discount_pct"].mean().reset_index()
avg_discount_by_basket["price_basket"] = pd.Categorical(
    avg_discount_by_basket["price_basket"],
    categories=basket_order,
    ordered=True
)
avg_discount_by_basket = avg_discount_by_basket.sort_values("price_basket")

# Plot
plt.figure(figsize=(16, 7))
sns.barplot(data=avg_discount_by_basket, x="price_basket", y="discount_pct", color=bar_color)
plt.title("Average Discount Percentage by Price Basket (Discounted Items Only)", fontsize=18, fontweight='bold')
plt.xlabel("Price Basket", fontsize=14, fontweight='bold')
plt.ylabel("Average Discount (%)", fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
plt.tight_layout()
plt.savefig("avg_discount_pct_flat_color.png", dpi=300)
plt.show()
