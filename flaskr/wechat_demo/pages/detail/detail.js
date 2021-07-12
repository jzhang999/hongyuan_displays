// instance of the page
Page({
  data: {
    product_id: "",
    items: []
  },
  onLoad(e) {
    this.setData({ product_id: JSON.stringify(wx.getStorageSync('productId')) })
    const that = this;
    wx.request({
      url: 'http://172.20.1.246:5000/product_search_id',
      method: "POST",
      data: {
        product_id: that.data.product_id,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ items: res.data });
      }
    });
    wx.showShareMenu({ // share the page
      withShareTicket: true
    });
  },
  onShareAppMessage: function (ops) {
    if (ops.from === 'button') {
    }
    return {
      title: "鸿源美腾",  // title for share
      path: 'pages/detail/detail',
      success: function (res) {
      },
      fail: function (res) {
      }
    }
  }
});