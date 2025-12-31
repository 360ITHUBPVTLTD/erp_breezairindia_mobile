import frappe
 
from .auth import change_password, get_current_user_details
from .attendance import get_employee_attendance
from .checkin import log_employee_checkin
from .events import get_employees_with_birthday_in_current_year
from .home import get_home_page
# from .leave import get_leave_data
 
frappe.whitelist()(get_current_user_details)
frappe.whitelist()(change_password)
frappe.whitelist()(get_home_page)
# frappe.whitelist()(get_leave_data)
frappe.whitelist()(log_employee_checkin)
frappe.whitelist()(get_employee_attendance)
frappe.whitelist()(get_employees_with_birthday_in_current_year)

from typing import Dict, List, Optional, Any
from frappe import _
from frappe.utils import getdate, nowdate, get_first_day, get_last_day
from .utils import get_employee_by_user
from .leave import get_employee_leave_data


@frappe.whitelist()
def get_leave_data(year: Optional[int] = None) -> List[Dict[str, Any]]:
	"""Get leave data for the current employee for a specific year.

	Args:
		year (Optional[int]): Year to fetch leave data for. Defaults to current year.

	Returns:
		List[Dict[str, Any]]: List of leave data dictionaries
	"""
	try:
		current_user = frappe.session.user
		if not current_user:
			frappe.throw(_("No active user session found"))

		# Get current year if not provided
		if not year:
			year = getdate(nowdate()).year

		# Validate year
		if not isinstance(year, int) or year < 1900 or year > 2100:
			frappe.throw(_("Invalid year provided: {0}").format(year))

		# Calculate date range for the year
		from_date = get_first_day(f"{year}-01-01")
		to_date = get_last_day(f"{year}-12-31")

		# Get employee data
		employee_data = get_employee_by_user(current_user)
		if not employee_data:
			frappe.throw(_("Employee data not found for current user"))

		return get_employee_leave_data([employee_data], to_date, from_date)

	except Exception as e:
		frappe.log_error(f"Error fetching leave data: {str(e)}")
		frappe.throw(_("Failed to fetch leave data {0}").format(str(e)))
