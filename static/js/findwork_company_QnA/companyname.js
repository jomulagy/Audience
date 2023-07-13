$(function() {
  $("#submit_button").click(function() {
    const inputName = $("#name").val();
    $("#company_name").val(inputName);
    $("#suggestion_box").addClass("invisible");
  });
});
