// 질문
var contentBoxElement = document.createElement("div");
contentBoxElement.classList.add("contentBox");

var questionTitleElement = document.createElement("h2");
questionTitleElement.classList.add("questiontitle");
questionTitleElement.textContent = "질문 제목: ";

var questionContentElement = document.createElement("div");
questionContentElement.classList.add("questionContent");

contentBoxElement.appendChild(questionTitleElement);
contentBoxElement.appendChild(questionContentElement);

var contentBoxUpElement = document.createElement("div");
contentBoxUpElement.classList.add("contentBoxUp");

var contentBoxDownElement = document.createElement("div");
contentBoxDownElement.classList.add("contentBoxDown");

parentElement.appendChild(contentBoxElement);
parentElement.appendChild(contentBoxUpElement);
parentElement.appendChild(contentBoxDownElement);



// 신고하기 (게시글)
const reportButton2 = document.querySelector('.reportText');
const reportMenu2 = document.querySelector('.reportMenu2');

reportButton2.addEventListener('click', () => {
  reportMenu2.style.display = 'block';
});

const reportSubmitButton2 = document.getElementById('report-submit2');
reportSubmitButton2.addEventListener('click', () => {
  const reportReason2 = document.getElementById('reportReason2').value;

  console.log('신고 이유:', reportReason2);

  reportMenu2.style.display = 'none';

  // Ajax 요청
  const requestData = {
    "post_id": post_id,
    "content": reportReason2
  };

  fetch('/employ/report/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      console.log('신고 응답:', data);
    })
    .catch(error => {
      console.log('신고 실패:', error);
    });
});

