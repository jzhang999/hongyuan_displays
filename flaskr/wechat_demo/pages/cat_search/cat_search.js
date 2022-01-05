// instance of the page
Page({
  data: {
    search_key: "",
    items: [],
    cat_array: [],
    index: 0
  },
  bindPickerChange(e) {
    this.setData({ search_key: JSON.stringify(this.data.cat_array[e.detail.value]) });
    this.setData({ index: e.detail.value });
    const that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/cat_search',
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
  },
  onLoad(e) {
    const that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/get_all_cats',
      method: "POST",
      success(res) {
        that.setData({ cat_array: res.data });
      }
    });
  }
});