document.addEventListener("DOMContentLoaded", () => {

    // Sidebar collapse
    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".sidebar");

    if (toggle && sidebar) {
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
        });
    }

    // Expand/collapse submenus
    document.querySelectorAll(".menu-link").forEach(link => {

        const submenu = link.nextElementSibling;

        if (!submenu || !submenu.classList.contains("submenu")) {
            return;
        }

        link.addEventListener("click", function (event) {

            event.preventDefault();

            submenu.classList.toggle("expanded");
            link.classList.toggle("open");

        });

    });

});