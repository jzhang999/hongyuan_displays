Page({
  data: {
    modalHidden: true
  },
  onShow: function() {
    this.setData({
      modalHidden: false
    })
  },
  modalCandel: function() {
    this.setData({
      modalHidden: true
    })
  },
  modalConfirm: function() {
    this.setData({
      modalHidden: true
    })
  },
  call_service() {
    wx.makePhoneCall({
      phoneNumber: '13306843920',
    })
  },
  call_line() {
    wx.makePhoneCall({
      phoneNumber: '13615743310',
    })
  }
}); // instance of the page