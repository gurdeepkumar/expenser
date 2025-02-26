document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("filterToggleBtn").addEventListener("click", function () {
        var filterDiv = document.getElementById("filterOptions");
        filterDiv.style.display = filterDiv.style.display === "none" || filterDiv.style.display === "" ? "block" : "none";
    });
});
