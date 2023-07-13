// const mypageButton1 = document.getElementById("mypage_button_1");
// const mypageButton2 = document.getElementById("mypage_button_2");
// 스타일 변경
// mypageButton1.style.backgroundColor = "#FFDCDC";

function show_mypage1() {
    $("#mypage_1").show();
    $("#mypage_2").hide();
    $("#mypage_button_1").css("background-color", "#FFDCDC");
    $("#mypage_button_2").css("background-color", "#FFFFFF");
}

function show_mypage2() {
    $("#mypage_1").hide();
    $("#mypage_2").show();
    $("#mypage_button_1").css("background-color", "#FFFFFF");
    $("#mypage_button_2").css("background-color", "#FFDCDC");
}

// function button_2() {
//     $('input[name="interest"]').change(function () {
//       $('input[name="interest"]').each(function () {
//         var checked = $(this).prop("checked"); 
//         // var checked = $(this).attr('checked');   
//         // var checked = $(this).is('checked');
//         var label1 = $(this).next().next().next().next().next().next();
//         var label2 = $(label1).next().next().next().next().next().next();
//         var $label = $(label2).next().next().next().next().next().next();
  
//         if (checked) $label.css("background-color", "#FFBDBD");
//         else $label.css("background-color", "#FFE5E5");
//       });
//     });
// }