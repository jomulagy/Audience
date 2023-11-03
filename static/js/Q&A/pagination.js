var linePosts;
var url = location.href
var urlParts = url.split("/")
var currentPage = 1;
var totalPages
var buttonCount;
const buttonSize = 30;
function loadQAList(page_num) {


  $.ajax({
    url: 'http://127.0.0.1:8000/employ/question/list/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({
      "post_id": urlParts[6],
      "page_num": page_num
    }),
    contentType: 'application/json',
    success: function (response) {
      linePosts = response.QA_List;
    },
    error: function (xhr, textStatus, error) {
      console.log('Q&A 리스트 불러오기 에러:', error);
    }
  });
}

function checkPosts() {
  if (typeof linePosts !== "undefined") {
    // "posts"가 정의되면 원하는 작업을 수행
    console.log("success : ", linePosts.length)
    lineShowPosts();
    buttonCount = linePosts.length
    totalPages = Math.floor(buttonCount / 4)+1;
    console.log(totalPages)
    renderButton()
  } else {
    // "posts"가 아직 정의되지 않았으면 재귀적으로 확인
    setTimeout(checkPosts, 1000); // 1초마다 확인
    console.log("failed")
  }
}

function lineShowPosts() {
  console.log(linePosts)
  var linePostList = document.getElementById("linePostList");
  linePostList.innerHTML = "";

  for (var i = 0; i < 5 && i < linePosts.length; i++) {
    var linePost = linePosts[i];
    var linePostElement = document.createElement("div");
    linePostElement.classList.add("linePost");
    linePostElement.id = linePost.id

    var lineTitleElement = document.createElement("h2");
    lineTitleElement.classList.add("linePost-title");
    lineTitleElement.textContent = linePost.title;

    var lineDateElement = document.createElement("h3");
    lineDateElement.classList.add("linePost-date");
    var dateString = linePost.created_at;
    var formattedDate = dateFormat(dateString);
    
    lineDateElement.textContent = formattedDate;

    var linkElement = document.createElement("a");
    linkElement.href = "/employ/question/"+urlParts[6]+"/"+linePost.id+"/";
    linkElement.appendChild(lineTitleElement);
    linkElement.appendChild(lineDateElement);

    linePostElement.appendChild(linkElement);

    linePostList.appendChild(linePostElement);
  }
}

function renderButton() {

  buttonContainer.innerHTML = '';
  if (currentPage > 1) {
    const prevButton = createButton('...');
    prevButton.addEventListener('click', () => {
      currentPage--;
      renderButton();
    });
    buttonContainer.appendChild(prevButton);
  }


  const startButton = (currentPage - 1) * 4;
  
  let endButton = totalPages;
  if (endButton > buttonCount) {
    endButton = buttonCount;
  }


  for (let i = startButton; i < endButton; i++) {
    const button = createButton(i + 1);
    buttonContainer.appendChild(button);
  }


  if (currentPage < totalPages) {
    const nextButton = createButton('…');
    nextButton.addEventListener('click', () => {
      currentPage++;
      renderButton();
    });
    buttonContainer.appendChild(nextButton);
  }
}

function createButton(number) {

  const button = document.createElement('div');
  button.classList.add('button');
  button.id = number;
  button.style.width = buttonSize + 'px';
  button.style.height = buttonSize + 'px';
  button.innerText = number;


  button.onclick = function () {
    loadQAList(number);
  
    // 최초 확인 시작
    checkPosts();
  }


  return button;
}
window.addEventListener('DOMContentLoaded', (event) => {
  var buttonCount;

  const buttonContainer = document.getElementById('buttonContainer');
  loadQAList(1);
  
  // 최초 확인 시작
  checkPosts();

});


