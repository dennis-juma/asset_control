document.addEventListener("DOMContentLoaded", function () {

    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".bulk-select-checkbox");
    const bulkActions = document.getElementById("bulk-actions");
    const selectedCount = document.getElementById("selected-count");
    const clearSelection = document.getElementById("clear-selection");

    function updateBulkActions() {

        const selected = document.querySelectorAll(
            ".bulk-select-checkbox:checked"
        );

        const count = selected.length;

        selectedCount.textContent = count;

        if (count > 0) {
            bulkActions.classList.remove("d-none");
        } else {
            bulkActions.classList.add("d-none");
        }

        if (selectAll) {
            selectAll.checked =
                checkboxes.length > 0 &&
                count === checkboxes.length;

            selectAll.indeterminate =
                count > 0 &&
                count < checkboxes.length;
        }
    }

    if (selectAll) {

        selectAll.addEventListener("change", function () {

            checkboxes.forEach(function (checkbox) {
                checkbox.checked = selectAll.checked;
            });

            updateBulkActions();
        });
    }

    checkboxes.forEach(function (checkbox) {

        checkbox.addEventListener(
            "change",
            updateBulkActions
        );

    });

    if (clearSelection) {

        clearSelection.addEventListener("click", function () {

            checkboxes.forEach(function (checkbox) {
                checkbox.checked = false;
            });

            if (selectAll) {
                selectAll.checked = false;
                selectAll.indeterminate = false;
            }

            updateBulkActions();
        });
    }

    const bulkUpdateForm = document.getElementById("bulk-update-form");

    if (bulkUpdateForm) {
        bulkUpdateForm.addEventListener("submit", function () {
            bulkUpdateForm.querySelectorAll("input[name='selected_ids']")
                .forEach(function (input) {
                    input.remove();
                });

            document.querySelectorAll(".bulk-select-checkbox:checked")
                .forEach(function (checkbox) {
                    const input = document.createElement("input");
                    input.type = "hidden";
                    input.name = "selected_ids";
                    input.value = checkbox.value;
                    bulkUpdateForm.appendChild(input);
                });
        });
    }

    updateBulkActions();
});
