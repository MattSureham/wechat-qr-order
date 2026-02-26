import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    cart: []
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
    },
    removeFromCart(state, productId) {
      const index = state.cart.findIndex(item => item.id === productId);
      if (index > -1) {
        state.cart.splice(index, 1);
      }
    },
    increaseQuantity(state, productId) {
      const item = state.cart.find(item => item.id === productId);
      if (item) {
        item.quantity++;
        item.subtotal = item.quantity * item.price;
      }
    },
    decreaseQuantity(state, productId) {
      const item = state.cart.find(item => item.id === productId);
      if (item && item.quantity > 1) {
        item.quantity--;
        item.subtotal = item.quantity * item.price;
      }
    },
    clearCart(state) {
      state.cart = [];
    }
  }
});

export default store;
