$('#list-tab a').on('click', function (e) {
  e.preventDefault()
  $(this).tab('show')
})
var counter = 2
$('#bag-button').click(function() {
	if (counter % 2 == 0) {
		$('#bag-button-span').text("Hide your bag");
		$('#bag-button-icon').attr("class", "fas fa-chevron-up fa-xs ml-2");
		counter ++
	} else {
		$('#bag-button-span').text("View your bag");
		$('#bag-button-icon').attr("class", "fas fa-chevron-down fa-xs ml-2");
		counter ++
	}
	
})