# WeChat QR Code Ordering Mini Program

扫码点单微信小程序 - Python + uniapp

## 项目结构

```
wechat-qr-order/
├── frontend/          # uniapp 前端
│   ├── pages/        # 页面
│   ├── components/   # 组件
│   ├── store/       # 状态管理
│   └── utils/       # 工具函数
└── backend/         # Python 后端
    ├── app/         # FastAPI 应用
    └── requirements.txt
```

## 功能特点

### 客户端 (小程序)
- 📱 微信扫码跳转点单
- 🛒 购物车功能
- 💳 微信支付集成
- 📋 订单历史
- 🏪 商家信息展示

### 服务端
- 📦 商品管理 (CRUD)
- 📝 订单管理
- 💰 收款记录
- 🏪 商家信息管理
- 🔗 桌码/二维码关联

## 快速开始

### 后端
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 前端 (uniapp)
```bash
# HBuilderX 打开 frontend 目录
# 或者使用命令行
cd frontend
npm install
npm run dev:%PLATFORM%
```

## 技术栈

- **前端**: uniapp (Vue 3 + TypeScript)
- **后端**: FastAPI + SQLAlchemy
- **数据库**: SQLite (开发) / MySQL (生产)
- **支付**: 微信支付 API

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/products | GET | 获取商品列表 |
| /api/products | POST | 添加商品 |
| /api/products/{id} | PUT | 更新商品 |
| /api/orders | POST | 创建订单 |
| /api/orders/{id} | GET | 获取订单详情 |
| /api/merchant | GET | 获取商家信息 |
| /api/merchant | PUT | 更新商家信息 |

## 配置

1. 复制 `backend/.env.example` 为 `.env`
2. 配置微信支付参数
3. 配置数据库连接

## License

MIT
