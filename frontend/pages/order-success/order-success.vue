<template>
  <view class="container">
    <view class="success-icon">✅</view>
    <text class="success-text">下单成功!</text>
    <text class="order-number">订单号: {{ orderNumber }}</text>
    
    <view class="info-card">
      <text class="info-title">订单信息</text>
      <view class="info-row">
        <text>订单金额:</text>
        <text class="amount">¥{{ orderAmount }}</text>
      </view>
      <view class="info-row">
        <text>支付方式:</text>
        <text>{{ paymentMethod === 'wechat' ? '微信支付' : '支付宝' }}</text>
      </view>
      <view class="info-row">
        <text>用餐位置:</text>
        <text>{{ tableNumber }}</text>
      </view>
    </view>

    <view class="tips">
      <text>📍 请到对应桌位就坐</text>
      <text>⏰ 商家正在准备您的订单</text>
    </view>

    <view class="btn-group">
      <view class="btn primary" @click="goHome">
        <text>返回首页</text>
      </view>
      <view class="btn secondary" @click="viewOrders">
        <text>查看订单</text>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      orderNumber: '',
      orderAmount: 0,
      paymentMethod: 'wechat',
      tableNumber: ''
    };
  },
  computed: {
    ...mapState(['apiBaseUrl'])
  },
  onLoad(options) {
    if (options.order_id) {
      this.loadOrder(options.order_id);
    }
  },
  methods: {
    async loadOrder(orderId) {
      try {
        const res = await uni.request({
          url: `${this.apiBaseUrl}/api/orders/${orderId}`
        });
        
        if (res.data) {
          this.orderNumber = res.data.order_number;
          this.orderAmount = res.data.final_amount;
          this.paymentMethod = res.data.payment_method || 'wechat';
          
          const table = uni.getStorageSync('currentTable');
          this.tableNumber = table ? table.table_number : '自提';
        }
      } catch (e) {
        console.error('加载订单失败', e);
      }
    },

    goHome() {
      uni.switchTab({
        url: '/pages/index/index'
      });
    },

    viewOrders() {
      uni.navigateTo({
        url: '/pages/orders/orders'
      });
    }
  }
};
</script>

<style>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60rpx 30rpx;
}

.success-icon {
  font-size: 120rpx;
}

.success-text {
  font-size: 40rpx;
  font-weight: bold;
  color: #07c160;
  margin-top: 20rpx;
}

.order-number {
  font-size: 24rpx;
  color: #999;
  margin-top: 16rpx;
}

.info-card {
  width: 100%;
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-top: 40rpx;
}

.info-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 16rpx 0;
  font-size: 28rpx;
  color: #666;
}

.amount {
  color: #ff4d4f;
  font-weight: bold;
}

.tips {
  margin-top: 40rpx;
  text-align: center;
}

.tips text {
  display: block;
  font-size: 26rpx;
  color: #999;
  margin-bottom: 10rpx;
}

.btn-group {
  display: flex;
  gap: 20rpx;
  margin-top: 60rpx;
  width: 100%;
}

.btn {
  flex: 1;
  padding: 24rpx;
  border-radius: 50rpx;
  text-align: center;
}

.btn.primary {
  background: #07c160;
}

.btn.primary text {
  color: #fff;
}

.btn.secondary {
  background: #fff;
  border: 2rpx solid #07c160;
}

.btn.secondary text {
  color: #07c160;
}
</style>
