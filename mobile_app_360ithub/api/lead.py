import frappe


@frappe.whitelist()
def get_lead_contacts(lead_name):
    lead = frappe.get_doc("Lead", lead_name)
    return {
        "name": lead.name,
        "lead_name": lead.lead_name,
        "email_id": lead.email_id,
        "mobile_no": lead.mobile_no,
        "company_name": lead.company_name,
        "status": lead.status,
        "custom_site_role": lead.custom_site_role,
    }

