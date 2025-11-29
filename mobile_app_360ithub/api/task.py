import frappe
from .common import get_doc_with_filters
from frappe.utils import getdate, today

@frappe.whitelist()
def get_task_summary():
    # user = frappe.session.user
    # tesks = get_doc_with_filters("Task", filters={"custom_task_owner": user}, limit=999999)
    pending_tasks = get_doc_with_filters("Task", filters=
[["status","not in",["Completed","Cancelled","Template"]]],  limit=9999999)

    task_without_due_date = [task for task in pending_tasks if not task.get('exp_end_date')]
    overdue_tasks = [
        task
        for task in pending_tasks
        if task.get("exp_end_date")
        and getdate(task.get("exp_end_date")) < getdate(today())
    ]
    todays_tasks = [task for task in pending_tasks if task.get("exp_end_date") == getdate(today())]
    upcoming_seven_days_tasks = [task for task in pending_tasks if task.get("exp_end_date") and getdate(task.get("exp_end_date")) > getdate(today()) and getdate(task.get("exp_end_date")) <= getdate(frappe.utils.add_days(today(), 7))]

    last_14_days_tasks = get_doc_with_filters(
        "Task",
        filters=[
            ["status", "not in", ["Cancelled", "Template"]],
            ["modified", ">=", frappe.utils.add_days(today(), -14)],
        ],
        limit=9999999,
    )

    last_14_days_todo = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Open"
    ]
    last_14_days_in_progress = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Working"
    ]
    last_14_days_review = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Pending Review"
    ]
    last_14_days_completed = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Completed"
    ]
    last_14_days_urgent_completed = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Completed" and task.get("priority") == "Urgent"
    ]
    last_14_days_high_completed = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Completed" and task.get("priority") == "High"
    ]
    last_14_days_medium_completed = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Completed" and task.get("priority") == "Medium"
    ]
    last_14_days_low_completed = [
        task
        for task in last_14_days_tasks
        if task.get("status") == "Completed" and task.get("priority") == "Low"
    ]

    return {
        "total_tasks": len(pending_tasks),
        "tasks_without_due_date": len(task_without_due_date),
        "overdue_tasks": len(overdue_tasks),
        "todays_tasks": len(todays_tasks),
        "upcoming_seven_days_tasks": len(upcoming_seven_days_tasks),
        "last_14_days_todo": len(last_14_days_todo),
        "last_14_days_in_progress": len(last_14_days_in_progress),
        "last_14_days_review": len(last_14_days_review),
        "last_14_days_completed": len(last_14_days_completed),
        "last_14_days_urgent_completed": len(last_14_days_urgent_completed),
        "last_14_days_high_completed": len(last_14_days_high_completed),
        "last_14_days_medium_completed": len(last_14_days_medium_completed),
        "last_14_days_low_completed": len(last_14_days_low_completed),
        # "last_14_days": last_14_days_tasks
    }