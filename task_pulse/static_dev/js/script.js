document.addEventListener("DOMContentLoaded", function() {
    var hamburger = document.querySelector(".collapse-btn");
    var body = document.querySelector("body");
    var sidebar = document.querySelector(".sidebar");
    
    if (hamburger) {
        hamburger.addEventListener("click", function() {
            console.log(1);
            body.classList.toggle("active");
            sidebar.classList.toggle("collapsed");
        });
    }
});
    
