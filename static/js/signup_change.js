// jquery 사용해서  radio , checkbox 의 체크여부 확인하기

// $('input:radio[name=이름]').is(':checked');

// $('input:checkbox[name=이름]').is(':checked');

// 결과는  true / false 로 나옴.
$(document).ready(function(){
  $.ajax({
    type: "GET",
    url: "/account/info/",
    success:function(data){
        var gender = data["gender"]
        console.log(gender)
        if(gender){
          var target = $("input[name='gender'][value='"+gender+"']");
          var num = $(target).attr("id").replace('gender_', '');
          $("#old_gender_label_"+num).click();
          console.log($("#old_gender_label_"+num))
        }
        var interests = data["interests"]
        for(var interest of interests){
          var target = $("input[name='interest'][value='"+interest+"']");
          var num = $(target).attr("id").replace('checkbox', '');
          $("#old_label_"+num).click();
        }

        var school = data["school"]
        if(school){
          var target = $("input[name='school'][value='"+school+"']");
          var num = $(target).attr("id").replace('aca_checkbox', '');
          $("#old_aca_label_"+num).click();
        }
        
    },
    error : function(xhr,errmsg,err) {
    console.log(xhr.status + ": " + xhr.responseText);
    }
  });
})

function button_1() {
  
    $('input[name="gender"]').change(function () {
      console.log(this)

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

function checkagain(type){
  //아이디 중복 체크
  if(type === "email"){
    $("#id_msg").css("display","none");
    $("#id_err").css("display","none");
    $("#id-format-err").css("display","none");
    var email = $("#id_input").val();

    $.ajax({
      type : 'POST',
      url : "/account/username/check/",
      data : JSON.stringify({
        "username" : email
      }),
      success : function(data){
        console.log(data.success)
        //중복
        if(data.success === "exist_username"){
          $("#id_err").text("이미 존재하는 아이디입니다.");
          $("#id_err").css("display","block")
        }

        //사용 가능하다는 안내문구
        else if(data.success === "no_exist_username"){
          $("#id_msg").text("사용 가능한 아이디입니다.");
          $("#id_msg").css("display","block")
        }

        //형식이 맞지 않을때
        else if(data.success === "Invalid email format"){
          $("#id_err").text("아이디가 email 형식이 아닙니다.");
          $("#id_err").css("display","block")
        }
        
      }
    })
  }
  //닉네임 중복 체크
  else if(type === "nickname"){
    $("#nickname-msg").css("display","none");
    $("#nickname-err").css("display","none");
    $("#nickname-required").css("display","none");
    var nickname = $("#nickname-input").val();

    $.ajax({
      type : 'POST',
      url : "/account/nickname/check/",
      data : JSON.stringify({
        "nickname" : nickname
      }),
      success : function(data){
        console.log(data.success)
        //사용 불가 안내무구

        if(data.success === "exist_nickname"){
          $("#nickname-err").text("이미 존재하는 닉네임입니다.");
          $("#nickname-err").css("display","block")
        }

        //사용 가능하다는 안내문구
        else if(data.success === "no_exist_nickname"){
          $("#nickname-msg").text("사용 가능한 닉네임입니다.");
          $("#nickname-msg").css("display","block")
        }
        
      }
    })
  }

  else if(type === "company"){
    $("#company-msg").css("display","none");
    $("#company-err").css("display","none");
    $("#company-required").css("display","none");
    var company = $("#company-input").val();

    $.ajax({
      type : 'POST',
      url : "/account/company/check/",
      data : JSON.stringify({
        "company" : company
      }),
      success : function(data){
        console.log(data.success)
        //사용 불가 안내무구

        if(data.success === "exist_company"){
          $("#company-err").css("display","block")
        }

        //사용 가능하다는 안내문구
        else if(data.success === "no_exist_company"){
          $("#company-msg").css("display","block")
        }
        
      }
    })
  }
  
}