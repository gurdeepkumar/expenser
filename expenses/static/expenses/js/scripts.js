document.addEventListener("DOMContentLoaded", function () {
    // Toggle filter options visibility
    var filterToggleBtn = document.getElementById("filterToggleBtn");
    var filterDiv = document.getElementById("filterOptions");

    if (filterToggleBtn && filterDiv) {
        filterToggleBtn.addEventListener("click", function () {
            filterDiv.style.display = (filterDiv.style.display === "none" || filterDiv.style.display === "") ? "block" : "none";
        });
    }

    // Handle row click to navigate
    document.querySelectorAll("tr[data-href]").forEach(row => {
        row.addEventListener("click", function () {
            var href = this.dataset.href;
            if (href) {
                console.log("Row clicked:", href);
                window.location.href = href;
            }
        });
    });

});
