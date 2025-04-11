""" Create consolidated df from data """

df = orderlines_cl.merge(orders_cl, on='id_order').merge(products_cl, on='sku').copy()
df['short'] = df.sku.str[:3].str.upper()
df = df.merge(brands_cl, on='short').copy()
df


""" Add revenue per orderline """

df['revenue'] = df.product_quantity * df.price
df



""" Clean df """

df = df.rename(
    columns = {
        'id' : 'id_orderline',
        'unit_price' : 'product_price_applied',
        'date' : 'timestamp',
        'total_price' : 'total_price_applied',
        'name' : 'product_name',
        'desc' : 'product_description',
        'price' : 'product_price_master',
        'in_stock' : 'product_in_stock',
        'type' : 'product_type',
        'long' : 'brand'
    }
)
df = df.drop(columns=['short', 'created_date', 'total_paid'])
df



""" Add discount information """

df['price_discount_total'] = df.product_price_master - df.product_price_applied
df['price_discount_rel'] = df.price_discount_total / df.product_price_master
df['discount_total'] = df.price_discount_total * df.product_quantity
df


""" Convert datetime columne """

df.timestamp = pd.to_datetime(df.timestamp)
df.dtypes


""" Create categories based on price """

products_ctg = products_cl.copy()
products_ctg['price_class'] = pd.cut(
    products_ctg['price'],
     (0, 50, 100, 200, 500, 1000, 10000000),
    labels=[
        'Low cost',
        'Affordable',
        'Mid-range',
        'Upper mid-range',
        'Premium',
        'High-end'
        ]
    )
products_ctg


""" Create categories based on name and description """

products_ctg["category"] = ""

products_ctg.loc[
    products_ctg["desc"].str.contains("keyboard|keypad", case=False),
    "category"
] += ", keyboard"

products_ctg.loc[
    (products_ctg["name"].str.contains("^.{0,7}apple iphone", case=False)) |
    (products_ctg["desc"].str.contains("^.{0,7}apple iphone", case=False)),
    "category"
] += ", smartphone"

products_ctg.loc[
    products_ctg["name"].str.contains("^.{0,7}apple ipod", case=False),
    "category"
] += ", ipod"

products_ctg.loc[
    (products_ctg["name"].str.contains("^.{0,7}apple ipad|tablet", case=False)) |
    (products_ctg["desc"].str.contains("^.{0,7}apple ipad|tablet", case=False)),
    "category"
] += ", tablet"

products_ctg.loc[
    products_ctg["name"].str.contains("imac|mac mini|mac pro", case=False),
    "category"
] += ", desktop"

products_ctg.loc[
    products_ctg["name"].str.contains("macbook", case=False),
    "category"
] += ", laptop"

products_ctg.loc[
    products_ctg["desc"].str.contains("backpack", case=False),
    "category"
] += ", backpack"

products_ctg.loc[
    products_ctg["desc"].str.contains("case|funda|housing|casing|folder", case=False),
    "category"
] += ", case"

products_ctg.loc[
    products_ctg["desc"].str.contains("dock|hub|connection|expansion box", case=False),
    "category"
] += ", dock"

products_ctg.loc[
    products_ctg["desc"].str.contains("cable|connector|lightning to usb|wall socket|power strip", case=False),
    "category"
] += ", cable"

products_ctg.loc[
    products_ctg["desc"].str.contains("flash drive|hard drive|pendrive|hard disk|memory|storage|ssd|modules|sshd|hdd|(?=.*hard)(?=.*disk)", case=False),
    "category"
] += ", storage"

products_ctg.loc[
    products_ctg["desc"].str.contains("battery", case=False),
    "category"
] += ", battery"

products_ctg.loc[
    products_ctg["desc"].str.contains("headset|headphones|in-ear", case=False),
    "category"
] += ", headset"

products_ctg.loc[
    products_ctg["desc"].str.contains("charger", case=False),
    "category"
] += ", charger"

products_ctg.loc[
    products_ctg["desc"].str.contains("mouse|trackpad", case=False),
    "category"
] += ", mouse"

products_ctg.loc[
    products_ctg["desc"].str.contains("stand|support", case=False),
    "category"
] += ", stand"

products_ctg.loc[
    products_ctg["desc"].str.contains("strap|armband|belt|bracelet", case=False),
    "category"
] += ", strap"

products_ctg.loc[
    products_ctg["desc"].str.contains("^.{0,6}apple watch|smartwatch|smart watch", case=False),
    "category"
] += ", smartwatch"

products_ctg.loc[
    products_ctg["desc"].str.contains("adapter", case=False),
    "category"
] += ", adapter"

products_ctg.loc[
    products_ctg["desc"].str.contains("^.{0,12}ram", case=False),
    "category"
] += ", ram"

products_ctg.loc[
    products_ctg["desc"].str.contains("protect|cover|sleeve|screensaver|shell", case=False),
    "category"
] += ", protection"

products_ctg.loc[
    products_ctg["desc"].str.contains("nas|server|raid|synology", case=False),
    "category"
] += ", server"

products_ctg.loc[
    products_ctg["desc"].str.contains("scale", case=False),
    "category"
] += ", scale"

products_ctg.loc[
    products_ctg["desc"].str.contains("thermometer|thermostat", case=False),
    "category"
] += ", thermometer"

products_ctg.loc[
    products_ctg["desc"].str.contains("monitor", case=False),
    "category"
] += ", monitor"

products_ctg.loc[
    products_ctg["desc"].str.contains("speaker|music system|(?=.*sound)(?=.*bar)", case=False),
    "category"
] += ", speaker"

products_ctg.loc[
    products_ctg["desc"].str.contains("camera|stabilizer|lenses", case=False),
    "category"
] += ", camera"

products_ctg.loc[
    products_ctg["desc"].str.contains("pointer", case=False),
    "category"
] += ", pointer"

products_ctg.loc[
    products_ctg["desc"].str.contains("refurbished|reconditioned|like new|revised", case=False),
    "category"
] += ", refurbished"

products_ctg.loc[
    products_ctg["desc"].str.contains("warranty|care", case=False),
    "category"
] += ", warranty"

products_ctg.loc[
    products_ctg["desc"].str.contains("scooter|wheel", case=False),
    "category"
] += ", rideables"

products_ctg.loc[
    products_ctg["desc"].str.contains("remote", case=False),
    "category"
] += ", remote"

products_ctg.loc[
    products_ctg["desc"].str.contains("router", case=False),
    "category"
] += ", router"

products_ctg.loc[
    products_ctg["desc"].str.contains(r"\d{3}W", case=False),
    "category"
] += ", power supply"

products_ctg.loc[
    products_ctg["desc"].str.contains("locator", case=False),
    "category"
] += ", locator"

products_ctg.loc[
    products_ctg["desc"].str.contains(
        "bulb|(?=.*philips)(?=.*switch)|(?=.*intelligent)(?=.*switch)|(?=.*intelligent)(?=.*home)|weather",case=False),
    "category"
] += ", smart home"

# Fallback-Kategorie
products_ctg.loc[
    products_ctg["category"] == "",
    "category"
] += ", other"

# Kategorien zählen
products_ctg["category"].value_counts()

