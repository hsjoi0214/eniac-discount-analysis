""" Show result on revenue """

df.merge(products_ctg, on='sku').groupby('category')['revenue'].sum().nlargest(20)


""" Plot the top 10 categories by revenue """

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# step 1: aggregate and clean
df_agg = df.merge(products_ctg, on='sku')[['revenue', 'category']]
df_agg['category'] = df_agg['category'].str.strip().str.lstrip(',').str.strip()
df_grouped = df_agg.groupby('category', as_index=False).agg({'revenue': 'sum'})

# step 2: sort and select top 10
df_top10 = df_grouped.sort_values('revenue', ascending=False).head(10).copy()

# step 3: plot
sns.set_style("white")
plt.rcParams["font.family"] = "DejaVu Sans"

plt.figure(figsize=(14, 4))
ax = sns.barplot(
    data=df_top10,
    x='category',
    y='revenue',
    color='#0097a7ff'
)

# step 4: axis + annotation titles & style
ax.set_title("Top 10 Categories by Revenue", fontsize=18, fontweight="bold", color="#434343")
ax.set_xlabel("Category", fontsize=14, fontweight="bold", color="#434343")
ax.set_ylabel("Revenue", fontsize=14, fontweight="bold", color="#434343")
ax.tick_params(axis='x', labelrotation=45, labelsize=12, labelcolor="#434343")
ax.tick_params(axis='y', labelsize=12, labelcolor="#434343")

# step 5: revenue on y axis to million
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"€{x/1e6:.1f}M"))

# step 6: show and format
plt.tight_layout()
plt.show()


""" Plot average discount per top 10 category by revenue """

# step 1: aggregate and clean
df_agg = df.merge(products_ctg, on='sku')[['revenue', 'price_discount_rel', 'category']]
df_agg['category'] = df_agg['category'].str.strip().str.lstrip(',').str.strip()
df_discount = df_agg[df_agg['category'].isin(df_top10['category'].tolist())]
df_discount = df_discount.groupby('category', as_index=False)['price_discount_rel'].mean()

# step 2: sort
df_discount['category'] = pd.Categorical(
    df_discount['category'], categories=df_top10['category'].tolist(), ordered=True
    )

# step 3: plot
sns.set_style("white")
plt.rcParams["font.family"] = "DejaVu Sans"

plt.figure(figsize=(14, 4))
ax = sns.barplot(
    data=df_discount,
    x='category',
    y='price_discount_rel',
    color='#0097a7ff'
)

# step 4: axis + annotation titles & style
ax.set_title("Average Discount by Category (Top 10 by Revenue)", fontsize=18, fontweight="bold", color="#434343")
ax.set_xlabel("Category", fontsize=14, fontweight="bold", color="#434343")
ax.set_ylabel("Average Discount", fontsize=14, fontweight="bold", color="#434343")
ax.tick_params(axis='x', labelrotation=45, labelsize=12, labelcolor="#434343")
ax.tick_params(axis='y', labelsize=12, labelcolor="#434343")

# step 5: discount on y axis to percent
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x * 100)}%"))

# step 6: show and format
plt.tight_layout()
plt.show()




""" Calculate correlation betw. discount and revenue within category/price on daily samples """

corr_dict = {}

df_merged = df.merge(products_ctg, on='sku')

for category in products_ctg['category'].unique():
  mask = (df_merged.category == category)
  corr_df = df[mask].resample('D', on='timestamp').agg({
      "revenue": "sum",
      "price_discount_rel": "mean"
  })
  corr = corr_df.corr().iloc[0, 1]
  nsamples = corr_df.shape[0]
  total_revenue = df[mask].revenue.sum()

  corr_dict[category] = {}

  corr_dict[category]['Overall - Corr'] = corr
  corr_dict[category]['Overall - N Samples'] = nsamples
  corr_dict[category]['Overall - Total Revenue'] = total_revenue

  for price_class in products_ctg['price_class'].unique():
      mask = (df_merged.category == category) & (df_merged.price_class == price_class)
      corr_df = df_merged[mask].resample('D', on='timestamp').agg({
          "revenue": "sum",
          "price_discount_rel": "mean"
      }).copy()
      corr = corr_df.corr().iloc[0, 1]
      nsamples = corr_df.shape[0]
      total_revenue = df[mask].revenue.sum()

      corr_dict[category][price_class + ' - Corr'] = corr
      corr_dict[category][price_class + ' - N Samples'] = nsamples
      corr_dict[category][price_class + ' - Total Revenue'] = total_revenue
      
""" Create df from dict """

df_all = pd.DataFrame.from_dict(corr_dict, orient='index')
df_all.index.name = 'Category'
df_all = df_all.reset_index()
df_all

""" Extract and format dfs """

df_corr = df_all[
    ['Category', 'Overall - Corr' ] +
     [category + ' - Corr' for category in products_ctg['price_class'].unique()]
    ].melt(id_vars=['Category'], var_name="Price Class", value_name="Corr")
df_corr.loc[:, 'Price Class'] = df_corr['Price Class'].str.replace(' - Corr', '')

