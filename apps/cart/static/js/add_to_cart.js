$('#add_to_cart').on('submit',function(e){

  e.preventDefault();

  var data = $(this).serialize()
  // console.log(data)

  $.ajax({
   url : "/ajax/add_to_cart", // the endpoint
   type : "POST", // http method
   data : data,

   // Handle a successful response
   success : function(json) {
       // console.log(json);
       // console.log("success");

       if (json.add_to_cart == false) {
        $('#max_quantity').attr("style", "display: block!important");
        $('#max_quantity').fadeOut(speed=6000, easing="linear");

        } else {
          $('#max_quantity').attr("style", "display: none!important")
          $('#add_to_cart_button').html("<i class='far fa-check-circle mr-2'></i><b>Added</b>");
          $('#cart-items').html(json.items_in_cart);

        }

         }

  });

});

