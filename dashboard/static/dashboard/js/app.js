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


document.addEventListener("DOMContentLoaded", function () {

    const assignmentType = document.querySelectorAll(
        'input[name="assignment_type"]'
    );

    const employeeGroup =
        document.getElementById("div_id_employee");

    const siteGroup =
        document.getElementById("div_id_site");

    function toggleFields() {

        const value =
            document.querySelector(
                'input[name="assignment_type"]:checked'
            ).value;

        if (value === "EMPLOYEE") {

            employeeGroup.style.display = "";

            siteGroup.style.display = "none";

        } else {

            employeeGroup.style.display = "none";

            siteGroup.style.display = "";

        }
    }

    assignmentType.forEach(function (radio) {

        radio.addEventListener(
            "change",
            toggleFields,
        );

    });

    toggleFields();

});