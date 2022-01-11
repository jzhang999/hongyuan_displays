// instance of the page
Page({
  data: {
    search_key: "",
    items: []
    // cat_name_array: [],
    // index: 0
  },
  goDetail(e) {
    let id = e.currentTarget.dataset.id;
    wx.setStorageSync('productId', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../detail/detail',
    })
  },
  onLoad(e) {
    let id = e.search_key;
    if (id === undefined) {
      this.setData({ search_key: JSON.stringify(wx.getStorageSync('brandname')) });
    } else {
      this.setData({ search_key: id })
    }

    const that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/brand_search',
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
  }
});