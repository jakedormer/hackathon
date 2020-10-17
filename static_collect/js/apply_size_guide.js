

$('.size_guide_apply_form').each(function() {


    $(this).find('#size_guide_apply').on('change',function(e){

      var data = $(this).parent().parent().serialize()
      console.log(data)

      $.ajax({
       url : "/ajax/apply_size_guide", // the endpoint
       type : "POST", // http method
       data : data,

       // Handle a successful response
       success : function(json) {
           console.log(json); // log the returned json to the console
           console.log("success"); // another sanity check
             }
      });

    });
});


