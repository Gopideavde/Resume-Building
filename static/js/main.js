// Custom JavaScript for ResumePro

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-hide toast notifications
    var toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toastNode) {
        var toast = new bootstrap.Toast(toastNode, { delay: 5000 });
        toast.show();
    });
});
