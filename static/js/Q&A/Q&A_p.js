// 줄; 게시글 데이터 (예시)
/*
var linePosts = [
  {
    lineTitle: "게시물 제목(답변 대기중)",
    lineDate: "2023.01.01",
    link: "https://www.google.com"
  },
  {
    lineTitle: "게시물 제목(답변 대기중)",
    lineDate: "2023.01.01",
    link: "https://www.naver.com"
  },
  {
    lineTitle: "게시물 제목(답변 대기중)",
    lineDate: "2023.01.01",
    link: "https://www.naver.com/222"
  },
  {
    lineTitle: "게시물 제목(답변 완료)",
    lineDate: "2023.01.01",
    link: "https://www.naver.com/777"
  },
  {
    lineTitle: "게시물 제목(답변 완료)",
    lineDate: "2023.01.01",
    link: "https://www.naver.com/000"
  }
];


function lineShowPosts() {
  var linePostList = document.getElementById("linePostList");
  linePostList.innerHTML = "";

  for (var i = 0; i < 5 && i < linePosts.length; i++) {
    var linePost = linePosts[i];
    var linePostElement = document.createElement("div");
    linePostElement.classList.add("linePost");

    var lineTitleElement = document.createElement("h2");
    lineTitleElement.classList.add("linePost-title");
    lineTitleElement.textContent = linePost.lineTitle;

    var lineDateElement = document.createElement("h3");
    lineDateElement.classList.add("linePost-date");
    lineDateElement.textContent = linePost.lineDate;

    var linkElement = document.createElement("a");
    linkElement.href = linePost.link;
    linkElement.target = "_blank"; 
    linkElement.appendChild(lineTitleElement);
    linkElement.appendChild(lineDateElement);

    linePostElement.appendChild(linkElement);

    linePostList.appendChild(linePostElement);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  lineShowPosts();
});
*/

function loadQAList() {
  $.ajax({
    url: 'http://127.0.0.1:8000/employ/question/list/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({
      post_id: 3,
      page_num: 1
    }),
    contentType: 'application/json',
    success: function(response) {
      var qaList = response.QA_List;
      // Q&A 리스트를 처리하는 로직 추가
      console.log('Q&A 리스트:', qaList);
    },
    error: function(xhr, textStatus, error) {
      console.log('Q&A 리스트 불러오기 에러:', error);
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  lineShowPosts();
  loadQAList();
});


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
});
//