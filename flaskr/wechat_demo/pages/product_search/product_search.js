// instance of the page
Page({
  data: {
    search_key: "",
    items: []
  },
  formSubmit(e) {
    this.setData({ search_key: JSON.stringify(e.detail.value) })
    const that = this;
    wx.request({
      url: 'https://ningbohongyuan.com/product_search',
      method: "POST",
      data: {
        search_key: that.data.search_key,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ items: res.data });
      }
    });
  },
  goDetail(e) {
    let id = e.currentTarget.dataset.id;
    wx.setStorageSync('productId', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../detail/detail',
    })
  }
});