import frappe
from frappe import _
from frappe.model.db_query import DatabaseQuery
from frappe.model.utils import is_virtual_doctype
from frappe.model.base_document import get_controller
import json



@frappe.whitelist()  
def get_permitted_doctypes(user=None):  
    if not user:  
        user = frappe.session.user  
      
    user_perms = frappe.utils.user.UserPermissions(user)  
    user_perms.build_permissions()  
      
    return {  
        "can_read": user_perms.can_read,  
        "can_write": user_perms.can_write,  
        "can_create": user_perms.can_create,  
        "can_delete": user_perms.can_delete,  
        # Add other permission types as needed  
    }






@frappe.whitelist()
def get_doc_with_filters(doctype, filters=None, fields=None, limit=20, order_by=None, group_by=None, start=0):
    """Get a list of documents with filters, optimized for REST API usage.

    This function mirrors the powerful querying capabilities of `frappe.desk.reportview.get_list`
    but returns data in a structured, uncompressed format suitable for APIs. It supports
    various filter formats, pagination, sorting, and grouping.

    Args:
        doctype (str): The Doctype to query.
        filters (list | dict | str, optional): Filters to apply. Can be:
            - A list of lists (standard Frappe format): `[["status", "=", "Open"]]`
            - A dictionary: `{"status": "Open", "priority": "High"}`
            - A JSON string representation of a list or dict.
            Defaults to None.
        fields (list, optional): Fields to fetch. Defaults to `['*']`.
        limit (int, optional): Number of records to return. Defaults to 10.
        order_by (str, optional): Field to order by. Defaults to 'modified desc'.
        group_by (str, optional): Field to group by. Defaults to None.
        start (int, optional): Start index for pagination. Defaults to 0.

    Returns:
        list[dict]: A list of documents, where each document is a dictionary.
    """

    # Prepare arguments similar to reportview.get_form_params()
    args = frappe._dict({
        'doctype': doctype,
        'filters': filters or [],
        'fields': fields or ['*'],
        'limit_page_length': limit,
        'limit_start': start,
        'order_by': order_by or 'modified desc',
        'group_by': group_by
    })

    # Parse JSON strings like reportview.parse_json() does
    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except (ValueError, TypeError):
            pass  # If parsing fails, use as-is

    # Update args with parsed filters
    args['filters'] = filters or []

    # Handle different filter formats
    if isinstance(args.filters, dict):
        # Convert dict filters to standard Frappe list format
        filter_list = []
        for key, value in args.filters.items():
            if isinstance(value, list) and len(value) >= 2:
                # Handle complex filters like ['>', 100] or ['in', [1,2,3]]
                operator = value[0]
                filter_value = value[1]
                filter_list.append([key, operator, filter_value])
            else:
                # Simple equality filter
                filter_list.append([key, '=', value])
        args.filters = filter_list
    elif isinstance(args.filters, list):
        # Check if it's already in proper 3-element format like [["field", "operator", value]]
        # If so, keep as is. This handles cases like [["exp_end_date", "Timespan", tomorrow]]
        if args.filters and isinstance(args.filters[0], list) and len(args.filters[0]) == 3:
            # Already in proper format, keep as is
            pass
        elif args.filters and not isinstance(args.filters[0], list):
            # Single filter condition, ensure it's properly wrapped
            if len(args.filters) == 3:
                args.filters = [args.filters]  # Wrap single condition in list
    else:
        # Ensure filters is always a list
        args.filters = [args.filters] if args.filters else []

    # Filters are now properly formatted for DatabaseQuery

    try:
        # Use the exact same logic as reportview.get_list()
        if is_virtual_doctype(args.doctype):
            controller = get_controller(args.doctype)
            data = controller.get_list(args)
        else:
            # Use DatabaseQuery directly like reportview does (uncompressed format)
            # Pass all args as kwargs except doctype (which is used in constructor)
            doctype = args.pop('doctype')  # Remove doctype from args
            data = DatabaseQuery(doctype).execute(**args)

        return data

    except Exception as e:
        frappe.log_error(f"Error in get_doc_with_filters: {str(e)}")
        frappe.throw(_(f"Failed to fetch {doctype} records: {str(e)}"))