document.addEventListener("DOMContentLoaded", function() {
    const inputs = Array.from(document.querySelectorAll("input[type=radio]"));

    const inputNames = [];
    for (let i = 0; i < inputs.length; i++) {
        let el = inputs[i];
        inputNames.push(el.getAttribute("name"));
    }

    console.log(inputNames);
})