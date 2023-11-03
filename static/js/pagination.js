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
    else {
        var data = {
            "keyword" : null,
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
            console.log(buttonCount)
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

          
            var data;
            if (segmentList.length == 9) {
              data = {
                "keyword": segmentList[4],
                "category": segmentList[5],
                "board_type": segmentList[6],
                "post_type": segmentList[7],
                "search_type": segmentList[8],
                "page_num": number
              };

              $.ajax({
                type: "POST",
                dataType: "json",
                url: "/audience/search/posts/keyword/",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(data) {
                  posts = data.ranks;
                  linePosts = data.posts;
                },
                error: function(err) {
                  console.log("Error occurred: " + err);
                }
              });
            } else {
              data = {
                "keyword": null,
                "category": segmentList[4],
                "board_type": segmentList[5],
                "post_type": segmentList[6],
                "search_type": segmentList[7],
                "page_num": number
              };

              $.ajax({
                type: "POST",
                dataType: "json",
                url: "/audience/search/posts/",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(data) {
                  posts = data.ranks;
                  linePosts = data.posts;
                },
                error: function(err) {
                  console.log("Error occurred: " + err);
                }
              });
            }
          
            
          }
          

        return button;
    }

    

});


  