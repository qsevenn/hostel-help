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

function showAnswerPopup(report_id) {
    document.getElementById("report-answer").style.display = "block";
    // current_report = document.getElementById(report_id);
    // form = current_report.getElementById("report_answer").style.display =
    //   "block";
    
    // answer_forms = document.getElementsByName("rpt_id")
    // answer_forms.forEach((form) => {
    //   if (form.value == parseInt(report_id)) {
    //     form.getElementById("report-answer").style.display = "block";
    //     form
    //       .getElementById("report-answer")
    //       .getElementsByName("report_id")[0].value = parseInt(report_id);
    //   }
    // });
}


function hideAnswerPopup() {
    document.getElementById("report-answer").style.display = "none";
}

function refreshToSameScroll() {
    location.reload();
}