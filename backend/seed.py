from faker import Faker
from decimal import Decimal
from datetime import datetime, timedelta
import random

from app.database import SessionLocal
from app.models import Customer, Product, Order, OrderItem, Payment


fake = Faker("en_US")
db = SessionLocal()


# -----------------------------
# Pakistani Data
# -----------------------------

PAKISTANI_CITIES = [
    "Karachi",
    "Lahore",
    "Islamabad",
    "Rawalpindi",
    "Faisalabad",
    "Multan",
    "Peshawar",
    "Quetta",
    "Hyderabad",
    "Nawabshah",
    "Sukkur",
    "Gujranwala",
    "Sialkot",
    "Bahawalpur",
    "Abbottabad",
]

PRODUCTS = [
    ("Laptop", "Electronics", 120000),
    ("Smartphone", "Electronics", 85000),
    ("Wireless Headphones", "Electronics", 12000),
    ("Smart Watch", "Electronics", 18000),
    ("Keyboard", "Accessories", 4500),
    ("Mouse", "Accessories", 2500),
    ("USB Cable", "Accessories", 1200),
    ("Power Bank", "Accessories", 5000),
    ("Backpack", "Bags", 6500),
    ("School Bag", "Bags", 4500),
    ("Office Chair", "Furniture", 28000),
    ("Study Table", "Furniture", 22000),
    ("LED Monitor", "Electronics", 35000),
    ("Printer", "Electronics", 42000),
    ("External Hard Drive", "Storage", 18000),
    ("SSD 512GB", "Storage", 16000),
    ("USB Flash Drive", "Storage", 2500),
    ("T-Shirt", "Clothing", 2500),
    ("Jeans", "Clothing", 4500),
    ("Jacket", "Clothing", 7500),
    ("Running Shoes", "Footwear", 9000),
    ("Formal Shoes", "Footwear", 8500),
    ("Sandals", "Footwear", 3500),
    ("Coffee Maker", "Kitchen", 15000),
    ("Electric Kettle", "Kitchen", 5500),
    ("Blender", "Kitchen", 8500),
    ("Microwave Oven", "Kitchen", 32000),
    ("Water Bottle", "Lifestyle", 1800),
    ("Travel Mug", "Lifestyle", 2200),
    ("Back Support Cushion", "Lifestyle", 3500),
    ("Notebook", "Stationery", 500),
    ("Pen Set", "Stationery", 800),
    ("Calculator", "Stationery", 1800),
    ("Desk Lamp", "Home", 4500),
    ("Wall Clock", "Home", 3000),
    ("Bed Sheet", "Home", 4000),
    ("Pillow", "Home", 2500),
    ("Face Wash", "Beauty", 1200),
    ("Shampoo", "Beauty", 1800),
    ("Perfume", "Beauty", 5500),
    ("Cricket Bat", "Sports", 8500),
    ("Football", "Sports", 3500),
    ("Badminton Racket", "Sports", 4500),
    ("Yoga Mat", "Sports", 3000),
    ("Water Bottle Sports", "Sports", 2200),
    ("Programming Book", "Books", 3500),
    ("Data Science Book", "Books", 4500),
    ("Python Book", "Books", 4000),
    ("SQL Book", "Books", 3800),
    ("AI Book", "Books", 5000),
]

ORDER_STATUSES = [
    "completed",
    "completed",
    "completed",
    "pending",
    "cancelled",
]

PAYMENT_METHODS = [
    "Cash",
    "Credit Card",
    "Debit Card",
    "JazzCash",
    "EasyPaisa",
]


try:

    print("🚀 Starting seed process...")

    # ---------------------------------
    # Clear old data
    # ---------------------------------

    print("🧹 Clearing old data...")

    db.query(Payment).delete()
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(Product).delete()
    db.query(Customer).delete()

    db.commit()

    # ---------------------------------
    # 1. Create Customers
    # ---------------------------------

    print("👥 Creating 100 customers...")

    customers = []

    for i in range(100):

        first_name = fake.first_name()
        last_name = fake.last_name()

        customer = Customer(
            name=f"{first_name} {last_name}",
            email=f"customer{i + 1}@example.com",
            city=random.choice(PAKISTANI_CITIES),
            created_at=fake.date_time_between(
                start_date="-2y",
                end_date="now"
            )
        )

        customers.append(customer)
        db.add(customer)

    db.commit()

    print("✅ 100 customers created!")

    # ---------------------------------
    # 2. Create Products
    # ---------------------------------

    print("📦 Creating 50 products...")

    products = []

    for name, category, price in PRODUCTS:

        product = Product(
            name=name,
            category=category,
            price=Decimal(str(price)),
            stock=random.randint(10, 200)
        )

        products.append(product)
        db.add(product)

    db.commit()

    print("✅ 50 products created!")

    # ---------------------------------
    # 3. Create Orders
    # ---------------------------------

    print("🛒 Creating 200 orders...")

    orders = []

    for i in range(200):

        customer = random.choice(customers)

        order_date = fake.date_time_between(
            start_date="-1y",
            end_date="now"
        )

        order = Order(
            customer_id=customer.id,
            order_date=order_date,
            status=random.choice(ORDER_STATUSES),
            total_amount=Decimal("0.00")
        )

        db.add(order)
        orders.append(order)

    db.commit()

    print("✅ 200 orders created!")

    # ---------------------------------
    # 4. Create Order Items
    # ---------------------------------

    print("🧾 Creating 500+ order items...")

    total_items = 0

    for order in orders:

        number_of_items = random.randint(2, 4)

        selected_products = random.sample(
            products,
            number_of_items
        )

        order_total = Decimal("0.00")

        for product in selected_products:

            quantity = random.randint(1, 5)

            unit_price = product.price

            item_total = unit_price * quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price
            )

            db.add(order_item)

            order_total += item_total
            total_items += 1

        order.total_amount = order_total

    db.commit()

    print(f"✅ {total_items} order items created!")

    # ---------------------------------
    # 5. Create Payments
    # ---------------------------------

    print("💳 Creating payments...")

    payment_count = 0

    for order in orders:

        # Only create payments for completed orders
        if order.status == "completed":

            payment = Payment(
                order_id=order.id,
                payment_date=order.order_date + timedelta(
                    minutes=random.randint(5, 1440)
                ),
                amount=order.total_amount,
                payment_method=random.choice(PAYMENT_METHODS),
                status="completed"
            )

            db.add(payment)

            payment_count += 1

    db.commit()

    print(f"✅ {payment_count} payments created!")

    # ---------------------------------
    # Final Summary
    # ---------------------------------

    print("\n" + "=" * 50)
    print("🎉 SEEDING COMPLETED SUCCESSFULLY!")
    print("=" * 50)

    print(f"👥 Customers: {db.query(Customer).count()}")
    print(f"📦 Products: {db.query(Product).count()}")
    print(f"🛒 Orders: {db.query(Order).count()}")
    print(f"🧾 Order Items: {db.query(OrderItem).count()}")
    print(f"💳 Payments: {db.query(Payment).count()}")

    print("=" * 50)


except Exception as e:

    db.rollback()

    print("\n❌ ERROR OCCURRED!")
    print(e)

finally:

    db.close()