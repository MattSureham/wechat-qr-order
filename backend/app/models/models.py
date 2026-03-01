from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Merchant(Base):
    """商家信息"""
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    address = Column(String(200))
    phone = Column(String(20))
    logo_url = Column(String(500))
    business_hours = Column(String(100))  # 营业时间，如 "9:00-21:00"
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联
    products = relationship("Product", back_populates="merchant")
    tables = relationship("Table", back_populates="merchant")
    orders = relationship("Order", back_populates="merchant")
    categories = relationship("Category", back_populates="merchant")


class Category(Base):
    """商品分类"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # 外键 - 添加商家关联
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    
    # 关联
    products = relationship("Product", back_populates="category")
    merchant = relationship("Merchant", back_populates="categories")


class Product(Base):
    """商品"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    original_price = Column(Float)  # 原价
    image_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # 招牌/推荐
    stock = Column(Integer, default=0)  # 库存，0表示不限
    sold_count = Column(Integer, default=0)  # 销量
    
    # 外键
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联
    merchant = relationship("Merchant", back_populates="products")
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


class Table(Base):
    """餐桌/桌码"""
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(20), nullable=False)  # 桌号，如 "A01", "1号桌"
    qr_code = Column(String(100), unique=True)  # 二维码标识
    capacity = Column(Integer, default=4)  # 可容纳人数
    is_active = Column(Boolean, default=True)
    
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联
    merchant = relationship("Merchant", back_populates="tables")
    orders = relationship("Order", back_populates="table")


class Order(Base):
    """订单"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True)  # 订单号
    
    # 订单状态: pending, paid, preparing, completed, cancelled
    status = Column(String(20), default="pending")
    
    # 金额
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    final_amount = Column(Float, nullable=False)
    
    # 支付信息
    payment_method = Column(String(20))  # wechat, alipay, cash
    payment_time = Column(DateTime)
    transaction_id = Column(String(100))  # 微信支付交易号
    
    # 客户信息
    customer_name = Column(String(50))
    customer_phone = Column(String(20))
    remark = Column(Text)  # 订单备注
    
    # 外键
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联
    merchant = relationship("Merchant", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """订单项"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # 关联
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
