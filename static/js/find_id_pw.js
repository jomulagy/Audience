// function show_form_id() {
//     $("#form_find_id").show();
//     $("#form_find_pw").hide();
//     $(".find_id_button").css("background-color", "#FFBDBD");
//     $(".find_pw_button").css("background-color", "#FFE5E5");
// }

// function show_form_pw() {
//     $("#form_find_id").hide();
//     $("#form_find_pw").show();
//     $(".find_id_button").css("background-color", "#FFE5E5");
//     $(".find_pw_button").css("background-color", "#FFBDBD");
// }

function show_form_id(){
    var form_find_id = document.getElementById("form_find_id");
    var form_find_pw = document.getElementById("form_find_pw");
    var find_id_button = document.getElementById("find_id_button");
    var find_pw_button = document.getElementById("find_pw_button");
    
    form_find_id.style.display = "block";
    form_find_pw.style.display = "none";
    find_id_button.style.backgroundColor = "#FFBDBD";
    find_pw_button.style.backgroundColor = "#FFE5E5";
}

function show_form_pw(){
    var form_find_id = document.getElementById("form_find_id");
    var form_find_pw = document.getElementById("form_find_pw");
    var find_id_button = document.getElementById("find_id_button");
    var find_pw_button = document.getElementById("find_pw_button");
    
    form_find_id.style.display = "none";
    form_find_pw.style.display = "block";
    find_id_button.style.backgroundColor = "#FFE5E5";
    find_pw_button.style.backgroundColor = "#FFBDBD";
}