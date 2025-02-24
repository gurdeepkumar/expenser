document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("filterToggleBtn").addEventListener("click", function () {
        var filterDiv = document.getElementById("filterOptions");
        filterDiv.style.display = filterDiv.style.display === "none" || filterDiv.style.display === "" ? "block" : "none";
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("filterToggleBtn").addEventListener("click", function () {
        var searchDiv = document.getElementById("filterOptionsHide");
        searchDiv.style.display = searchDiv.style.display === "block" || searchDiv.style.display === "none" ? "block" : "none";
    });
});
    