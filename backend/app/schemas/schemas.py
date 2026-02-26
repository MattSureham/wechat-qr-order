from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ Merchant Schemas ============

class MerchantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    business_hours: Optional[str] = None


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(MerchantBase):
    pass


class MerchantResponse(MerchantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Category Schemas ============

class CategoryBase(BaseModel):
    name: str
    sort_order: int = 0
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Product Schemas ============

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: bool = True
    is_featured: bool = False
    stock: int = 0
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    merchant_id: int


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    merchant_id: int
    sold_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(ProductResponse):
    category_name: Optional[str] = None


# ============ Table Schemas ============

class TableBase(BaseModel):
    table_number: str
    qr_code: str
    capacity: int = 4


class TableCreate(TableBase):
    merchant_id: int


class TableUpdate(TableBase):
    is_active: bool = True


class TableResponse(TableBase):
    id: int
    merchant_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Order Schemas ============

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float
    subtotal: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    table_id: int
    items: List[OrderItemCreate]
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    remark: Optional[str] = None
    discount_amount: float = 0


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    total_amount: float
    discount_amount: float
    final_amount: float
    payment_method: Optional[str] = None
    payment_time: Optional[datetime] = None
    transaction_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    remark: Optional[str] = None
    table_id: Optional[int] = None
    merchant_id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


# ============ Payment Schemas ============

class PaymentRequest(BaseModel):
    order_id: int
    payment_method: str = "wechat"


class PaymentResponse(BaseModel):
    order_id: int
    payment_url: Optional[str] = None  # 支付链接/二维码
    qr_code: Optional[str] = None  # 支付二维码
    status: str
    message: str
