// instance of the page
Page({
  data: {
    items: []
  },
  handleTap_cat(e) {
    wx.redirectTo({
      url: '../cat_search/cat_search'
    })
  },
  handleTap_prod(e) {
    wx.redirectTo({
      url: '../product_search/product_search'
    })
  },
  goDetail(e) {
    let id = e.currentTarget.dataset.id;
    wx.setStorageSync('productId', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../detail/detail',
    })
  },
  onLoad(e) {
    const that = this;
    wx.request({
      url: 'http://0.0.0.0:5000/recommendation',
      method: "POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ items: res.data });
      }
    });
  }
});