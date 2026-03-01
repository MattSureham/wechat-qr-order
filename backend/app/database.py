from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库"""
    from app.models import models
    Base.metadata.create_all(bind=engine)
    seed_data()


def seed_data():
    """填充初始数据"""
    from sqlalchemy.orm import Session
    from app.models import models
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_merchant = db.query(models.Merchant).first()
        if existing_merchant:
            return
        
        # 创建商家
        merchant = models.Merchant(
            id=1,
            name="示例餐厅",
            description="美味佳肴，等您来尝",
            address="示例地址123号",
            phone="13800138000",
            logo_url="",
            business_hours="9:00-21:00"
        )
        db.add(merchant)
        
        # 创建分类
        categories = [
            models.Category(id=1, name="热销推荐", sort_order=1),
            models.Category(id=2, name="招牌菜品", sort_order=2),
            models.Category(id=3, name="主食", sort_order=3),
            models.Category(id=4, name="饮品", sort_order=4),
            models.Category(id=5, name="小吃", sort_order=5),
        ]
        for cat in categories:
            db.add(cat)
        
        db.flush()
        
        # 创建商品
        products = [
            # 热销推荐
            models.Product(id=1, name="招牌烤鸭", description="北京烤鸭，色泽金黄，皮脆肉嫩", price=128.0, original_price=158.0, 
                          category_id=1, merchant_id=1, is_available=True, is_featured=True, stock=50),
            models.Product(id=2, name="红烧肉", description="肥而不腻，入口即化", price=58.0, original_price=68.0,
                          category_id=1, merchant_id=1, is_available=True, is_featured=True, stock=30),
            models.Product(id=3, name="清蒸鲈鱼", description="新鲜鲈鱼，清蒸最佳", price=78.0, original_price=88.0,
                          category_id=1, merchant_id=1, is_available=True, stock=20),
            
            # 招牌菜品
            models.Product(id=4, name="宫保鸡丁", description="经典川菜，麻辣鲜香", price=42.0,
                          category_id=2, merchant_id=1, is_available=True, is_featured=True, stock=40),
            models.Product(id=5, name="麻婆豆腐", description="麻辣鲜香，下饭神器", price=28.0,
                          category_id=2, merchant_id=1, is_available=True, stock=50),
            models.Product(id=6, name="鱼香肉丝", description="酸甜可口，经典美味", price=38.0,
                          category_id=2, merchant_id=1, is_available=True, stock=35),
            
            # 主食
            models.Product(id=7, name="白米饭", description="东北大米，粒粒分明", price=3.0,
                          category_id=3, merchant_id=1, is_available=True, stock=100),
            models.Product(id=8, name="扬州炒饭", description="配料丰富，香味扑鼻", price=25.0,
                          category_id=3, merchant_id=1, is_available=True, stock=30),
            models.Product(id=9, name="牛肉拉面", description="汤鲜面韧，牛肉充足", price=35.0,
                          category_id=3, merchant_id=1, is_available=True, stock=25),
            
            # 饮品
            models.Product(id=10, name="鲜榨橙汁", description="新鲜橙子榨取", price=18.0, original_price=22.0,
                          category_id=4, merchant_id=1, is_available=True, stock=50),
            models.Product(id=11, name="柠檬茶", description="清新解腻", price=15.0,
                          category_id=4, merchant_id=1, is_available=True, stock=60),
            models.Product(id=12, name="可乐", description="冰镇可乐", price=5.0,
                          category_id=4, merchant_id=1, is_available=True, stock=100),
            
            # 小吃
            models.Product(id=13, name="炸鸡翅", description="外酥里嫩", price=22.0,
                          category_id=5, merchant_id=1, is_available=True, is_featured=True, stock=40),
            models.Product(id=14, name="薯条", description="金黄酥脆", price=15.0,
                          category_id=5, merchant_id=1, is_available=True, stock=50),
            models.Product(id=15, name="春卷", description="脆皮春卷", price=18.0,
                          category_id=5, merchant_id=1, is_available=True, stock=35),
        ]
        for product in products:
            db.add(product)
        
        # 创建桌位
        tables = [
            models.Table(id=1, table_number="1", qr_code="TABLE_001", capacity=4, merchant_id=1),
            models.Table(id=2, table_number="2", qr_code="TABLE_002", capacity=4, merchant_id=1),
            models.Table(id=3, table_number="3", qr_code="TABLE_003", capacity=6, merchant_id=1),
            models.Table(id=4, table_number="4", qr_code="TABLE_004", capacity=6, merchant_id=1),
            models.Table(id=5, table_number="5", qr_code="TABLE_005", capacity=8, merchant_id=1),
            models.Table(id=6, table_number="6", qr_code="TABLE_006", capacity=10, merchant_id=1),
            models.Table(id=7, table_number="A01", qr_code="TABLE_A01", capacity=2, merchant_id=1),
            models.Table(id=8, table_number="A02", qr_code="TABLE_A02", capacity=2, merchant_id=1),
        ]
        for table in tables:
            db.add(table)
        
        db.commit()
        print("Initial data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()
