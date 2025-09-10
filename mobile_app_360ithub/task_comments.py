import frappe

def publish_task_comment_event(doc, method):
    """
    Publishes a real-time event when a new comment is added to a Task.
    """
    if doc.reference_doctype == 'Task' and frappe.db.exists("Task", doc.reference_name):
        task_id = doc.reference_name

        data = {
            "task_id": task_id,
            "comment_content": doc.content,
            "comment_by": doc.owner,
            "comment_name": doc.name
        }

        # Event name follows the convention: `[event_type]_[doctype]`
        event_name = "new_task_comment:" + task_id

        # Room is specific to the task, so clients can listen to a particular task's events
        # room_name = f"task_events:{task_id}"

        frappe.publish_realtime(
            event=event_name,
            message=data,
            # room=room_name
        )


def delete_task_comment_event(doc, method):
    if doc.reference_doctype == 'Task' and frappe.db.exists("Task", doc.reference_name):
        task_id = doc.reference_name

        data = {
            "task_id": task_id,
            "comment_name": doc.name
        }
        event_name = "new_task_comment:" + task_id

        frappe.publish_realtime(
            event=event_name,
            message=data,
            # room=room_name
        )
