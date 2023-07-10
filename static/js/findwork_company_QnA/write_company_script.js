
// 버튼 요소 가져오기
var button1 = document.getElementsByClassName('intern_btn');

// 각 버튼에 대해 이벤트 핸들러 추가
for (var i = 0; i < button1.length; i++) {
  button1[i].addEventListener('click', function() {
    // 현재 클릭된 버튼의 클래스를 변경하여 활성화 상태를 표시
    this.classList.toggle('active');
  });
}

// 버튼 요소 가져오기
var button2 = document.getElementsByClassName('permanent_btn');

// 각 버튼에 대해 이벤트 핸들러 추가
for (var i = 0; i < button2.length; i++) {
  button2[i].addEventListener('click', function() {
    // 현재 클릭된 버튼의 클래스를 변경하여 활성화 상태를 표시
    this.classList.toggle('active');
  });
}

// 버튼 요소 가져오기
var button3 = document.getElementsByClassName('temporary_btn');

// 각 버튼에 대해 이벤트 핸들러 추가
for (var i = 0; i < button3.length; i++) {
  button3[i].addEventListener('click', function() {
    // 현재 클릭된 버튼의 클래스를 변경하여 활성화 상태를 표시
    this.classList.toggle('active');
  });
}

// 버튼 요소 가져오기
var button4 = document.getElementsByClassName('newcomer_btn');

// 각 버튼에 대해 이벤트 핸들러 추가
for (var i = 0; i < button4.length; i++) {
  button4[i].addEventListener('click', function() {
    // 현재 클릭된 버튼의 클래스를 변경하여 활성화 상태를 표시
    this.classList.toggle('active');
  });
}

// 버튼 요소 가져오기
var button5 = document.getElementsByClassName('experienced_btn');

// 각 버튼에 대해 이벤트 핸들러 추가
for (var i = 0; i < button5.length; i++) {
  button5[i].addEventListener('click', function() {
    // 현재 클릭된 버튼의 클래스를 변경하여 활성화 상태를 표시
    this.classList.toggle('active');
  });
}

var fileInput = document.getElementById('upload-input');
var previewContainer = document.getElementById('preview-container');
var previewImage = document.createElement('img');
previewImage.id = 'preview-image';

fileInput.addEventListener('change', function(event) {
  var file = event.target.files[0];
  var reader = new FileReader();

  reader.onload = function(event) {
    var imageUrl = event.target.result;
    previewImage.src = imageUrl;
    previewContainer.appendChild(previewImage);
  };

  reader.readAsDataURL(file);
});


function handleInput(event) {
  var input = event.target.value;
  event.target.value = input.replace(/[^0-9]/g, '');
}

var startDateInput = document.getElementById("start-date");
    flatpickr(startDateInput, {
      dateFormat: "Y-m-d",
      onChange: function(selectedDates) {
        var endDateInput = document.getElementById("end-date");
        var endDatePicker = flatpickr(endDateInput);
        endDatePicker.set("minDate", selectedDates[0]);
      }
    });

    // 마감일자 선택
    var endDateInput = document.getElementById("end-date");
    flatpickr(endDateInput, {
      dateFormat: "Y-m-d",
      onChange: function(selectedDates) {
        var startDateInput = document.getElementById("start-date");
        var startDatePicker = flatpickr(startDateInput);
        startDatePicker.set("maxDate", selectedDates[0]);
      }
    });

    var tagContainer = document.getElementById("tag-container");
var inputContainer = document.getElementById("input-container");
var maxTags = 5; // 최대 태그 개수

function handleKeyDown(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    addTag();
  }
}

function addTag() {
  var input = document.getElementById("tag-input");
  var tagText = input.value.trim();
  if (tagText !== "") {
    var tags = tagText.split("#").filter(Boolean);

    tags.forEach(function(tag) {
      if (tagContainer.childElementCount < maxTags) {
        createTagInput(tag);
      }
    });

    input.value = "";
  }
}

function createTagInput(tag) {
  var input = document.createElement("input");
  input.type = "text";
  input.value = "#" + tag;
  input.className = "tag-input";
  input.onclick = function() {
    var newTag = prompt("해시태그 수정:", tag);
    if (newTag !== null) {
      input.value = "#" + newTag;
      adjustInputWidth(input); // 수정된 값에 따라 너비 조정
    }
  };

  tagContainer.appendChild(input);
  adjustInputWidth(input);

  // 버튼 위치 제한
  var lastInput = tagContainer.lastElementChild;
  var leftPosition = lastInput.getBoundingClientRect().left;
  if (leftPosition + lastInput.offsetWidth > 600) {
    tagContainer.style.flexWrap = "wrap";
    input.style.marginTop = "10px";
  }
}

function adjustInputWidth(input) {
  var tagText = input.value;
  var tempSpan = document.createElement("span");
  tempSpan.style.visibility = "hidden";
  tempSpan.style.whiteSpace = "nowrap";
  tempSpan.innerHTML = tagText;
  document.body.appendChild(tempSpan);

  var width = tempSpan.offsetWidth * 1.4 + 10;
  input.style.width = width + "px";

  document.body.removeChild(tempSpan);
}

document.getElementById("tag-input").addEventListener("keydown", handleKeyDown);


