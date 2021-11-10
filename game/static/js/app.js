document.addEventListener("DOMContentLoaded", function() {
    function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
    }

    // Get unique names of quizitems
    const inputs = Array.from(document.querySelectorAll("input[type=radio]"));
    const quizItemIds = [];
    for (let i = 0; i < inputs.length; i++) {
        let el = inputs[i];
        quizItemIds.push(el.getAttribute("name"));
    }
    const uniqueQuizItemIds = quizItemIds.filter(onlyUnique);

    // Inform if any of the answers weren't chosen
    const button = document.querySelector("button[type=submit]");
    button.addEventListener("click", function() {
        const unanswered = [];
        for (let i = 0; i < 10; i++) {
            let quizItemId = uniqueQuizItemIds[i];
            let divQuestionContainer = document.getElementById(quizItemId);
            let counter = divQuestionContainer.dataset["counter"];
            let quizitemChecked = document.querySelector("input[name='" + quizItemId + "']:checked");
            if (quizitemChecked == null) {
                unanswered.push(counter);
            }
        }

        if (unanswered.length > 0) {
            let message = "";
            if (unanswered.length === 1) {
                message += "Proszę zaznacz odpowiedź do pytania: ";
            } else {
                message += "Proszę zaznacz odpowiedzi do pytań: ";
            }
            message += unanswered.join(", ");
            message += "."
            alert(message);
        }
    })
})