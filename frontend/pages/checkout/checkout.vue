<template>
  <view class="container">
    <!-- 订单信息 -->
    <view class="section">
      <view class="section-title">订单信息</view>
      <view class="order-items">
        <view v-for="item in cart" :key="item.id" class="order-item">
          <text class="item-name">{{ item.name }}</text>
          <text class="item-quantity">x{{ item.quantity }}</text>
          <text class="item-price">¥{{ item.subtotal }}</text>
        </view>
      </view>
    </view>

    <!-- 桌位信息 -->
    <view class="section" v-if="currentTable">
      <view class="section-title">用餐位置</view>
      <view class="info-row">
        <text>{{ currentTable.table_number }}号桌</text>
      </view>
    </view>

    <!-- 备注 -->
    <view class="section">
      <view class="section-title">订单备注</view>
      <textarea 
        class="remark-input" 
        v-model="remark" 
        placeholder="请输入备注（如：少辣、忌口等）"
        maxlength="200"
      />
    </view>

    <!-- 支付方式 -->
    <view class="section">
      <view class="section-title">支付方式</view>
      <view class="payment-methods">
        <view 
          class="method-item" 
          :class="{ active: paymentMethod === 'wechat' }"
          @click="paymentMethod = 'wechat'"
        >
          <text class="method-icon">💚</text>
          <text>微信支付</text>
        </view>
        <view 
          class="method-item" 
          :class="{ active: paymentMethod === 'alipay' }"
          @click="paymentMethod = 'alipay'"
        >
          <text class="method-icon">💙</text>
          <text>支付宝</text>
        </view>
      </view>
    </view>

    <!-- 底部栏 -->
    <view class="footer">
      <view class="total-info">
        <text class="label">合计:</text>
        <text class="amount">¥{{ cartTotal }}</text>
      </view>
      <view class="pay-btn" @click="submitOrder">
        <text>提交订单</text>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

export default {
  data() {
    return {
      remark: '',
      paymentMethod: 'wechat',
      currentTable: null
    };
  },
  computed: {
    ...mapState(['cart']),
    ...mapGetters(['cartTotal'])
  },
  onLoad() {
    this.currentTable = uni.getStorageSync('currentTable') || null;
  },
  methods: {
    async submitOrder() {
      if (this.cart.length === 0) {
        uni.showToast({ title: '购物车为空', icon: 'none' });
        return;
      }

      uni.showLoading({ title: '提交中...' });

      try {
        // 创建订单
        const orderData = {
          table_id: this.currentTable?.id || 1,
          items: this.cart.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            unit_price: item.price,
            subtotal: item.subtotal
          })),
          remark: this.remark,
          discount_amount: 0
        };

        const res = await uni.request({
          url: 'http://localhost:8000/api/orders',
          method: 'POST',
          data: orderData
        });

        if (res.data && res.data.id) {
          // 模拟支付
          await this.processPayment(res.data.id);
        }
      } catch (e) {
        console.error('提交订单失败', e);
        uni.showToast({ title: '提交失败', icon: 'none' });
      } finally {
        uni.hideLoading();
      }
    },

    async processPayment(orderId) {
      uni.showLoading({ title: '支付中...' });

      try {
        // 模拟支付成功
        await new Promise(resolve => setTimeout(resolve, 1500));

        const payRes = await uni.request({
          url: `http://localhost:8000/api/orders/${orderId}/pay`,
          method: 'PUT',
          data: {
            payment_method: this.paymentMethod,
            transaction_id: 'SIM' + Date.now()
          }
        });

        if (payRes.data && payRes.data.status === 'paid') {
          // 清除购物车
          this.$store.commit('clearCart');

          uni.showToast({ title: '支付成功', icon: 'success' });

          setTimeout(() => {
            uni.redirectTo({
              url: `/pages/order-success/order-success?order_id=${orderId}`
            });
          }, 1500);
        }
      } catch (e) {
        console.error('支付失败', e);
        uni.showToast({ title: '支付失败', icon: 'none' });
      }
    }
  }
};
</script>

<style>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 140rpx;
}

.section {
  background: #fff;
  margin-bottom: 20rpx;
  padding: 30rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.order-item {
  display: flex;
  align-items: center;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}

.order-item:last-child {
  border-bottom: none;
}

.item-name {
  flex: 1;
  font-size: 28rpx;
}

.item-quantity {
  color: #999;
  margin: 0 20rpx;
}

.item-price {
  color: #333;
  width: 150rpx;
  text-align: right;
}

.info-row {
  font-size: 28rpx;
  color: #666;
}

.remark-input {
  width: 100%;
  height: 150rpx;
  padding: 20rpx;
  background: #f9f9f9;
  border-radius: 12rpx;
  font-size: 28rpx;
}

.payment-methods {
  display: flex;
  gap: 20rpx;
}

.method-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30rpx;
  border: 2rpx solid #eee;
  border-radius: 12rpx;
  font-size: 28rpx;
}

.method-item.active {
  border-color: #07c160;
  color: #07c160;
}

.method-icon {
  margin-right: 10rpx;
  font-size: 36rpx;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120rpx;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.1);
}

.total-info {
  flex: 1;
}

.label {
  font-size: 28rpx;
  color: #666;
}

.amount {
  font-size: 40rpx;
  color: #ff4d4f;
  font-weight: bold;
  margin-left: 10rpx;
}

.pay-btn {
  background: #07c160;
  padding: 24rpx 80rpx;
  border-radius: 50rpx;
}

.pay-btn text {
  color: #fff;
  font-size: 32rpx;
}
</style>
