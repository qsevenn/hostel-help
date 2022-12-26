window.onload = function changeColor() {
    let arr = document.getElementsByClassName('status')
    for(let report of arr) {
        switch (report.textContent) {
            case 'Активна':
                report.style.color = '#41B562';
                break;
            case 'Закрита':
                report.style.color = '#BD3229';
                break;
        }
    }
}

function showPassword() {
  let input = document.getElementById("id_password");
  if (input.type === "password") {
    input.type = "text";
  } else {
    input.type = "password";
  }
}

function showAnswerPopup(obj) {
    report_id = obj.getAttribute('data-value');
    answer_form = document.getElementById('report-answer');
    document.getElementById("report_id").setAttribute("value", report_id);
    answer_form.style.display = "block";
}

function showReplies(obj){
    var report_id = obj.getAttribute("data-value");
    var elements = document.getElementsByClassName("all-replies");
    elements = Array.prototype.slice.call(elements)
    // show_buttons = document.getElementsByClassName("show-replies");
    var hide_buttons = document.getElementsByClassName("hide-replies");
    hide_buttons = Array.prototype.slice.call(hide_buttons);
    console.log(elements)
    elements.forEach((element) => {
        if (report_id === element.getAttribute("data-value")) {
            console.log(element.getAttribute("data-value"));
            element.style.display = "block";
            obj.style.display = "none"
            hide_buttons.forEach((button) => {
                if (report_id === button.getAttribute("data-value")){
                    button.style.display = "block";
                }
            })
        }
    })
}

function hideReplies(obj) {
    var report_id = obj.getAttribute("data-value");
    var elements = document.getElementsByClassName("all-replies");
    elements = Array.prototype.slice.call(elements);
    show_buttons = document.getElementsByClassName("show-replies");
    // var hide_buttons = document.getElementsByClassName("hide-replies");
    show_buttons = Array.prototype.slice.call(show_buttons);
    // console.log(elements);
    elements.forEach((element) => {
      if (report_id === element.getAttribute("data-value")) {
        // console.log(element.getAttribute("data-value"));
        element.style.display = "none";
        obj.style.display = "none";
        show_buttons.forEach((button) => {
          if (report_id === button.getAttribute("data-value")) {
            button.style.display = "block";
          }
        });
      }
    });
}

function hideAnswerPopup() {
    document.getElementById("report-answer").style.display = "none";
}

function refreshToSameScroll() {
    location.reload();
}