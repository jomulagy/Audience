$(function() {
  $("#name").keyup(function() {
    const recommendBox = document.querySelector("#suggestion_box");
    recommendBox.classList.remove('invisible');
    const inputName = document.getElementById("name").value;

    recommendBox.innerHTML = "";

    const suggestedItems = document.createElement('div');
    suggestedItems.id = "suggested_items";
    recommendBox.appendChild(suggestedItems);

    $.ajax({
      url: "/job/company/search/",
      method: "POST",
      data: JSON.stringify({ name: inputName }),
      contentType: "application/json",
      success: function(response) {
        const companies = response.companies;
        for (var i in companies) {
          var companyName = companies[i].name;
          if (companyName.includes(inputName)) { // 입력한 단어가 포함된 경우에만 추가
            var playerContent = document.createTextNode(companyName);
            var suggestedItem = document.createElement('div');
            suggestedItem.className = "item";
            suggestedItem.addEventListener('click', function(e) {
              document.getElementById("name").value = this.textContent.split(' ')[0];
            });
            suggestedItem.appendChild(playerContent);
            suggestedItems.appendChild(suggestedItem);
          }
        }
      }
    });
  });
});
