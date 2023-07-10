// 줄; 게시글 데이터 (예시)
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
