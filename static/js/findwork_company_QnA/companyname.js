$(function() {
  $("#submit_button").click(function() {
    const inputName = $("#name").val();
    $.ajax({
      type: 'POST',
      dataType: 'json',
      data : JSON.stringify({"name":inputName}),
      url: "/job/company/search/",
      contentType: 'application/json',
      error: function (err) {
        console.log("실행중 오류가 발생하였습니다.");
      },
      success: function (data) {
        $('#suggestion_box').removeClass("invisible")
        $('#suggestion_box').css("display","flex")
        for (const company of data["companies"]) {
          var newDiv = $('<div>').addClass('suggested_items').text(company);
          $(newDiv).click(function(){
            $("#search-company").val($(this).text())
            clearModal();
          })
          $('#suggestion_box').append(newDiv);
      }
      }
    })
    
    $("#company_name").val(inputName);
    $("#suggestion_box").addClass("invisible");
  });
});
function clearModal(){
  $('#name').val("");
  $('#suggestion_box').empty();
  $('#suggestion_box').addClass("invisible")
  $('#suggestion_box').css("display","none")
  $('.search_wrapper').css("display","none")
  $(".container").removeClass("blurred")

}