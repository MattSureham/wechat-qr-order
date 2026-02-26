<template>
  <view class="container">
    <!-- 商家信息头部 -->
    <view class="merchant-header" v-if="merchant">
      <image class="merchant-logo" :src="merchant.logo_url || '/static/logo.png'" mode="aspectFill" />
      <view class="merchant-info">
        <text class="merchant-name">{{ merchant.name }}</text>
        <text class="merchant-desc">{{ merchant.description || '欢迎光临' }}</text>
        <text class="merchant-hours">{{ merchant.business_hours || '9:00-21:00' }}</text>
      </view>
    </view>

    <!-- 桌号提示 -->
    <view class="table-tip" v-if="currentTable">
      <text>📍 当前位置: {{ currentTable.table_number }}号桌</text>
    </view>

    <!-- 分类标签 -->
    <scroll-view class="category-scroll" scroll-x>
      <view class="category-list">
        <view 
          class="category-item" 
          :class="{ active: selectedCategory === null }"
          @click="selectCategory(null)"
        >
          全部
        </view>
        <view 
          v-for="cat in categories" 
          :key="cat.id"
          class="category-item"
          :class="{ active: selectedCategory === cat.id }"
          @click="selectCategory(cat.id)"
        >
          {{ cat.name }}
        </view>
      </view>
    </scroll-view>

    <!-- 商品列表 -->
    <scroll-view class="product-scroll" scroll-y>
      <view class="product-list">
        <view 
          v-for="product in filteredProducts" 
          :key="product.id"
          class="product-item"
          :class="{ unavailable: !product.is_available }"
          @click="addToCart(product)"
        >
          <image class="product-image" :src="product.image_url || '/static/food.png'" mode="aspectFill" />
          <view class="product-info">
            <text class="product-name">{{ product.name }}</text>
            <text class="product-desc">{{ product.description || '美味可口' }}</text>
            <view class="product-price-row">
              <text class="product-price">¥{{ product.price }}</text>
              <text class="product-original" v-if="product.original_price">¥{{ product.original_price }}</text>
              <text class="product-tag" v-if="product.is_featured">推荐</text>
            </view>
          </view>
          <view class="add-btn" @click.stop="addToCart(product)">
            <text>+</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 购物车底部 -->
    <view class="cart-bar" v-if="cart.length > 0" @click="showCart = true">
      <view class="cart-icon">
        <text>🛒</text>
        <view class="cart-badge">{{ cartItemCount }}</view>
      </view>
      <view class="cart-info">
        <text class="cart-total">¥{{ cartTotal }}</text>
      </view>
      <view class="checkout-btn" @click.stop="goToCheckout">
        <text>去结算</text>
      </view>
    </view>

    <!-- 购物车弹窗 -->
    <view class="cart-modal" v-if="showCart" @click="showCart = false">
      <view class="cart-content" @click.stop>
        <view class="cart-header">
          <text>购物车</text>
          <text class="clear-btn" @click="clearCart">清空</text>
        </view>
        <scroll-view class="cart-items" scroll-y>
          <view v-for="item in cart" :key="item.id" class="cart-item">
            <text class="item-name">{{ item.name }}</text>
            <view class="item-controls">
              <text class="minus-btn" @click="decreaseQuantity(item)">-</text>
              <text class="item-quantity">{{ item.quantity }}</text>
              <text class="plus-btn" @click="increaseQuantity(item)">+</text>
            </view>
            <text class="item-price">¥{{ item.subtotal }}</text>
          </view>
        </scroll-view>
        <view class="cart-footer">
          <text class="total-label">合计:</text>
          <text class="total-price">¥{{ cartTotal }}</text>
          <view class="pay-btn" @click="goToCheckout">
            <text>结算</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

export default {
  data() {
    return {
      merchant: null,
      categories: [],
      products: [],
      selectedCategory: null,
      currentTable: null,
      showCart: false
    };
  },
  computed: {
    ...mapState(['cart']),
    ...mapGetters(['cartItemCount', 'cartTotal']),
    filteredProducts() {
      if (!this.selectedCategory) {
        return this.products.filter(p => p.is_available);
      }
      return this.products.filter(p => p.is_available && p.category_id === this.selectedCategory);
    }
  },
  onLoad(options) {
    // 获取桌码参数
    if (options.scene) {
      // 微信扫码跳转
      this.handleScanResult(options.scene);
    } else if (options.table) {
      this.loadTable(options.table);
    }
    
    this.loadData();
  },
  methods: {
    async loadData() {
      await Promise.all([
        this.loadMerchant(),
        this.loadCategories(),
        this.loadProducts()
      ]);
    },
    
    async loadMerchant() {
      try {
        const res = await uni.request({
          url: 'http://localhost:8000/api/merchant?merchant_id=1'
        });
        if (res.data) {
          this.merchant = res.data;
        }
      } catch (e) {
        console.error('加载商家失败', e);
      }
    },
    
    async loadCategories() {
      try {
        const res = await uni.request({
          url: 'http://localhost:8000/api/categories'
        });
        this.categories = res.data || [];
      } catch (e) {
        console.error('加载分类失败', e);
      }
    },
    
    async loadProducts() {
      try {
        const res = await uni.request({
          url: 'http://localhost:8000/api/products'
        });
        this.products = res.data || [];
      } catch (e) {
        console.error('加载商品失败', e);
      }
    },
    
    async handleScanResult(scene) {
      // 处理扫码结果
      try {
        const res = await uni.request({
          url: `http://localhost:8000/api/tables/qr/${scene}`
        });
        if (res.data) {
          this.currentTable = res.data;
          uni.setStorageSync('currentTable', res.data);
        }
      } catch (e) {
        console.error('桌码无效', e);
      }
    },
    
    async loadTable(tableId) {
      try {
        const res = await uni.request({
          url: `http://localhost:8000/api/tables/qr/${tableId}`
        });
        if (res.data) {
          this.currentTable = res.data;
        }
      } catch (e) {
        console.error('桌码无效', e);
      }
    },
    
    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
    },
    
    addToCart(product) {
      this.$store.commit('addToCart', product);
      uni.showToast({
        title: '已加入购物车',
        icon: 'none'
      });
    },
    
    increaseQuantity(item) {
      this.$store.commit('increaseQuantity', item.id);
    },
    
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        this.$store.commit('decreaseQuantity', item.id);
      } else {
        this.$store.commit('removeFromCart', item.id);
      }
    },
    
    clearCart() {
      this.$store.commit('clearCart');
    },
    
    goToCheckout() {
      this.showCart = false;
      uni.navigateTo({
        url: '/pages/checkout/checkout'
      });
    }
  }
};
</script>

