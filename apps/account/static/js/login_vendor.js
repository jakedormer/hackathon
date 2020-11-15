// $('#vendor_login').on('submit',function(e){

//   var data = $(this).serialize()
//   // console.log(data)

//   $.ajax({
//    url : "/login-vendor", // the endpoint
//    type : "POST", // http method
//    data : data,

//    // Handle a successful response
//    success : function(json) {
//        console.log(json);
//        // console.log("success");

//        if (json.token == true) {
//         localStorage.setItem('aveste_token', JSON.stringify(json.token));
//         } else {
//           $('#alert_login').text(json.error);
//           $('#alert_login').css('display', 'block')
//           } 
//         }
        

//   });

// });

document.addEventListener('DOMContentLoaded', function() {

    if (document.contentType == "application/json") {

      var json = JSON.parse(document.body.innerText)
      if (json.token) {
        console.log(json.token)
        localStorage.setItem('aveste_token', JSON.stringify(json.token));
        // window.close()
      }
    }

}, false);




