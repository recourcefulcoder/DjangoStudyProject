var includeUserCheckbox = document.getElementsByName("include_users")[0];
var includeTasksCheckbox = document.getElementsByName('include_tasks')[1];

includeTasksCheckbox.disabled = true;

includeUserCheckbox.addEventListener('change', function() {
    includeTasksCheckbox.disabled = !this.checked;
    if (!this.disabled) {
        includeTasksCheckbox.checked = false;
    }
});