df_nsamples = df_all[
    ['Category', 'Overall - N Samples'] +
     [category + ' - N Samples' for category in products_ctg['price_class'].unique()]
    ].melt(id_vars=['Category'], var_name="Price Class", value_name="N Samples")
df_nsamples.loc[:, 'Price Class'] = df_nsamples['Price Class'].str.replace(' - N Samples', '')

df_revenue = df_all[
    ['Category', 'Overall - Total Revenue'] +
     [category + ' - Total Revenue' for category in products_ctg['price_class'].unique()]
    ].melt(id_vars=['Category'], var_name="Price Class", value_name="Total Revenue")
df_revenue.loc[:, 'Price Class'] = df_revenue['Price Class'].str.replace(' - Total Revenue', '')


""" Create final df """

df_merged = df_corr.merge(
    df_nsamples, on=['Category', 'Price Class']
    ).merge(
        df_revenue, on=['Category', 'Price Class']
        ).dropna(subset='Corr')
df_merged['Corr Abs'] = df_merged.Corr.abs()
df_merged


""" Calculate p-value and filter by it """

from scipy.stats import t
import numpy as np

def correlation_significance(r, n):
    if n - 2 < 0:
        return np.nan

    if 1 - r**2 < 0:
        return np.nan

    denominator = np.sqrt(1 - r**2)
    if denominator == 0:
        return np.nan

    t_val = r * np.sqrt(n - 2) / denominator
    p_val = 2 * (1 - t.cdf(abs(t_val), df=n-2))

    return p_val

df_merged['P Value'] = df_merged.apply(lambda x: correlation_significance(x['Corr'], x['N Samples']), axis=1).copy()
df_merged = df_merged[df_merged['P Value'] < 0.05]
df_merged


""" Plot correlation """

# step 1: add color for correlation groups
def color_group(corr):
    if corr < 0:
        return "neg"
    elif corr > 0:
        return "pos"
    else:
        return "neu"

df_merged.loc[:, "Color Group"] = df_merged["Corr"].apply(color_group).copy(deep=True)

palette = {
    "neg": "#d9d9d9",  # grey
    "neu": "#d9d9d9",  # grey
    "pos": "#0097a7ff"   # blue
}

# step 2: plot and size
plt.figure(figsize=(5, 4))
sns.scatterplot(
    data=df_merged[df_merged['Price Class'] != 'Overall'],
    x="Corr", y="Total Revenue",
    hue="Color Group",
    palette=palette,
    legend=False,
    s=100
)

# step 3: axis + annotation titles & style
plt.yscale("log")
plt.xticks([-1, -0.5, 0, 0.5, 1], color="#434343")
plt.axvline(x=0, color='gray', linewidth=0.8)
plt.axvline(x=-.5, color='gray', linewidth=0.4)
plt.axvline(x=.5, color='gray', linewidth=0.4)
plt.xlabel("Impact of Discounts", fontsize=14, fontweight='bold', color="#434343")
plt.ylabel("Total Revenue", fontsize=14, fontweight='bold', color="#434343")
plt.tick_params(axis='y', labelsize=12, colors="#434343")

# step 4: y axis in K EUR
def format_k_eur(x, pos):
    return f"€{int(x/1000):,}".replace(",", ".") + "K"
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_k_eur))

# step 5: set font
plt.rcParams["font.family"] = "DejaVu Sans"


""" Plot revenue, orders and discount """

# step 1: resample and aggregate
df_temp = df.resample('W', on='timestamp').agg({
    "id_order": "nunique",
    "revenue": "sum",
    "price_discount_rel": "mean"
})

# step 2: format
df_temp = df_temp.div(df_temp.iloc[0]) * 100
df_temp = df_temp.rename_axis("timestamp").reset_index()
df_long = df_temp.rename(columns={
    'revenue': 'Revenue',
    'id_order': '# of Orders',
    'price_discount_rel': 'Ø Relative Discount'
}).melt(id_vars='timestamp', var_name='Metric', value_name='Value')

# step 3: set color and font
palette = {
    'Revenue': '#ffab40ff',        # orange
    '# of Orders': '#0097a8ff',    # blue
    'Ø Relative Discount': '#bfbfbf'  # grey
}
plt.rcParams["font.family"] = "DejaVu Sans"  # Arial-Ersatz

# step 4: plot and size

scale = 2
fig, ax = plt.subplots(figsize=(13*scale, 6*scale))
sns.lineplot(
    data=df_long,
    x="timestamp", y="Value", hue="Metric",
    palette=palette, ax=ax, linewidth=3, legend=False
)

# step 3: axis + annotation titles & style
ax.set_yticks([])
ax.set_ylabel("Normalized Value", fontsize=14, fontweight="bold", color="#434343")
ax.tick_params(axis='y', left=False)
plt.yscale("log")
ax.set_ylabel(None)
ax.set_yticklabels([])
plt.gca().set_yticks([])

ax.set_xlabel("")
ax.tick_params(axis='x', labelsize=12*scale, colors="#434343")
for label in ax.get_xticklabels():
    label.set_fontsize(12*scale)
    label.set_fontweight("bold")
    label.set_color("#434343")