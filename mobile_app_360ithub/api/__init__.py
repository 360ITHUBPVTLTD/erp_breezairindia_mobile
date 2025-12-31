import frappe
 
from .auth import change_password, get_current_user_details
from .attendance import get_employee_attendance
from .checkin import log_employee_checkin
from .events import get_employees_with_birthday_in_current_year
from .home import get_home_page
from .leave import get_leave_data
 
frappe.whitelist()(get_current_user_details)
frappe.whitelist()(change_password)
frappe.whitelist()(get_home_page)
frappe.whitelist()(get_leave_data)
frappe.whitelist()(log_employee_checkin)
frappe.whitelist()(get_employee_attendance)
frappe.whitelist()(get_employees_with_birthday_in_current_year)