<style>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 120rpx;
}

.merchant-header {
  display: flex;
  padding: 30rpx;
  background: #fff;
}

.merchant-logo {
  width: 120rpx;
  height: 120rpx;
  border-radius: 12rpx;
  background: #eee;
}

.merchant-info {
  flex: 1;
  margin-left: 20rpx;
}

.merchant-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.merchant-desc {
  display: block;
  font-size: 24rpx;
  color: #666;
  margin-top: 8rpx;
}

.merchant-hours {
  display: block;
  font-size: 22rpx;
  color: #999;
  margin-top: 8rpx;
}

.table-tip {
  padding: 20rpx 30rpx;
  background: #fff3cd;
  color: #856404;
  font-size: 26rpx;
  text-align: center;
}

.category-scroll {
  background: #fff;
  white-space: nowrap;
  padding: 20rpx 0;
}

.category-list {
  display: flex;
  padding: 0 30rpx;
}

.category-item {
  padding: 12rpx 30rpx;
  margin-right: 20rpx;
  font-size: 28rpx;
  color: #666;
  background: #f5f5f5;
  border-radius: 30rpx;
}

.category-item.active {
  background: #07c160;
  color: #fff;
}

.product-scroll {
  height: calc(100vh - 400rpx);
}

.product-list {
  padding: 20rpx;
}

.product-item {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
}

.product-item.unavailable {
  opacity: 0.5;
}

.product-image {
  width: 180rpx;
  height: 180rpx;
  background: #eee;
}

.product-info {
  flex: 1;
  padding: 20rpx;
}

.product-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
}

.product-desc {
  display: block;
  font-size: 24rpx;
  color: #999;
  margin-top: 8rpx;
}

.product-price-row {
  display: flex;
  align-items: center;
  margin-top: 16rpx;
}

.product-price {
  font-size: 32rpx;
  color: #ff4d4f;
  font-weight: bold;
}

.product-original {
  font-size: 24rpx;
  color: #999;
  text-decoration: line-through;
  margin-left: 12rpx;
}

.product-tag {
  margin-left: 12rpx;
  padding: 4rpx 12rpx;
  font-size: 20rpx;
  background: #07c160;
  color: #fff;
  border-radius: 4rpx;
}

.add-btn {
  width: 60rpx;
  height: 60rpx;
  background: #07c160;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto 20rpx;
  align-self: center;
}

.add-btn text {
  font-size: 36rpx;
  color: #fff;
}

.cart-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100rpx;
  background: #333;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
}

.cart-icon {
  position: relative;
  font-size: 48rpx;
  margin-top: -30rpx;
}

.cart-badge {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  background: #ff4d4f;
  color: #fff;
  font-size: 20rpx;
  padding: 4rpx 10rpx;
  border-radius: 20rpx;
}

.cart-info {
  flex: 1;
  margin-left: 30rpx;
}

.cart-total {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
}

.checkout-btn {
  background: #07c160;
  padding: 20rpx 50rpx;
  border-radius: 40rpx;
}

.checkout-btn text {
  color: #fff;
  font-size: 28rpx;
}

.cart-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: flex-end;
}

.cart-content {
  width: 100%;
  background: #fff;
  border-radius: 24rpx 24rpx 0 0;
  max-height: 70vh;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
}

.clear-btn {
  color: #ff4d4f;
}

.cart-items {
  max-height: 50vh;
  padding: 0 30rpx;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}

.item-name {
  flex: 1;
  font-size: 28rpx;
}

.item-controls {
  display: flex;
  align-items: center;
}

.minus-btn, .plus-btn {
  width: 48rpx;
  height: 48rpx;
  background: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
}

.item-quantity {
  width: 60rpx;
  text-align: center;
}

.item-price {
  width: 120rpx;
  text-align: right;
  color: #ff4d4f;
}

.cart-footer {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-top: 1rpx solid #eee;
}

.total-label {
  font-size: 28rpx;
}

.total-price {
  flex: 1;
  font-size: 36rpx;
  color: #ff4d4f;
  font-weight: bold;
  margin-left: 20rpx;
}

.pay-btn {
  background: #07c160;
  padding: 20rpx 60rpx;
  border-radius: 40rpx;
}

.pay-btn text {
  color: #fff;
  font-size: 28rpx;
}
</style>
