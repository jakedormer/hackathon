$('#size_guide_apply_form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check

});

$('#size_guide_apply_form').find('#size_guide_apply').on('change',function(e){
  
  // var prev = $(this).val();
  // console.log(prev);

  $.ajax({
   url : "/ajax/apply_size_guide", // the endpoint
   type : "POST", // http method
   data : $("#size_guide_apply_form").serialize(),

   // handle a successful response
   success : function(json) {
       console.log(json); // log the returned json to the console
       console.log("success"); // another sanity check
       $("body").css("cursor", "progress");
         }
  });
  // console.log("form submitted");

});


