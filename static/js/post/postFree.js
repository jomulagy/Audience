// 좋아요/싫어요
let likeClicked = false;
let notLikeClicked = false;

function toggleLike() {
  if (!likeClicked) {
    likeClicked = true;
    if (notLikeClicked) {
      notLikeClicked = false;
    }

    $.ajax({
      url: 'http://127.0.0.1:8000/util/like/create/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        "likes_count": 1,
        "dislikes_count": 0,
        "is_liked": true,
        "is_disliked": false
      }),
      success: function (response) {
        console.log(response);
      },
      error: function (xhr, textStatus, error) {
        console.log(error);
      }
    });
  } else {
    likeClicked = false;
  }
}



function toggleNotLike() {
  if (!notLikeClicked) {
    notLikeClicked = true;
    if (likeClicked) {
      likeClicked = false;
    }
    $.ajax({
      url: 'http://127.0.0.1:8000/util/dislike/create/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        "likes_count": 0,
        "dislikes_count": 1,
        "is_liked": false,
        "is_disliked": true
      }),
      success: function (response) {
        console.log(response);
      },
      error: function (xhr, textStatus, error) {
        console.log(error);
      }
    });
  } else {
    notLikeClicked = false;
  }
}


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
    post_id: 1,
    content: reportReason2
  };

  fetch('http://127.0.0.1:8000/employ/report/create/', {
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




// 댓글 달기
document.addEventListener("DOMContentLoaded", function () {
  const commentList = document.getElementById("comment-list");
  const commentInput = document.getElementById("comment-input");
  const commentSubmit = document.getElementById("comment-submit");

  commentSubmit.addEventListener("click", function () {
    const commentContent = commentInput.value.trim();
    if (commentContent !== "") {

      // Ajax
      const requestData = {
        post_id: 1,
        content: commentContent
      };

      // fetch('http://127.0.0.1:8000/comment/create/', {
      //   method: 'POST',
      //   headers: {
      //     contentType: 'application/json'
      //   },
      //   body: JSON.stringify(requestData)
      // })
      //   .then(response => response.json())
      //   .then(data => {
      //     const comment = createCommentElement(commentContent);
      //     commentList.insertBefore(comment, commentList.firstChild);
      //     commentInput.value = "";
      //   })
      //   .catch(error => {
      //     console.log('댓글 작성 실패:', error);
      //   });


      const comment = createCommentElement("aa"); 
      console.log(comment)
      commentList.insertBefore(comment, commentList.firstChild);
      commentInput.value = "";
    }
  });

  function createCommentElement(content) {
    const comment = document.createElement("div");
    comment.classList.add("comment");

    const commentId = document.createElement("p");
    commentId.textContent = "[아이디]";

    const commentContent = document.createElement("p");
    commentContent.textContent = `${content}`;

    const commentOptions = document.createElement("div");
    commentOptions.classList.add("comment-options");

    const replyButton = document.createElement("button");
    replyButton.textContent = "대댓글 달기";
    replyButton.addEventListener("click", function () {
      const replyForm = createReplyForm(replyButton);
      comment.appendChild(replyForm);
      replyButton.style.display = "none"; // 대댓글 버튼 숨기기
    });

    const editButton = document.createElement("button");
    editButton.textContent = "수정하기";
    editButton.addEventListener("click", function () {
      const newContent = prompt("댓글을 수정하세요", commentContent.textContent);
      if (newContent !== null) {
        commentContent.textContent = `${newContent}`;
        // ajax
        const requestData = {
          comment_id: 1,
          content: newContent
        };

        fetch('http://127.0.0.1:8000/comment/update/', {
          method: 'POST',
          headers: {
            contentType: 'application/json'
          },
          body: JSON.stringify(requestData)
        })
          .then(response => response.json())
          .then(data => {
            commentContent.textContent = data.content;
          })
          .catch(error => {
            console.log('댓글 수정 실패:', error);
          });
      }
    });

    const deleteButton = document.createElement("delete-button");
    deleteButton.textContent = " 삭제하기";
    deleteButton.addEventListener("click", function () {
      comment.remove(); // 댓글 삭제
      adjustCommentBoxHeight();
      
      //   // Ajax
      // const requestData = {
      //   comment_id: 1 // 대댓글 ID를 적절히 설정해야 합니다.
      // };

      // fetch('http://127.0.0.1:8000/comment/comment/delete/', {
      //   method: 'POST',
      //   headers: {
      //     contentType: 'application/json'
      //   },
      //   body: JSON.stringify(requestData)
      // })
      //   .then(response => response.json())
      //   .then(data => {
      //     if (data.success) {
      //       reply.remove();
      //     } else {
      //       console.log('댓글 삭제 실패');
      //     }
      //   })
      //   .catch(error => {
      //     console.log('댓글 삭제 실패:', error);
      //   });
      });

    commentOptions.appendChild(replyButton);
    commentOptions.appendChild(editButton);
    commentOptions.appendChild(deleteButton);

    comment.appendChild(commentId);
    comment.appendChild(commentContent);
    comment.appendChild(commentOptions);

    return comment;
    }
    
  

  function createReplyForm(replyButton) {
    const replyForm = document.createElement("div");
    replyForm.classList.add("reply-form");

    const replyInput = document.createElement("textarea");
    replyInput.placeholder = "대댓글을 작성하세요";

    const replySubmit = document.createElement("button");
    replySubmit.textContent = "SEND";
    replySubmit.addEventListener("click", function () {
      const replyContent = replyInput.value.trim();
      if (replyContent !== "") {

        // Ajax
        const requestData = {
          reply_id: 1,
          content: replyContent
        };

        fetch('http://127.0.0.1:8000/comment/reply/update/', {
          method: 'POST',
          headers: {
            contentType: 'application/json'
          },
          body: JSON.stringify(requestData)
        })
          .then(response => response.json())
          .then(data => {
            const reply = createReplyElement(data.content);
            replyForm.parentNode.insertBefore(reply, replyForm.nextSibling);
            replyForm.parentNode.removeChild(replyForm);
            replyButton.style.display = "block";
          })
          .catch(error => {
            console.log('대댓글 작성 실패:', error);
          });
        /*
        const reply = createReplyElement(replyContent);
        replyForm.parentNode.insertBefore(reply, replyForm.nextSibling);
        replyForm.parentNode.removeChild(replyForm);
        replyButton.style.display = "block"; */
      }
    });

    replyForm.appendChild(replyInput);
    replyForm.appendChild(replySubmit);

    return replyForm;
  }

  function createReplyElement(content) {
    const reply = document.createElement("div");
    reply.classList.add("reply");

    const replyRe = document.createElement("p");
    replyRe.textContent = "└ RE: [아이디]";

    const replyContent = document.createElement("p");
    replyContent.textContent = `${content}`;

    const replyOptions = document.createElement("div");
    replyOptions.classList.add("comment-options");

    const editButton = document.createElement("button");
    editButton.textContent = "수정하기";
    editButton.addEventListener("click", function () {
      const newContent = prompt("대댓글을 수정하세요", replyContent.textContent);
      if (newContent !== null) {
        // Ajax
        const requestData = {
          reply_id: 1, // 대댓글 ID를 적절히 설정해야 합니다.
          content: newContent
        };

        fetch('http://127.0.0.1:8000/comment/reply/update/', {
          method: 'POST',
          headers: {
            contentType: 'application/json'
          },
          body: JSON.stringify(requestData)
        })
          .then(response => response.json())
          .then(data => {
            replyContent.textContent = data.content;
          })
          .catch(error => {
            console.log('대댓글 수정 실패:', error);
          });

        replyContent.textContent = `${newContent}`;
      }
    });

    const deleteButton = document.createElement("delete-button");
    deleteButton.textContent = " 삭제하기";
    deleteButton.addEventListener("click", function () {
      /*
      // Ajax
    const requestData = {
      reply_id: 1 // 대댓글 ID를 적절히 설정해야 합니다.
    };

    fetch('http://127.0.0.1:8000/comment/reply/delete/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          reply.remove();
        } else {
          console.log('대댓글 삭제 실패');
        }
      })
      .catch(error => {
        console.log('대댓글 삭제 실패:', error);
      });
    });
    */

      replyOptions.appendChild(editButton);
      replyOptions.appendChild(deleteButton);

      reply.appendChild(replyRe);
      reply.appendChild(replyContent);
      reply.appendChild(replyOptions);

      return reply;
    })
  };

  /*
    document.addEventListener("DOMContentLoaded", function () {
      const commentList = document.getElementById("comment-list");
      const commentSubmit = document.getElementById("comment-submit");
      const commentBox = document.querySelector(".commentBox");
      const commentBoxDown = document.querySelector(".commentBoxDown");
      const backg = document.querySelector(".backg");
      const commentInput = document.querySelector(".comment-input-container");
      const commentDelete = document.querySelector("#delete-button");
  
    
      commentSubmit.addEventListener("click", function () {
        commentBox.style.height = 300 + commentList.offsetHeight + "px";
        commentBoxDown.style.top = 2050 + commentList.offsetHeight + "px";
        backg.style.height = 2000 + commentList.offsetHeight + "px";
        commentInput.style.top = 200 + commentList.offsetHeight + "px";
      });
    });
    
    document.addEventListener("DOMContentLoaded", function () {
      comment.remove();
      commentDelete.addEventListener("click", function () {
        const commentHeight = commentList.offsetHeight;
      
        commentBox.style.height = 300 + commentHeight + "px";
        commentBoxDown.style.top = 2050 + commentHeight + "px";
        backg.style.height = 2000 + commentHeight + "px";
        commentInput.style.top = 200 + commentHeight + "px";
      });*/
});
document.addEventListener("DOMContentLoaded", function () {
  const commentList = document.getElementById("comment-list");
  const commentSubmit = document.getElementById("comment-submit");
  const commentBox = document.querySelector(".commentBox");
  const commentBoxDown = document.querySelector(".commentBoxDown");
  const backg = document.querySelector(".backg");
  const commentInput = document.querySelector(".comment-input-container");

  commentSubmit.addEventListener("click", function () {
    const commentHeight = commentList.offsetHeight;
    const newCommentBoxHeight = 300 + commentHeight;

    commentBox.style.height = newCommentBoxHeight + "px";
    commentBoxDown.style.top = 1750 + commentHeight + "px";
    backg.style.height = 1700 + commentHeight + "px";
    commentInput.style.top = 200 + commentHeight + "px";
  });

  commentList.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-button")) {
      const comment = event.target.closest(".comment");
      const commentHeight = comment.offsetHeight;

      comment.remove(); // 댓글 삭제
      adjustCommentBoxHeight();
      const newCommentBoxHeight = parseInt(commentBox.style.height) - commentHeight;
      commentBox.style.height = newCommentBoxHeight + "px";
    }
  });
});
  
