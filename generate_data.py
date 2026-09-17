import sqlite3, random, csv
from datetime import date, timedelta

random.seed(42)

conn = sqlite3.connect("bigbasket_capstone.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS category_targets;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    supplier TEXT NOT NULL,
    unit_price_inr INTEGER NOT NULL
);
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    signup_date TEXT NOT NULL,
    city TEXT NOT NULL
);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    amount_inr INTEGER NOT NULL,
    payment_mode TEXT NOT NULL,
    status TEXT NOT NULL,
    rating INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
CREATE TABLE category_targets (
    category TEXT PRIMARY KEY,
    target_revenue_inr INTEGER NOT NULL
);
""")

cities = ["Bengaluru", "Mumbai", "Hyderabad", "Pune"]

products_raw = [
    ("Banana 1kg", "Fruits & Vegetables", "FreshFarms Co", 50),
    ("Tomato 1kg", "Fruits & Vegetables", "FreshFarms Co", 40),
    ("Onion 1kg", "Fruits & Vegetables", "GreenValley Traders", 35),
    ("Apple 1kg", "Fruits & Vegetables", "GreenValley Traders", 180),
    ("Spinach Bunch", "Fruits & Vegetables", "FreshFarms Co", 25),
    ("Toned Milk 1L", "Dairy & Eggs", "DairyBest Ltd", 60),
    ("Paneer 200g", "Dairy & Eggs", "DairyBest Ltd", 90),
    ("Eggs (12pc)", "Dairy & Eggs", "CountryEggs Farms", 84),
    ("Curd 400g", "Dairy & Eggs", "DairyBest Ltd", 45),
    ("Butter 100g", "Dairy & Eggs", "CountryEggs Farms", 55),
    ("Potato Chips 90g", "Snacks & Beverages", "SnackHub India", 30),
    ("Cola 750ml", "Snacks & Beverages", "SnackHub India", 45),
    ("Biscuit Pack", "Snacks & Beverages", "BakeHouse Supplies", 35),
    ("Fruit Juice 1L", "Snacks & Beverages", "SnackHub India", 110),
    ("Namkeen 200g", "Snacks & Beverages", "BakeHouse Supplies", 60),
    ("Shampoo 340ml", "Personal Care", "CarePlus Distributors", 220),
    ("Toothpaste 150g", "Personal Care", "CarePlus Distributors", 95),
    ("Soap Bar 125g", "Personal Care", "CarePlus Distributors", 40),
    ("Hand Wash 250ml", "Personal Care", "CarePlus Distributors", 99),
    ("Face Wash 100g", "Personal Care", "CarePlus Distributors", 150),
    ("Dish Wash Bar", "Household Essentials", "HomeEssentials Traders", 20),
    ("Detergent 1kg", "Household Essentials", "HomeEssentials Traders", 130),
    ("Floor Cleaner 1L", "Household Essentials", "HomeEssentials Traders", 145),
    ("Toilet Cleaner 500ml", "Household Essentials", "HomeEssentials Traders", 89),
    ("Garbage Bags (30pc)", "Household Essentials", "HomeEssentials Traders", 75),
    ("Bread Loaf", "Bakery", "BakeHouse Supplies", 45),
    ("Croissant (2pc)", "Bakery", "BakeHouse Supplies", 70),
    ("Muffin Pack (4pc)", "Bakery", "BakeHouse Supplies", 120),
    ("Cake Slice", "Bakery", "BakeHouse Supplies", 85),
    ("Cookies 200g", "Bakery", "BakeHouse Supplies", 65),
    ("Premium Face Cream 50g", "Personal Care", "CarePlus Distributors", 450),
]
products = [(i, *p) for i, p in enumerate(products_raw, start=1)]
cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

first_names = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Reyansh","Ayaan","Krishna","Ishaan",
               "Ananya","Diya","Saanvi","Aadhya","Kiara","Myra","Anika","Navya","Riya","Siya",
               "Rohan","Kabir","Dev","Yash","Aryan","Zara","Meera","Tara","Nisha","Priya",
               "Aman","Rahul","Karan","Varun","Nikhil","Pooja","Neha","Simran","Divya","Isha",
               "Rohit","Sanjay","Vikram","Manish","Deepak","Kavya","Shreya","Anjali","Pallavi","Sneha"]
customers = []
start_signup = date(2025, 1, 1)
for i, fname in enumerate(first_names, start=1):
    city = cities[i % len(cities)]
    signup = start_signup + timedelta(days=random.randint(0, 400))
    customers.append((i, fname, signup.isoformat(), city))
cur.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)

popularity_weights = [10,8,6,3,5, 9,7,6,8,4, 10,9,5,4,6, 3,5,9,4,3, 8,6,5,4,7, 6,4,3,5,4]
order_date_start = date(2026, 1, 1)
order_date_end = date(2026, 6, 30)
total_days = (order_date_end - order_date_start).days

TOTAL_ORDERS = 500
product_ids_weighted = []
for pid, w in zip(range(1, 31), popularity_weights):
    product_ids_weighted.extend([pid] * w)

payment_modes = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Wallet"]
product_lookup = {p[0]: p for p in products}
customer_lookup = {c[0]: c for c in customers}

orders = []
order_id = 1
for _ in range(TOTAL_ORDERS):
    cust_id = random.randint(1, 50)
    prod_id = random.choice(product_ids_weighted)
    unit_price = product_lookup[prod_id][4]
    quantity = random.randint(1, 5)
    amount = quantity * unit_price
    day_offset = random.randint(0, total_days)
    o_date = order_date_start + timedelta(days=day_offset)
    payment_mode = random.choice(payment_modes)
    roll = random.random()
    if roll < 0.85:
        status = "Delivered"
        rating = random.randint(1, 5)
    elif roll < 0.95:
        status = "Cancelled"
        rating = None
    else:
        status = "Pending"
        rating = None
    orders.append([order_id, cust_id, prod_id, o_date.isoformat(), quantity, amount, payment_mode, status, rating])
    order_id += 1
cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?)", [tuple(o) for o in orders])

category_targets = [
    ("Fruits & Vegetables", 12000),
    ("Dairy & Eggs", 16500),
    ("Snacks & Beverages", 13000),
    ("Personal Care", 15500),
    ("Household Essentials", 17000),
    ("Bakery", 12000),
]
cur.executemany("INSERT INTO category_targets VALUES (?,?)", category_targets)

conn.commit()

raw_rows = []
for o in orders:
    order_id, cust_id, prod_id, o_date, qty, amt, pm, status, rating = o
    cust = customer_lookup[cust_id]
    raw_rows.append({
        "order_id": order_id, "order_date": o_date, "customer_name": cust[1],
        "city": cust[3], "category": product_lookup[prod_id][2], "product_id": prod_id,
        "quantity": qty, "amount_inr": amt, "payment_mode": pm, "status": status,
        "rating": rating if rating is not None else "",
    })

rng2 = random.Random(7)
casing_idx = rng2.sample(range(len(raw_rows)), 20)
for idx in casing_idx:
    r = raw_rows[idx]
    variant = rng2.choice(["upper", "lower", "space"])
    r["city"] = r["city"].upper() if variant == "upper" else (r["city"].lower() if variant == "lower" else " " + r["city"] + " ")
    variant2 = rng2.choice(["upper", "lower", "space"])
    r["category"] = r["category"].upper() if variant2 == "upper" else (r["category"].lower() if variant2 == "lower" else " " + r["category"] + " ")

null_idx = rng2.sample([i for i in range(len(raw_rows)) if i not in casing_idx], 10)
for idx in null_idx:
    raw_rows[idx]["amount_inr"] = ""

outlier_pool = [i for i in range(len(raw_rows)) if i not in casing_idx and i not in null_idx]
outlier_idx = rng2.sample(outlier_pool, 5)
for idx in outlier_idx:
    raw_rows[idx]["amount_inr"] = raw_rows[idx]["amount_inr"] * 40

dup_pool = [i for i in range(len(raw_rows)) if i not in casing_idx and i not in null_idx and i not in outlier_idx]
dup_idx = rng2.sample(dup_pool, 8)
all_rows = raw_rows + [dict(raw_rows[i]) for i in dup_idx]

fieldnames = ["order_id","order_date","customer_name","city","category","product_id",
              "quantity","amount_inr","payment_mode","status","rating"]
with open("orders_raw.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(all_rows)

with open("products.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["product_id", "product_name", "category", "supplier", "unit_price_inr"])
    w.writerows(products)

conn.close()
print("bigbasket_capstone.db, orders_raw.csv, products.csv created.")
