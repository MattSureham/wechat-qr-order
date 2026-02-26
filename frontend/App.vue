<script>
export default {
  onLaunch: function() {
    console.log('App Launch');
    
    // 获取设备信息
    uni.getSystemInfo({
      success: function(e) {
        // #ifndef MP
        Vue.prototype.StatusBar = e.statusBarHeight;
        if (e.customBar) {
          Vue.prototype.CustomBar = e.customBar;
        }
        // #endif
      }
    });
  },
  onShow: function() {
    console.log('App Show');
  },
  onHide: function() {
    console.log('App Hide');
  }
}
</script>

<style>
/* Base styles */
page {
  background-color: #f5f5f5;
  font-size: 28rpx;
}

.container {
  padding: 20rpx;
}
</style>
