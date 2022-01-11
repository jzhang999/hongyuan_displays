Page({
  data: {
    items: [],
    cat_objs: []
  },
  onShow: function (options) {
    const that = this;
    wx.request({
      url: 'https://www.ningbohongyuan.com/get_all_cat_objs',
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