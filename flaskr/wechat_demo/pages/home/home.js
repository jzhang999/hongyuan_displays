// instance of the page
Page({
  data: {
    items: [],
    cat_objs: [],
    brand_objs: [],
    autoplay: true,
    interval: 3000
  },
  formSubmit(e) {
    wx.setStorageSync('searchKey', JSON.stringify(e.detail.value));
    wx.redirectTo({
      url: '../product_search/product_search'
    })
  },
  handleTap_rec_more(e) {
    wx.redirectTo({
      url: '../more_rec/more_rec'
    })
  },
  handleTap_cat_more(e) {
    wx.redirectTo({
      url: '../more_cat/more_cat'
    })
  },
  handleTap_brand_more(e) {
    wx.redirectTo({
      url: '../more_brand/more_brand'
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
      url: 'https://www.ningbohongyuan.com/recommendation',
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
      url: 'https://www.ningbohongyuan.com/get_all_cat_objs',
      method: "POST",
      success(res) {
        that.setData({ cat_objs: res.data });
      }
    });
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
  goCategory(e) {
    let cat_name = e.currentTarget.dataset.id;
    wx.setStorageSync('catname', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../cat_search/cat_search',
    })
  },
  goBrand(e) {
    let brand_name = e.currentTarget.dataset.id;
    wx.setStorageSync('brandname', e.currentTarget.dataset.id);
    wx.navigateTo({
      url: '../brand_search/brand_search',
    })
  },
});