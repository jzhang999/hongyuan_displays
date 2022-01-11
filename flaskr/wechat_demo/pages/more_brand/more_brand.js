Page({
  data: {
    items: [],
    brand_objs: []
  },
  onShow: function (options) {
    const that = this;
    wx.request({
      url: 'https://www.ningbohongyuan.com/get_all_brand_objs',
      method: "POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      dataType:'json',
      success(res) {
        that.setData({ brand_objs: res.data });
      }
    });
  },
  goBrand(e) {
    let brand_name = e.currentTarget.dataset.id;
    wx.setStorageSync('brandname', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../brand_search/brand_search',
    })
  },
});