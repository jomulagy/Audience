$("#create-btn").click(function () {
  var url = location.href
  var urlParts = url.split("/")
  console.log(urlParts)
  if(decodeURIComponent(urlParts[5])==="구직"){
    if(decodeURIComponent(urlParts[6])==="구직"){
      location.href = "/job/create/"
    }
    else if(decodeURIComponent(urlParts[6])==="free"){
      location.href = "/job/freepost/create/"
    }
  }
  if(decodeURIComponent(urlParts[5])==="구인"){
    if(decodeURIComponent(urlParts[6])==="구인"){
      location.href = "/employ/create/"
    }
    else if(decodeURIComponent(urlParts[6])==="free"){
      location.href = "/employ/freepost/create/"
    }
  }
})

$("#search-btn").click(function(){
  var keyword = $("#keyword").val()
  var search_type = $('select[name="searchField"]').val();
  var url = location.href
  var urlParts = url.split("/")
  location.href = "/audience/search/"+keyword+"/"+urlParts[5]+"/"+urlParts[6]+"/"+urlParts[7]+"/"+search_type+"/"

})

$(".searchBox").click(function(){
  var url = location.href
  var urlParts = url.split("/")
  location.href = "/audience/search/"+urlParts[5]+"/"+urlParts[6]+"/"+$(this).text()+"/"+urlParts[8]+"/"
})
// 사각형; 게시글 데이터 (예시)
function truncateContentName(content) {
  if (content.length > 20) {
    return content.slice(0, 20) + "...";
  } else {
    return content;
  }
}

function showPosts(posts) {
  var postList = document.getElementById("postList");
  postList.innerHTML = "";
  for (var i = 0; i < 4 && i < posts.length; i++) {
    var post = posts[i];
    var postElement = document.createElement("div");
    postElement.classList.add("post");

    var contentElement = document.createElement("h3");
    contentElement.classList.add("post-content");
    contentElement.textContent = truncateContentName(post.content);

    var titleElement = document.createElement("h3");
    titleElement.classList.add("post-title");
    titleElement.textContent = post.title;

    var viewsElement = document.createElement("p");
    viewsElement.classList.add("post-views");
    viewsElement.textContent = "조회수: " + post.views;

    var linkElement = document.createElement("a");
    linkElement.href = post.link;
    linkElement.target = "_blank";

    linkElement.appendChild(titleElement);
    linkElement.appendChild(contentElement);
    linkElement.appendChild(viewsElement);

    postElement.appendChild(linkElement);

    postList.appendChild(postElement);
  }
}

// document.addEventListener("DOMContentLoaded", function () {
//   showPosts();
// });


// 검색 기능 ---> ajax,,,
function searchPosts(target) {

  var word = target.value;
  var encodeWord = encodeURI(word);
  console.log(word);
  console.log(encodeWord);

  // Ajax
  $.ajax({
    type: 'GET',
    dataType: 'json',
    url: "/audience/search/posts/" + word,
    contentType: 'application/json',
    error: function (err) {
      console.log("실행중 오류가 발생하였습니다.");
    },
    success: function (data) {

      console.log("data확인 : " + data);
      console.log("결과 갯수 : " + data.dataSearch.content.length);
      console.log("첫번째 결과 : " + data.dataSearch.content[0]);
      $("#schoolList").empty();
      var checkWord = $("#word").val(); //검색어 입력값
      console.log(data.dataSearch.content.length);
    }
  })
}
function addNewPost(target){

}


document.addEventListener("DOMContentLoaded", function () {
  function checkPosts() {
    if (typeof posts !== "undefined") {
      // "posts"가 정의되면 원하는 작업을 수행
      console.log("success : ",posts)
      showPosts(posts);
      lineShowPosts(posts);
      // searchPosts();
    } else {
      // "posts"가 아직 정의되지 않았으면 재귀적으로 확인
      setTimeout(checkPosts, 1000); // 1초마다 확인
      console.log("failed")
    }
  }

  // 최초 확인 시작
  checkPosts();
});

function lineShowPosts(linePosts) {
  var linePostList = document.getElementById("linePostList");
  linePostList.innerHTML = "";

  for (var i = 0; i < 5 && i < linePosts.length; i++) {
    var linePost = linePosts[i];
    var linePostElement = document.createElement("div");
    linePostElement.classList.add("linePost");

    var lineCompanyElement = document.createElement("h2");
    lineCompanyElement.classList.add("linePost-company");

    var lineTitleElement = document.createElement("h2");
    lineTitleElement.classList.add("linePost-title");
    lineTitleElement.textContent = linePost.title;

    var lineViewsElement = document.createElement("p");
    lineViewsElement.classList.add("linePost-views");
    lineViewsElement.textContent = "조회수: " + linePost.views;

    var linkElement = document.createElement("a");
    linkElement.href = getLink(linePost.id);
    linkElement.target = "_blank";
    linkElement.appendChild(lineCompanyElement);
    linkElement.appendChild(lineTitleElement);
    linkElement.appendChild(lineViewsElement);

    linePostElement.appendChild(linkElement);

    linePostList.appendChild(linePostElement);
  }
}

function getLink(id){
  var url = location.href
  var urlParts = url.split("/")
  if(decodeURIComponent(urlParts[5])==="구직"){
    if(decodeURIComponent(urlParts[6])==="구직"){
      return "/job/"+id+"/"
    }
    else if(decodeURIComponent(urlParts[6])==="free"){
      return "/job/freepost/"+id+"/"
    }
  }
  if(decodeURIComponent(urlParts[5])==="구인"){
    if(decodeURIComponent(urlParts[6])==="구인"){
      return "/employ/"+id+"/"
    }
    else if(decodeURIComponent(urlParts[6])==="free"){
      return "/employ/freepost/"+id+"/"
    }
  }
}
