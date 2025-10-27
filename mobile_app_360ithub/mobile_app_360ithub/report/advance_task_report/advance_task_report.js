frappe.query_reports["Advance Task Report"] = {
    "filters": [
        {
            "fieldname": "task_owner",
            "label": __("Task Owner"),
            "fieldtype": "Link",
            "options": "User",
            "width": "120"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nOpen\nWorking\nOverdue\nCompleted\nCancelled",
            "width": "100"
        },
        {
            "fieldname": "priority",
            "label": __("Priority"),
            "fieldtype": "Select",
            "options": "\nLow\nMedium\nHigh\nUrgent",
            "width": "100"
        },
        {
            "fieldname": "type",
            "label": __("Type"),
            "fieldtype": "Link",
            "options": "Task Type",
            "width": "120"
        },
        {
            "fieldname": "exp_end_date",
            "label": __("Expected End Date"),
            "fieldtype": "DateRange",
            "width": "180"
        },
        {
            "fieldname": "timespan",
            "label": __("Timespan"),
            "fieldtype": "Select",
            "options": "\nToday\nThis Week\nThis Month\nOverdue",
            "width": "120"
        }
    ]
};
