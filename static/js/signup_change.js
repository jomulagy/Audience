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