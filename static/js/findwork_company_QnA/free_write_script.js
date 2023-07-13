  

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


