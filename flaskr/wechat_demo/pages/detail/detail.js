// instance of the page
Page({
  data: {
    product_id: "",
    item: {},
    pics: []
  },
  onLoad(e) {
    const that = this;
    wx.request({
      url: 'https://ningbohongyuan.com/product_search_id',
      method: "POST",
      data: {
        product_id: e.product_id,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ product_id: e.product_id });
        that.setData({ item: res.data[0] });
        that.setData({ pics: [that.data.item['pic_name0'], that.data.item['pic_name1'], that.data.item['pic_name2']] });
      }
    });
    wx.showShareMenu({ // share the page
      withShareTicket: true
    });
  },
  onShareAppMessage: function (ops) {
    if (ops.from === 'image') {
    }
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