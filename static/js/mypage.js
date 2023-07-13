// const mypageButton1 = document.getElementById("mypage_button_1");
// const mypageButton2 = document.getElementById("mypage_button_2");
// 스타일 변경
// mypageButton1.style.backgroundColor = "#FFDCDC";
console.log(interests)

function show_mypage1() {
    $("#mypage_1").show();
    $("#mypage_2").hide();
    $("#mypage_button_1").css("background-color", "#FFDCDC");
    $("#mypage_button_2").css("background-color", "#FFFFFF");
    for (var i=0; i < interests;i++){
        console.log(interests[i]);
        $("label[value='" + interests[i] + "']").css("background-color", "#FFBDBD");
    }
}

function show_mypage2() {
    $("#mypage_1").hide();
    $("#mypage_2").show();
    $("#mypage_button_1").css("background-color", "#FFFFFF");
    $("#mypage_button_2").css("background-color", "#FFDCDC");
    // $("<a>").text(data.title).class("notice_title").id(data.id).appendTo(notice);
    // $("<a>").text(data.views).class("views").id(data.id).appendTo(notice);     
    $.ajax({
        type : 'GET',
        url : "/account/posts/detail/",
        data: JSON.stringify({

        }),
        success : function(data){
            // console.log("111");
            var notice = document.querySelector('.notice');
            var posts = data.posts;
            $("a.notice_title").text(posts[1]).id(posts[0]).text(posts[1]).appendTo(notice);
            $("a.views").text(posts[1]).id(posts[0]).text(posts[2] + "회").appendTo(notice);            
        }
    })
       
    
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