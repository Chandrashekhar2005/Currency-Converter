// =============================
// Live Currency Converter
// script.js
// =============================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    const amount = document.querySelector("input[name='amount']");
    const base = document.querySelector("select[name='base']");
    const target = document.querySelector("select[name='target']");
    const clearBtn = document.querySelector(".clear-btn");

    // -------------------------
    // Keyboard Shortcut
    // Press Enter to Submit
    // -------------------------
    document.addEventListener("keydown", function(e){

        if(e.key === "Enter"){
            form.submit();
        }

    });

    // -------------------------
    // Clear Form
    // -------------------------
    clearBtn.addEventListener("click", function(){

        amount.value = "";

        base.selectedIndex = 0;

        target.selectedIndex = 1;

    });

    // -------------------------
    // Swap Currency
    // -------------------------

    const swapBtn = document.createElement("button");

    swapBtn.type = "button";

    swapBtn.innerHTML = "🔄 Swap";

    swapBtn.style.background = "#0d6efd";

    swapBtn.style.color = "white";

    swapBtn.style.marginTop = "15px";

    swapBtn.style.width = "100%";

    swapBtn.style.padding = "12px";

    swapBtn.style.border = "none";

    swapBtn.style.borderRadius = "10px";

    swapBtn.style.cursor = "pointer";

    document.querySelector(".buttons").after(swapBtn);

    swapBtn.addEventListener("click", function(){

        let temp = base.value;

        base.value = target.value;

        target.value = temp;

    });

    // -------------------------
    // Save History
    // -------------------------

    const result = document.querySelector(".result");

    if(result){

        const saveBtn = document.createElement("button");

        saveBtn.type = "button";
        saveBtn.innerHTML = "💾 Save History";

        saveBtn.style.background = "#28a745";
        saveBtn.style.color = "white";
        saveBtn.style.marginTop = "15px";
        saveBtn.style.width = "100%";
        saveBtn.style.padding = "12px";
        saveBtn.style.border = "none";
        saveBtn.style.borderRadius = "10px";
        saveBtn.style.cursor = "pointer";

        result.appendChild(saveBtn);

        saveBtn.addEventListener("click", function(){

            fetch("/save_history",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    result:result.innerText
                })
            })
            .then(response=>response.json())
            .then(data=>{
                alert(data.message);
            });

        });

    }

    // -------------------------
    // Clear Conversion Result
    // -------------------------

    const clearResultBtn = document.getElementById("clearResultBtn");

    if (clearResultBtn) {

        clearResultBtn.addEventListener("click", function () {

            // Clear amount
           amount.value = "";

            // Reset currencies
            base.selectedIndex = 0;
            target.selectedIndex = 1;

            // Hide conversion result
            const resultSection = document.getElementById("resultSection");

            if (resultSection) {
                resultSection.style.display = "none";
            }

        });

    }

    // -------------------------
    // Dark / Light Mode
    // -------------------------

    const themeToggle = document.getElementById("themeToggle");

    // Restore saved theme
    if(localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        themeToggle.innerHTML = "☀️ Light Mode";
    }

    themeToggle.addEventListener("click", function(){

        document.body.classList.toggle("dark-mode");

        if(document.body.classList.contains("dark-mode")){
            themeToggle.innerHTML = "☀️ Light Mode";
            localStorage.setItem("theme","dark");
        }else{
            themeToggle.innerHTML = "🌙 Dark Mode";
            localStorage.setItem("theme","light");
        }

    });

});