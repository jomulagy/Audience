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
    $("#form_find_pw").hide();
    $("#form_find_id").show();
    $("#form_show_user_id").hide();
    $("#form_show_user_pw").hide();
    $("#find_id_button").css("background-color", "#FFBDBD");
    $("#find_pw_button").css("background-color", "#FFE5E5");
}

function show_form_pw(){
    $("#form_find_id").hide();
    $("#form_find_pw").show();
    $("#form_show_user_id").hide();
    $("#form_show_user_pw").hide();
    $("#find_id_button").css("background-color", "#FFE5E5");
    $("#find_pw_button").css("background-color", "#FFBDBD");
}

function show_id_result(){
    $("#form_show_user_id").show();
    $("#form_find_id").hide();


}
function show_pw_result(){
    $("#form_show_user_pw").show();
    $("#form_find_id").hide();
    $("#form_find_pw").hide();
}

//json
//아이디 찾기
function findId(){
    var namee = $('#name').val();
    var subname = $('#subname').val();

    $.ajax({
        type : 'POST',
        url : "/account/username/search/",
        data: JSON.stringify({
            "name" : namee,
            "subname" : subname
        }),
        success : function(data){
            show_id_result();

            var showBox = document.querySelector('.show_box_id');
            showBox.innerHTML = '아이디: ' + data.username;

        }, error: function(){
            console.log('실패');
        }
    })
}


//비밀번호 찾기
function findPw(){
    var email = $('#username').val();
    //비밀번호 찾기
    $.ajax({
        type : 'POST',
        url : "/account/password/search/",
        data: JSON.stringify({
            "username" : email
        }),
        success : function(data){
            show_pw_result();
            var showBox = document.querySelector('.show_box_pw');
            $("<p>").text("아이디로 메일을 보냈습니다.").appendTo(showBox);
            $("<p>").text("메일을 통해 비밀번호를 변경해주십시오.").appendTo(showBox);
            
        }, error: function(){
            console.log('실패');
        }
    })      
}