// 좋아요/싫어요
let likeClicked = false;
let notLikeClicked = false;

function toggleLike() {
  if (!likeClicked) {
    likeClicked = true;
    if (notLikeClicked) {
      notLikeClicked = false;
    }
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
  } else {
    notLikeClicked = false;
  }
}

/*
// 답글 달기
const replyButton = document.querySelector('.commentOfComment');
const replyForm = document.querySelector('.replyForm');

replyButton.addEventListener('click', () => {
  replyForm.style.display = 'block';
});
*/


// 댓글 달기
document.addEventListener("DOMContentLoaded", function () {
  const commentList = document.getElementById("comment-list");
  const commentInput = document.getElementById("comment-input");
  const commentSubmit = document.getElementById("comment-submit");

  commentSubmit.addEventListener("click", function () {
    const commentContent = commentInput.value.trim();
    if (commentContent !== "") {
      const comment = createCommentElement(commentContent);
      commentList.insertBefore(comment, commentList.firstChild);
      commentInput.value = "";
    }
  });

  function createCommentElement(content) {
    const comment = document.createElement("div");
    comment.classList.add("comment");

    const commentContent = document.createElement("p");
    commentContent.textContent = `[아이디] ${content}`;

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
        commentContent.textContent = `[아이디] ${newContent}`;
      }
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "삭제하기";
    deleteButton.addEventListener("click", function () {
      comment.remove();
    });

    commentOptions.appendChild(replyButton);
    commentOptions.appendChild(editButton);
    commentOptions.appendChild(deleteButton);

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
        const reply = createReplyElement(replyContent);
        replyForm.parentNode.insertBefore(reply, replyForm.nextSibling);
        replyForm.parentNode.removeChild(replyForm);
        replyButton.style.display = "block"; // 대댓글 작성 후 대댓글 버튼 다시 보이기
      }
    });

    replyForm.appendChild(replyInput);
    replyForm.appendChild(replySubmit);

    return replyForm;
  }

  function createReplyElement(content) {
    const reply = document.createElement("div");
    reply.classList.add("reply");

    const replyContent = document.createElement("p");
    replyContent.textContent = `└ RE: [아이디] ${content}`;

    const replyOptions = document.createElement("div");
    replyOptions.classList.add("comment-options");

    const editButton = document.createElement("button");
    editButton.textContent = "수정하기";
    editButton.addEventListener("click", function () {
      const newContent = prompt("대댓글을 수정하세요", replyContent.textContent);
      if (newContent !== null) {
        replyContent.textContent = `└ RE: [아이디] ${newContent}`;
      }
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "삭제하기";
    deleteButton.addEventListener("click", function () {
      reply.remove();
    });

    replyOptions.appendChild(editButton);
    replyOptions.appendChild(deleteButton);

    reply.appendChild(replyContent);
    reply.appendChild(replyOptions);

    return reply;
  }
});