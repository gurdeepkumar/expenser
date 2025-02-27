document.addEventListener("DOMContentLoaded", function () {
    // Toggle filter options visibility
    document.getElementById("filterToggleBtn").addEventListener("click", function () {
        var filterDiv = document.getElementById("filterOptions");
        filterDiv.style.display = filterDiv.style.display === "none" || filterDiv.style.display === "" ? "block" : "none";
    });

    // Handle row click to navigate
    document.querySelectorAll("tr[data-href]").forEach(row => {
        row.addEventListener("click", function () {
            console.log("Row clicked:", this.dataset.href);
            window.location.href = this.dataset.href;
        });
    });
});

