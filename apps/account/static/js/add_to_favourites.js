$('#add_to_favourites').on('submit',function(e){

  e.preventDefault();

  var data = $(this).serialize()
  console.log(data)

  $.ajax({
   url : "/ajax/add_to_favourites", // the endpoint
   type : "POST", // http method
   data : data,

   // Handle a successful response
   success : function(json) {
       console.log(json);
       console.log("success");

       if (json.add_to_favourites == false) {
        $('#add_to_favourites_button').attr("class", "btn btn-warning btn-sm op-50");
        $('#add_to_favourites_button').attr("title", "Add this brand to your favourites");

        } else {
        $('#add_to_favourites_button').attr("class", "btn btn-warning btn-sm");
        $('#add_to_favourites_button').attr("title", "Remove this brand from your favourites");

        }

         }

  });

});