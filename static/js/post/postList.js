// 사각형; 게시글 데이터 (예시)
var posts = [
  {
    title: "첫 번째 게시글 제목",
    content: "내용",
    views: 100,
    link: "https://www.google.com"
  },
  {
    title: "두 번째 게시글 제목",
    content: "20자 이상의 게시글입니다. 20자 이상의 게시글입니다. 20자 이상의 게시글입니다.",
    views: 90,
    link: "https://www.naver.com"
  },
  {
    title: "세 번째 게시글 제목",
    content: "내용",
    views: 80,
    link: "https://www.naver.com/222"
  },
  {
    title: "네 번째 게시글 제목",
    content: "내용",
    views: 60,
    link: "https://www.naver.com/777"
  }
];

function truncateContentName(content) {
  if (content.length > 20) {
    return content.slice(0, 20) + "...";
  } else {
    return content;    
  }
}

function showPosts() {
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

document.addEventListener("DOMContentLoaded", function () {
  showPosts();
});

  
  // 검색 기능 ---> ajax,,,
  function searchPosts(target){

    var word = target.value;
    var encodeWord = encodeURI(word);
    console.log(word);
    console.log(encodeWord);
    
    // Ajax
    $.ajax({
       type : 'GET',
       dataType : 'json',
       url : "http://127.0.0.1:8000/audience/search/posts/" + word,
       contentType: 'application/json',
       error : function(err) {
          console.log("실행중 오류가 발생하였습니다.");
       },
       success : function(data) {

          console.log("data확인 : " + data);
          console.log("결과 갯수 : " + data.dataSearch.content.length);
          console.log("첫번째 결과 : " + data.dataSearch.content[0]);
          $("#schoolList").empty();
          var checkWord = $("#word").val(); //검색어 입력값
          console.log(data.dataSearch.content.length);
             }
          })
    }


    function listenForNewPosts() {
      setInterval(function() {
        var newPost = {
          title: "새로운 게시글 " + (posts.length + 1),
          content: "내용",
          views: Math.floor(Math.random() * 100)
        };
    
        posts.unshift(newPost); 
    
        addNewPost(newPost); 
    
        if (posts.length > 5) {
          var postList = document.getElementById("newPostContainer");
          postList.removeChild(postList.lastChild);
        }
      }, 3000);
    }
    
    document.addEventListener("DOMContentLoaded", function() {
      showPosts(posts);
      searchPosts();
      listenForNewPosts();
    });


// 줄; 게시글 데이터 (예시)
var linePosts = [
  {
    lineTitle: "첫 번째 게시글",
    lineCompany: "회사명",
    lineViews: 100,
    link: "https://www.google.com"
  },
  {
    lineTitle: "두 번째 게시글",
    lineCompany: "회사명",
    lineViews: 50,
    link: "https://www.naver.com"
  },
  {
    lineTitle: "세 번째 게시글",
    lineCompany: "회사명",
    lineViews: 70,
    link: "https://www.naver.com/222"
  },
  {
    lineTitle: "네 번째 게시글",
    lineCompany: "회사명",
    lineViews: 55,
    link: "https://www.naver.com/777"
  },
  {
    lineTitle: "다섯 번째 게시글",
    lineCompany: "회사명",
    lineViews: 60,
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

    var lineCompanyElement = document.createElement("h2");
    lineCompanyElement.classList.add("linePost-company");
    lineCompanyElement.textContent = "[" + linePost.lineCompany + "]";

    var lineTitleElement = document.createElement("h2");
    lineTitleElement.classList.add("linePost-title");
    lineTitleElement.textContent = linePost.lineTitle;

    var lineViewsElement = document.createElement("p");
    lineViewsElement.classList.add("linePost-views");
    lineViewsElement.textContent = "조회수: " + linePost.lineViews;

    var linkElement = document.createElement("a");
    linkElement.href = linePost.link;
    linkElement.target = "_blank"; 
    linkElement.appendChild(lineCompanyElement);
    linkElement.appendChild(lineTitleElement);
    linkElement.appendChild(lineViewsElement);

    linePostElement.appendChild(linkElement);

    linePostList.appendChild(linePostElement);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  lineShowPosts();
});