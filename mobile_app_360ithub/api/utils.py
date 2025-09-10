import frappe

def get_employee_by_user(user, fields=["*"]):
    if isinstance(fields, str):
        fields = [fields]
    emp_data = frappe.db.get_value(
        "Employee",
        {"user_id": user},
        fields,
        as_dict=1,
    )
    return emp_data
@frappe.whitelist()
def get_last_log_details(emp_id=None):
    """
    Get the last log type and time of the given employee

    Args:
        emp_id (str): The employee id for which the last log needs to be retrieved.
            If not provided, the employee id of the current user is used.

    Returns:
        dict: The last log's type and time.
    """
    if not emp_id:
        emp_id = get_employee_by_user(frappe.session.user).get("name")
    last_log = frappe.db.get_value(
        "Employee Checkin",
        {"employee": emp_id},
        ["log_type", "time"],
        order_by="time DESC",
        as_dict=1,
    )
    return last_log
