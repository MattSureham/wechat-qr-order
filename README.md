# 扫码点单微信小程序

扫码点单微信小程序 - Python + uniapp

## 项目介绍

这是一个完整的扫码点单解决方案顾客通过微信扫描餐桌上的二维码，即可直接进入小程序点单、加入购物车、完成支付。

## 功能特点

### 🛒 顾客端
- 📱 微信扫码直接点单
- 🛒 购物车功能
- 💳 微信/支付宝支付
- 📋 订单历史查询
- 🏪 商家信息展示

### 🏪 管理端（待开发）
- 📦 商品管理
- 📝 订单管理
- 💰 收款记录
- 🏪 商家信息配置
- 📊 数据统计

## 技术栈

| 技术 | 说明 |
|------|------|
| **前端** | uniapp (Vue 3 + TypeScript) |
| **后端** | FastAPI + SQLAlchemy |
| **数据库** | SQLite (开发) / MySQL (生产) |
| **支付** | 微信支付 API |

## 环境要求

- **Python**: 3.8.9 或更高版本
- **Node.js**: 14+ (前端开发)
- **MySQL**: 5.7+ (生产环境)

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/MattSureham/wechat-qr-order.git
cd wechat-qr-order
```

### 2. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --reload

# 服务运行在 http://localhost:8000
```

### 3. 安装前端依赖并启动

#### 方式一：使用 HBuilderX（推荐）

1. 下载 HBuilderX: https://www.dcloud.io/hbuilderx.html
2. 用 HBuilderX 打开 `frontend` 目录
3. 修改 `manifest.json` 中的 `YOUR_WECHAT_APPID` 为你的小程序 AppID

**运行项目：**
- 快捷键：**Ctrl + R** (Windows) / **Cmd + R** (Mac)
- 或者点击菜单：**运行** -> **运行到浏览器** -> 选择 Chrome/Safari
- 首次运行会自动安装 uni-app 依赖

**发行小程序：**
- 菜单：**发行** -> **微信小程序** -> **发行**
- 首次需要配置微信开发者工具安装路径

#### 方式二：命令行

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev:mp-weixin

# 构建生产
npm run build:mp-weixin
```

### 4. 配置桌码

在数据库中创建桌位记录，生成二维码：
- 二维码内容: `https://your-domain.com?scene=TABLE_001`
- 或使用小程序短链

## 项目结构

```
wechat-qr-order/
├── frontend/                 # uniapp 前端
│   ├── pages/               # 页面
│   │   ├── index/           # 点单首页
│   │   ├── checkout/        # 订单确认
│   │   └── order-success/   # 成功页
│   ├── store/               # Vuex 状态管理
│   ├── App.vue              # 根组件
│   ├── main.js              # 入口文件
│   └── pages.json           # 页面配置
│
└── backend/                 # Python 后端
    ├── app/
    │   ├── api/             # API 路由
    │   │   └── routes.py   # 接口定义
    │   ├── models/          # 数据库模型
    │   │   └── models.py
    │   ├── schemas/         # Pydantic 模型
    │   │   └── schemas.py
    │   ├── config.py        # 配置
    │   ├── database.py      # 数据库连接
    │   └── main.py          # FastAPI 应用
    │
    └── requirements.txt     # Python 依赖
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/merchant` | GET | 获取商家信息 |
| `/api/merchant` | PUT | 更新商家信息 |
| `/api/products` | GET | 获取商品列表 |
| `/api/products` | POST | 添加商品 |
| `/api/products/{id}` | PUT | 更新商品 |
| `/api/categories` | GET | 获取分类列表 |
| `/api/tables` | GET | 获取桌位列表 |
| `/api/tables/qr/{qr_code}` | GET | 通过二维码获取桌位 |
| `/api/orders` | POST | 创建订单 |
| `/api/orders/{id}` | GET | 获取订单详情 |
| `/api/orders/{id}/pay` | PUT | 订单支付 |
| `/api/orders/{id}/status` | PUT | 更新订单状态 |

## 配置说明

### 后端配置 (`backend/app/config.py`)

```python
# 数据库
DATABASE_URL = "sqlite:///./wechat_order.db"  # 开发环境
# DATABASE_URL = "mysql://user:pass@localhost/db"  # 生产环境

# 微信支付
WECHAT_MCHID = ""        # 商户号
WECHAT_APPID = ""        # 小程序 AppID
WECHAT_PRIVATE_KEY = ""  # 商户私钥
WECHAT_APIV3_KEY = ""   # APIv3 密钥
```

### 前端配置

修改 `frontend/manifest.json`:
```json
{
  "mp-weixin": {
    "appid": "your_wechat_appid"
  }
}
```

修改 `frontend/pages/index/index.vue` 中的 API 地址:
```javascript
url: 'http://localhost:8000/api/...'
// 改为你的服务器地址
```

## 常见问题

### 1. 扫码后显示"页面不存在"
检查 `pages.json` 中的页面路径配置是否正确。

### 2. 无法创建订单
检查后端服务是否正常运行，确保数据库已初始化。

### 3. 支付失败
- 生产环境需要配置真实的微信支付商户号
- 检查域名是否已备案并配置到小程序后台

## 后续开发

- [ ] 管理后台（网页端）
- [ ] 真实微信支付集成
- [ ] 订单推送通知
- [ ] 数据统计分析
- [ ] 会员系统

## License

MIT

## 作者

Matt / Matilda
