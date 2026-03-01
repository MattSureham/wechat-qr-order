import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

// 从本地存储加载购物车数据
const loadCartFromStorage = () => {
  try {
    const cart = uni.getStorageSync('cart');
    return cart ? JSON.parse(cart) : [];
  } catch (e) {
    console.error('Failed to load cart from storage:', e);
    return [];
  }
};

// 保存购物车到本地存储
const saveCartToStorage = (cart) => {
  try {
    uni.setStorageSync('cart', JSON.stringify(cart));
  } catch (e) {
    console.error('Failed to save cart to storage:', e);
  }
};

const store = new Vuex.Store({
  state: {
    cart: loadCartFromStorage(),
    // API配置
    apiBaseUrl: 'http://localhost:8000'
  },
  getters: {
    cartItemCount: state => {
      return state.cart.reduce((total, item) => total + item.quantity, 0);
    },
    cartTotal: state => {
      return state.cart.reduce((total, item) => total + item.subtotal, 0).toFixed(2);
    }
  },
  mutations: {
    addToCart(state, product) {
      const existingItem = state.cart.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity++;
        existingItem.subtotal = existingItem.quantity * existingItem.price;
      } else {
        state.cart.push({
          id: product.id,
          name: product.name,
          price: product.price,
          quantity: 1,
          subtotal: product.price
        });
      }
      // 持久化到本地存储
      saveCartToStorage(state.cart);
    },
    removeFromCart(state, productId) {
      const index = state.cart.findIndex(item => item.id === productId);
      if (index > -1) {
        state.cart.splice(index, 1);
      }
      // 持久化到本地存储
      saveCartToStorage(state.cart);
    },
    increaseQuantity(state, productId) {
      const item = state.cart.find(item => item.id === productId);
      if (item) {
        item.quantity++;
        item.subtotal = item.quantity * item.price;
      }
      // 持久化到本地存储
      saveCartToStorage(state.cart);
    },
    decreaseQuantity(state, productId) {
      const item = state.cart.find(item => item.id === productId);
      if (item && item.quantity > 1) {
        item.quantity--;
        item.subtotal = item.quantity * item.price;
      }
      // 持久化到本地存储
      saveCartToStorage(state.cart);
    },
    clearCart(state) {
      state.cart = [];
      // 持久化到本地存储
      saveCartToStorage(state.cart);
    },
    setApiBaseUrl(state, url) {
      state.apiBaseUrl = url;
    }
  }
});

export default store;
