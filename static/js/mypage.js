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