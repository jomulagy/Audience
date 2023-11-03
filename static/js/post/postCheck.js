let likeClicked = false;
let dislikeClicked = false;

function toggleLike() {
  $.ajax({
    url: '/util/like/create/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({"post_id" : post_id }),
    success: function (response) {
      $(".goodText").text(response.likes_count+'👍'+"\n좋아요")
      //$(".badText").text(response.likes_count+"👎"+"싫어요")
    },
    error: function (xhr, textStatus, error) {
      console.log('좋아요 클릭 에러:', error);
    }
  });
}

function toggleDislike() {
  $.ajax({
    url: '/util/dislike/create/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({"post_id" : post_id }),
    success: function (response) {
      //$(".goodText").text(response.likes_count+'👍'+"좋아요")
      $(".badText").text(response.likes_count+"👎"+"\n싫어요")
    },
    error: function (xhr, textStatus, error) {
      console.log('싫어요 클릭 에러:', error);
    }
  });
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
        post_id: post_id,
        content: "sss"
        //commentContent
      };

      fetch('/comment/create/', {
        method: 'POST',
        headers: {
          contentType: 'application/json'
        },
        body: JSON.stringify(requestData)
      })
        .then(response => response.json())
        .then(data => {
          const comment = createCommentElement(commentContent, data.id);
          console.log(comment)
          commentList.insertBefore(comment, commentList.firstChild);
          commentInput.value = "";
        })
        .catch(error => {
          console.log('댓글 작성 실패:', error);
        });

      /*
            const comment = createCommentElement("aa"); 
            console.log(comment)
            commentList.insertBefore(comment, commentList.firstChild);
            commentInput.value = "";
            */
    }
  });

  function createCommentElement(content, id) {
    const comment = document.createElement("div");
    comment.classList.add("comment");
    comment.setAttribute("id", id)
    const commentId = document.createElement("p");
    commentId.textContent = "[아이디]";

    const commentContent = document.createElement("p");
    commentContent.classList.add("comment_content")
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

        fetch('/comment/update/', {
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
      console.log(comment.id)
      comment.remove(); // 댓글 삭제
      adjustCommentBoxHeight();

      // Ajax
      const requestData = {
        comment_id: 1
      };

      fetch('/comment/comment/delete/', {
        method: 'POST',
        headers: {
          contentType: 'application/json'
        },
        body: JSON.stringify(requestData)
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            reply.remove();
          } else {
            console.log('댓글 삭제 실패');
          }
        })
        .catch(error => {
          console.log('댓글 삭제 실패:', error);
        });
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

        fetch('/comment/reply/update/', {
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


    //<button class="reply_update" onclick="updateReply(this)">수정하기</button>

    const editButton = document.createElement("button");
    editButton.textContent = "수정하기";
    editButton.addEventListener("click", function () {
      const newContent = prompt("대댓글을 수정하세요", replyContent.textContent);
      if (newContent !== null) {
        // Ajax
        const requestData = {
          reply_id: 1,
          content: newContent
        };

        fetch('/comment/reply/update/', {
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

      // Ajax
      const requestData = {
        reply_id: 1
      };

      fetch('/comment/reply/delete/', {
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


    replyOptions.appendChild(editButton);
    replyOptions.appendChild(deleteButton);

    reply.appendChild(replyRe);
    reply.appendChild(replyContent);
    reply.appendChild(replyOptions);

    return reply;
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
    commentBoxDown.style.top = 2126 + commentHeight + "px";
    backg.style.height = 2000 + commentHeight + "px";
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
  commentBoxDown.style.top = 2126 + commentHeight + "px";
  backg.style.height = 2000 + commentHeight + "px";
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

/*-----------------------삭제하기-------------------------------*/
$(document).on('click', 'delete-button', function () {
  var comment = $(this).parent().parent();
  var comment_id = comment.attr("id");
  comment.remove(); // 댓글 삭제
  adjustCommentBoxHeight();

  // Ajax
  const requestData = {
    "comment_id": comment_id
  };

  fetch('/comment/delete/', {
    method: 'POST',
    headers: {
      contentType: 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        reply.remove();
      } else {
        console.log('댓글 삭제 실패');
      }
    })
    .catch(error => {
      console.log('댓글 삭제 실패:', error);
    });
});


/*---------------------------수정하기--------------------------------*/
function updateComment(button) {
  var comment = button.parentNode.parentNode;
  console.log(button.parentNode.parentNode.id)
  var commentId = button.parentNode.parentNode.id
  var commentContent = $(comment).find('p:first-child + p').text();
  const newContent = prompt("댓글을 수정하세요", commentContent.textContent);
  console.log(newContent)
  adjustCommentBoxHeight();

  // AJAX
  const requestData = {
    "comment_id": commentId,
    "content": newContent
  };

  fetch('/comment/update/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {

        $(comment).find('.comment_content').text(newContent);
      } else {
        console.log('댓글 수정 실패');
      }
    })
    .catch(error => {
      console.log('댓글 수정 실패:', error);
    });
}


/*----------------------대댓글 달기--------------------------------*/

// $(document).on('click', '.recomment', function() {
//   var comment = $(this).closest('.comment');
//   var commentId = comment.attr('id');

//   var commentContent = comment.find('p:first-child + p').text();
//   console.log(commentContent)

//   adjustCommentBoxHeight();
//   comment.find('p:first-child + p').text(data.content);
//         const reply = createReplyElement(data.content);
//         replyForm.parentNode.insertBefore(reply, replyForm.nextSibling);
//         replyForm.parentNode.removeChild(replyForm);
//         replyButton.style.display = "block";
//   // AJAX
//   const requestData = {
//     "comment_id": commentId
//   };

//   // fetch('/reply/update/', {
//   //   method: 'POST',
//   //   headers: {
//   //     'Content-Type': 'application/json'
//   //   },
//   //   body: JSON.stringify(requestData)
//   // })
//   //   .then(response => response.json())
//   //   .then(data => {
//   //     if (data.success) {
//   //       //comment.find('p:first-child + p').text(data.content);
//   //       const reply = createReplyElement(data.content);
//   //       replyForm.parentNode.insertBefore(reply, replyForm.nextSibling);
//   //       replyForm.parentNode.removeChild(replyForm);
//   //       replyButton.style.display = "block";

//   //     } else {
//   //       console.log('대댓글 달기 실패');
//   //     }
//   //   })
//   //   .catch(error => {
//   //     console.log('대댓글 달기 실패:', error);
//   //   });
//     });
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
        comment_id: replyButton.parentNode.parentNode.id,
        content: replyContent
      };
      console.log(requestData)
      fetch('/comment/reply/create/', {
        method: 'POST',
        headers: {
          contentType: 'application/json'
        },
        body: JSON.stringify(requestData)
      })
        .then(response => response.json())
        .then(data => {
          const reply = createReplyElement(requestData.content, data.author);
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
  console.log(replyButton.parentNode.parentNode)
  replyButton.parentNode.parentNode.appendChild(replyForm);
}

function createReplyElement(content, user) {
  const reply = document.createElement("div");
  reply.classList.add("reply_content");

  const replyRe = document.createElement("p");
  replyRe.textContent = "└ RE: [" + user + "]";

  const replyContent = document.createElement("p");
  replyContent.classList.add("reply_content")
  replyContent.textContent = `${content}`;

  const replyOptions = document.createElement("div");
  replyOptions.classList.add("comment-options");



  const editButton = document.createElement("button");
  editButton.classList.add("reply_update")
  editButton.textContent = "수정하기";
  editButton.addEventListener('click', function() {
    updateReply(this);
  });

  const deleteButton = document.createElement("delete-button");
  deleteButton.textContent = " 삭제하기";
  deleteButton.addEventListener("click", function () {
    deleteReply(this);
    
  });


  replyOptions.appendChild(editButton);
  replyOptions.appendChild(deleteButton);

  reply.appendChild(replyRe);
  reply.appendChild(replyContent);
  reply.appendChild(replyOptions);

  return reply;
};
function updateReply(button) {
  var reply = button.parentNode.parentNode;
  var replyId = button.parentNode.parentNode.id
  var replyContent = $(reply).find('p:first-child + p').text();
  console.log(replyContent)
  const newRelyContent = prompt("대댓글을 수정하세요", replyContent.textContent);
  
  if (newRelyContent !== null) {
    // Ajax
    const requestData = {
      "reply_id": replyId,
      "content": newRelyContent
    };

    fetch('/comment/reply/update/', {
      method: 'POST',
      headers: {
        contentType: 'application/json'
      },
      body: JSON.stringify(requestData)
    })
      .then(response => response.json())
      .then(data => {
        //replyContent.textContent = data.content;
        $(reply).find('.reply_content').text(newRelyContent);

      })
      .catch(error => {
        console.log('대댓글 수정 실패:', error);
      });

    replyContent.textContent = `${newRelyContent}`;
  }
};
    
function deleteReply(button) {
  var reply = button.parentNode.parentNode;
  var replyId = button.parentNode.parentNode.id
  
  const requestData = {
    "reply_id": replyId
  };

  fetch('/comment/reply/delete/', {
    method: 'POST',
    headers: {
      contentType: 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      reply.remove()

    })
    .catch(error => {
      console.log('대댓글 삭제 실패:', error);
    });
};   
