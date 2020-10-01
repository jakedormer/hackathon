$('#size_guide_apply_form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check

});

$('#size_guide_apply').on('change',function(e){
  var prev = $(this).find("selected").text();
  console.log("jake");

  $.ajax({
         url : "/ajax/apply_size_guide", // the endpoint
         type : "POST", // http method
         data : { 
            size_guide: '',
            product : $('#post-text').val(),

            }, // data sent with the post request

         // handle a successful response
         success : function(json) {
             $('#post-text').val(''); // remove the value from the input
             console.log(json); // log the returned json to the console
             console.log("success"); // another sanity check
         }
  // console.log("form submitted");

          });
});

