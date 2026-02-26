from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import models
from app.schemas import schemas
from datetime import datetime
import uuid
import random

router = APIRouter()


def generate_order_number():
    """生成订单号"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = str(random.randint(1000, 9999))
    return f"ORD{timestamp}{random_str}"


# ============ Merchant API ============

@router.get("/merchant", response_model=schemas.MerchantResponse)
def get_merchant(merchant_id: int = 1, db: Session = Depends(get_db)):
    """获取商家信息"""
    merchant = db.query(models.Merchant).filter(models.Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="商家不存在")
    return merchant


@router.put("/merchant", response_model=schemas.MerchantResponse)
def update_merchant(
    merchant_data: schemas.MerchantUpdate,
    merchant_id: int = 1,
    db: Session = Depends(get_db)
):
    """更新商家信息"""
    merchant = db.query(models.Merchant).filter(models.Merchant.id == merchant_id).first()
    if not merchant:
        # 创建默认商家
        merchant = models.Merchant(id=1, name="示例商家")
        db.add(merchant)
        db.commit()
        db.refresh(merchant)
    
    for key, value in merchant_data.model_dump(exclude_unset=True).items():
        setattr(merchant, key, value)
    
    db.commit()
    db.refresh(merchant)
    return merchant


# ============ Category API ============

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories(
    merchant_id: int = 1,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """获取分类列表"""
    query = db.query(models.Category)
    if is_active:
        query = query.filter(models.Category.is_active == True)
    return query.order_by(models.Category.sort_order).all()


@router.post("/categories", response_model=schemas.CategoryResponse)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """创建分类"""
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ============ Product API ============

@router.get("/products", response_model=List[schemas.ProductListResponse])
def get_products(
    merchant_id: int = 1,
    category_id: Optional[int] = None,
    is_available: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(models.Product).filter(models.Product.merchant_id == merchant_id)
    
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if is_available is not None:
        query = query.filter(models.Product.is_available == is_available)
    if is_featured is not None:
        query = query.filter(models.Product.is_featured == is_featured)
    
    products = query.order_by(models.Product.id).all()
    
    # 添加分类名称
    result = []
    for p in products:
        p_dict = schemas.ProductListResponse.model_validate(p).model_dump()
        if p.category:
            p_dict["category_name"] = p.category.name
        result.append(p_dict)
    
    return result


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


@router.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    """创建商品"""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product_data: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新商品"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除商品"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    db.delete(product)
    db.commit()
    return {"message": "商品已删除"}


# ============ Table API ============

@router.get("/tables", response_model=List[schemas.TableResponse])
def get_tables(
    merchant_id: int = 1,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """获取桌位列表"""
    query = db.query(models.Table).filter(models.Table.merchant_id == merchant_id)
    if is_active:
        query = query.filter(models.Table.is_active == True)
    return query.all()


@router.get("/tables/qr/{qr_code}", response_model=schemas.TableResponse)
def get_table_by_qr(qr_code: str, db: Session = Depends(get_db)):
    """通过二维码获取桌位"""
    table = db.query(models.Table).filter(
        models.Table.qr_code == qr_code,
        models.Table.is_active == True
    ).first()
    if not table:
        raise HTTPException(status_code=404, detail="桌位不存在")
    return table


@router.post("/tables", response_model=schemas.TableResponse)
def create_table(
    table: schemas.TableCreate,
    db: Session = Depends(get_db)
):
    """创建桌位"""
    db_table = models.Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


# ============ Order API ============

@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(
    order_data: schemas.OrderCreate,
    merchant_id: int = 1,
    db: Session = Depends(get_db)
):
    """创建订单"""
    # 计算订单金额
    total_amount = sum(item.subtotal for item in order_data.items)
    final_amount = total_amount - order_data.discount_amount
    
    # 创建订单
    db_order = models.Order(
        order_number=generate_order_number(),
        status="pending",
        total_amount=total_amount,
        discount_amount=order_data.discount_amount,
        final_amount=final_amount,
        customer_name=order_data.customer_name,
        customer_phone=order_data.customer_phone,
        remark=order_data.remark,
        table_id=order_data.table_id,
        merchant_id=merchant_id
    )
    db.add(db_order)
    db.flush()  # 获取订单ID
    
    # 创建订单项
    for item_data in order_data.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            subtotal=item_data.subtotal
        )
        db.add(db_item)
        
        # 更新商品销量
        product = db.query(models.Product).filter(models.Product.id == item_data.product_id).first()
        if product:
            product.sold_count += item_data.quantity
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.get("/orders", response_model=List[schemas.OrderResponse])
def get_orders(
    merchant_id: int = 1,
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """获取订单列表"""
    query = db.query(models.Order).filter(models.Order.merchant_id == merchant_id)
    
    if status:
        query = query.filter(models.Order.status == status)
    
    return query.order_by(models.Order.created_at.desc()).offset(offset).limit(limit).all()


@router.put("/orders/{order_id}/pay", response_model=schemas.OrderResponse)
def pay_order(
    order_id: int,
    payment_method: str = "wechat",
    transaction_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """订单支付"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="订单状态不允许支付")
    
    order.status = "paid"
    order.payment_method = payment_method
    order.payment_time = datetime.now()
    if transaction_id:
        order.transaction_id = transaction_id
    
    db.commit()
    db.refresh(order)
    return order


@router.put("/orders/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """更新订单状态"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order
