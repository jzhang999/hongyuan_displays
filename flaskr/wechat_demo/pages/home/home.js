// instance of the page
Page({
  data: {
    items: [],
    cat_objs: []
  },
  formSubmit(e) {
    wx.setStorageSync('searchKey', JSON.stringify(e.detail.value));
    wx.redirectTo({
      url: '../product_search/product_search'
    })
  },
  // handleTap_prod(e) {
  //   wx.redirectTo({
  //     url: '../product_search/product_search'
  //   })
  // },
  handleTap_more(e) {
    wx.redirectTo({
      url: '../more_rec/more_rec'
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
      url: 'http://127.0.0.1:5000/recommendation',
      method: "POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ items: res.data });
      }
    });
  },
  onShow: function (options) {
    const that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/get_all_cat_objs',
      method: "POST",
      success(res) {
        that.setData({ cat_objs: res.data });
      }
    });
  },
  goCategory(e) {
    let cat_name = e.currentTarget.dataset.id;
    wx.setStorageSync('catname', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../cat_search/cat_search',
    })
  },
});