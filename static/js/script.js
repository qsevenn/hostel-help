function openMenu() {
    document.getElementById('menu').classList.toggle('show');
}

window.onclick = function (event) {
    if (!event.target.matches('#menu-button')) {
        let dropdown = document.getElementById('menu');
        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
}

function showAnswerPopup(obj) {
    report_id = obj.getAttribute('data-value');
    answer_form = document.getElementById('report-answer');
    document.getElementById("report_id").setAttribute("value", report_id);
    answer_form.style.display = "block";
}

function showReplies(){
    document.getElementById("all-replies").style.display = "block";
    document.getElementById("show-replies").style.display = "none";
    document.getElementById("hide-replies").style.display = "block";
}

function hideReplies() {
  document.getElementById("all-replies").style.display = "none";
  document.getElementById("hide-replies").style.display = "none";
  document.getElementById("show-replies").style.display = "block";
}

function hideAnswerPopup() {
    document.getElementById("report-answer").style.display = "none";
}

function refreshToSameScroll() {
    location.reload();
}