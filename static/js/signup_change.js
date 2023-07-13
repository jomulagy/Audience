// jquery 사용해서  radio , checkbox 의 체크여부 확인하기

// $('input:radio[name=이름]').is(':checked');

// $('input:checkbox[name=이름]').is(':checked');

// 결과는  true / false 로 나옴.

function button_1() {
    $('input[name="gender"]').change(function () {
      $('input[name="gender"]').each(function () {
        var checked = $(this).prop("checked"); 
        // var checked = $(this).attr('checked');   
        // var checked = $(this).is('checked');
        var $label = $(this).next();
  
        if (checked) $label.css("background-color", "#FFBDBD");
        else $label.css("background-color", "#FFE5E5");
      });
    });
}

function button_2() {
    $('input[name="interest"]').change(function () {
      $('input[name="interest"]').each(function () {
        var checked = $(this).prop("checked");
        // var checked = $(this).attr('checked');   
        // var checked = $(this).is('checked');
        var label1 = $(this).next().next().next().next().next().next();
        var label2 = $(label1).next().next().next().next().next().next();
        var $label = $(label2).next().next().next().next().next().next();
  
        if (checked) $label.css("background-color", "#FFBDBD");
        else $label.css("background-color", "#FFE5E5");
      });
    });
}

function button_3() {
    $('input[name="school"]').change(function () {
      $('input[name="school"]').each(function () {
        var checked = $(this).prop("checked"); 
        // var checked = $(this).attr('checked');   
        // var checked = $(this).is('checked');
        var $label = $(this).next().next().next().next().next().next();
  
        if (checked) $label.css("background-color", "#FFBDBD");
        else $label.css("background-color", "#FFE5E5");
      });
    });
}

function display_filename(input) {
    var file = input.files[0];
    var filename = document.getElementById("filename");
    if (file) {
        filename.textContent = file.name;
    }
}

function checkagain(){
  $.ajax({
    type : 'POST',
    url : "/",
    data : JSON.stringify({
      "username" : email
    }),
    success : function(data){
      //사용 불가 안내무구
      if (data.true == exist_company){
        $("p.error_message").text("이미 존재하는 회사 이름입니다.");
      }
      else if(data.true == exist_username){
        $("p.error_message").text("이미 존재하는 아이디입니다.");
      }
      else if(data.true == exist_nickname){
        $("p.error_message").text("이미 존재하는 닉네임입니다.");
      }
      //사용 가능하다는 안내문구
      else if(data.true == no_exist_username){
        $("p.able_message").text("사용 가능한 아이디입니다.");
      }
      else if(data.true == no_exist_company){
        $("p.able_message").text("사용 가능한 회사이름입니다.");
      }
      else if(data.true == no_exist_nickname){
        $("p.able_message").text("사용 가능한 닉네임입니다.");
      }
      
    }
  })
}