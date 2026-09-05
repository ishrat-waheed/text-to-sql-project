from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    city = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship(
        "Order",
        back_populates="customer"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100))
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )
    order_date = Column(
        DateTime,
        default=datetime.utcnow
    )
    status = Column(String(50), default="completed")
    total_amount = Column(Numeric(10, 2), nullable=False)

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order"
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    payment_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_method = Column(String(50))
    status = Column(String(50), default="completed")

    order = relationship(
        "Order",
        back_populates="payment"
    )