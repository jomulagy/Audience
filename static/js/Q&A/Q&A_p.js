var linePosts;
var url = location.href
var urlParts = url.split("/")

function dateFormat(dateString){
  // Date 객체로 변환
  var date = new Date(dateString);

  // 연, 월, 일 추출
  var year = date.getFullYear();
  var month = (date.getMonth() + 1).toString().padStart(2, '0'); // 월은 0부터 시작하므로 +1 필요
  var day = date.getDate().toString().padStart(2, '0');

  // 연, 월, 일을 조합하여 원하는 형식으로 표시
  var formattedDate = year + '.' + month + '.' + day;
  return formattedDate;
}




// document.addEventListener("DOMContentLoaded", function () {
//   loadQAList();
//   function checkPosts() {
//     if (typeof linePosts !== "undefined") {
//       // "posts"가 정의되면 원하는 작업을 수행
//       console.log("success : ",posts)
//       lineShowPosts();
//       // searchPosts();
//     } else {
//       // "posts"가 아직 정의되지 않았으면 재귀적으로 확인
//       setTimeout(checkPosts, 1000); // 1초마다 확인
//       console.log("failed")
//     }
//   }

//   // 최초 확인 시작
//   checkPosts();
  
// });



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