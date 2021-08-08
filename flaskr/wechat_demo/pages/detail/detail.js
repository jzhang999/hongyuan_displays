// instance of the page
Page({
  data: {
    product_id: "",
    item: {},
    pics: []
  },
  onLoad(e) {
    let id = e.product_id;
    if (id === undefined) {
      this.setData({ product_id: JSON.stringify(wx.getStorageSync('productId')) });
    } else {
      this.setData({ product_id: id })
    }
    // this.setData({ product_id: JSON.stringify(wx.getStorageSync('productId')) })
    const that = this;
    wx.request({
      url: 'https://www.ningbohongyuan.com/product_search_id',
      method: "POST",
      data: {
        product_id: that.data.product_id,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ item: res.data[0] });
        that.setData({ pics: [that.data.item['pic_name0'], that.data.item['pic_name1'], that.data.item['pic_name2']] });
      }
    });
    wx.showShareMenu({ // share the page
      withShareTicket: true
    });
  },
  onShareAppMessage: function (e) {
    return {
      title: "鸿源美腾",  // title for share
      path: 'pages/detail/detail?product_id=' + this.data.product_id,
      success: function (res) {
      },
      fail: function (res) {
      }
    }
  }
});