// document.addEventListener("DOMContentLoaded", function () {
// const commentList = document.getElementById("comment-list");
// const commentSubmit = document.getElementById("comment-submit");
// const commentBox = document.querySelector(".commentBox");
// const commentBoxDown = document.querySelector(".commentBoxDown");
// const backg = document.querySelector(".backg");
// const commentInput = document.querySelector(".comment-input-container");
 
function adjustCommentBoxHeight() {
  const commentList = document.getElementById("comment-list");
  const commentHeight = commentList.offsetHeight;
  const newCommentBoxHeight = 300 + commentHeight;
  
  const commentBox = document.querySelector(".commentBox");
  const commentBoxDown = document.querySelector(".commentBoxDown");
  const backg = document.querySelector(".backg");
  const commentInput = document.querySelector(".comment-input-container");
  commentBox.style.height = newCommentBoxHeight + "px";
  commentBoxDown.style.top = 1750 + commentHeight + "px";
  backg.style.height = 1700 + commentHeight + "px";
  commentInput.style.top = 200 + commentHeight + "px";
}
 /*
commentSubmit.addEventListener("click", function () {
  adjustCommentBoxHeight();
});
 
commentList.addEventListener("click", function (event) {
  if (event.target.classList.contains("delete-button")) {
    const comment = event.target.closest(".comment");
    const commentHeight = comment.offsetHeight;
 
    comment.remove(); 
 
    adjustCommentBoxHeight();
  }
});
});*/