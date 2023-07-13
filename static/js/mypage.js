// const mypageButton1 = document.getElementById("mypage_button_1");
// const mypageButton2 = document.getElementById("mypage_button_2");
// 스타일 변경
// mypageButton1.style.backgroundColor = "#FFDCDC";
console.log(interests)

var labels = querySelector('.change_label');
var linePosts;


function show_mypage1() {
    $("#mypage_1").show();
    $("#mypage_2").hide();
    $("#mypage_button_1").css("background-color", "#FFDCDC");
    $("#mypage_button_2").css("background-color", "#FFFFFF");
    for (var i=0; i < interests;i++){
        console.log(interests[i]);
        $("label[value='" + interests[i] + "']").css("background-color", "#FFBDBD");
    }
}

function show_mypage2() {
    $("#mypage_1").hide();
    $("#mypage_2").show();
    $("#mypage_button_1").css("background-color", "#FFFFFF");
    $("#mypage_button_2").css("background-color", "#FFDCDC");
    // $("<a>").text(data.title).class("notice_title").id(data.id).appendTo(notice);
    // $("<a>").text(data.views).class("views").id(data.id).appendTo(notice);     
    $.ajax({
        type : 'GET',
        url : "/account/posts/detail/",
        data: JSON.stringify({

        }),
        success : function(data){
            // console.log("111");
            var notice = document.querySelector('.notice');
            var posts = data.posts;
            $("a.notice_title").text(posts[1]).id(posts[0]).text(posts[1]).appendTo(notice);
            $("a.views").text(posts[1]).id(posts[0]).text(posts[2] + "회").appendTo(notice);            
        }
    })
       
    
}

// function button_2() {
//     $('input[name="interest"]').change(function () {
//       $('input[name="interest"]').each(function () {
//         var checked = $(this).prop("checked");
//         // var checked = $(this).attr('checked');
//         // var checked = $(this).is('checked');
//         var label1 = $(this).next().next().next().next().next().next();
//         var label2 = $(label1).next().next().next().next().next().next();
//         var $label = $(label2).next().next().next().next().next().next();

//         if (checked) $label.css("background-color", "#FFBDBD");
//         else $label.css("background-color", "#FFE5E5");
//       });
//     });
// }
var posts;
var linePosts;
window.addEventListener('DOMContentLoaded', (event) => {
    var buttonCount;

    const buttonContainer = document.getElementById('buttonContainer');


    var url = window.location.href; // 현재 페이지의 URL을 가져옵니다.
    url = decodeURIComponent(url);
    var segments = url.split('/'); // URL을 '/'로 분할하여 segments 배열에 저장합니다.

    var segmentList = []; // 분할된 URL 세그먼트를 저장할 배열입니다.

// segments 배열을 순회하며 빈 값을 제외한 세그먼트를 segmentList에 저장합니다.
    $.each(segments, function(index, segment) {
        if (segment !== '') {
            segmentList.push(segment);
        }
    });

    if(segmentList.length == 9){
        var data = {
            "keyword" : segmentList[4],
            "category" : segmentList[5],
            "board_type" : segmentList[6],
            "post_type" : segmentList[7],
            "search_type" : segmentList[8]
        }
    }
    else{
        var data = {
            "keyword" : None,
            "category" : segmentList[4],
            "board_type" : segmentList[5],
            "post_type" : segmentList[6],
            "search_type" : segmentList[7]
        } 
    }
    $.ajax({
        type: "POST",
        dataType: "json",    
        url: "/audience/total_pages/",
        data: JSON.stringify(data),
        success: function(data) {
            buttonCount = data.total_pages;
            renderButton();
            
            $("#1").trigger("click");
        },
       
        
        error: function(err) {
            console.log(err)
        },
        
    })



    
    const buttonSize = 30;

    let currentPage = 1;
    let totalPages = buttonCount / 4;

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
        let endButton = startButton + 4;

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


        button.onclick = function() {

          
            lineShowPosts(linePosts)
          
            
          }
          

        return button;
    }

    

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
      linkElement.href = linePost.link;
      linkElement.target = "_blank"; 
      linkElement.appendChild(lineCompanyElement);
      linkElement.appendChild(lineTitleElement);
      linkElement.appendChild(lineViewsElement);
  
      linePostElement.appendChild(linkElement);
  
      linePostList.appendChild(linePostElement);
    }
  }
  