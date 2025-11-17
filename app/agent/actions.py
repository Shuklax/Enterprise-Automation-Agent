from typing import Dict, Any

def determine_action(category: str, data: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """
    Determine what action to take based on category and data
    Returns (action_type, action_params)
    """
    
    if category == "high_value_order":
        return "approve_order", {
            "order_id": data.get("order_id"),
            "amount": data.get("amount")
        }
    
    elif category == "suspicious_activity":
        return "flag_for_review", {
            "order_id": data.get("order_id"),
            "reason": "Suspicious pattern detected"
        }
    
    elif category == "urgent_request":
        return "send_notification", {
            "recipient": "support@company.com",
            "priority": "high",
            "subject": f"Urgent: {data.get('order_id')}"
        }
    
    elif category == "routine_processing":
        return "update_status", {
            "entity_id": data.get("order_id"),
            "new_status": "processed"
        }
    
    else:
        return "update_status", {
            "entity_id": data.get("order_id", "unknown"),
            "new_status": "reviewed"
        }