$.ajax({
  url: '/ajax/apply_size_guide/',
  data: {
    'username': 'jake'
  },
  dataType: 'json',
  success: function (data) {
    if (data.updated) {
      alert("Product Updated");
    }
  }
});