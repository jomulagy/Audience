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

function show_id_result(){
    var form_find_id = document.getElementById("form_show_user");
    var form_find_pw = document.getElementById("form_find_id");
    
    form_find_id.style.display = "block";
    form_find_pw.style.display = "none";
}
function show_pw_result(){
    var form_find_id = document.getElementById("form_find_pw");
    var form_find_pw = document.getElementById("form_show_user");
    
    form_find_id.style.display = "none";
    form_find_pw.style.display = "block";
}

//json
var namee = $('#name').val();
var nickname = $('#nickname').val();
var email = $('#id').val();
$.ajax({
    type : 'POST',
    url : "/account/username/search/",
    data: JSON.stringify({
        "email" : email,
        "name" : namee
    }),
    success : function(data){
        show_id_result();
    }
})

$.ajax({
    type : 'POST',
    url : "/account/password/search/",
    data: JSON.stringify({
        "username" : username
    }),
    success : function(data){
        show_pw_result();
    }
})