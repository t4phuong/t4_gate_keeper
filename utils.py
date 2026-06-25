import pytz
# pyrefly: ignore [missing-import]
from odoo import fields

def get_local_datetime(dt, env):
    """Convert a UTC Datetime or a string representing it into a timezone-aware datetime in the user's timezone."""
    if not dt:
        return None
    if isinstance(dt, str):
        dt = fields.Datetime.to_datetime(dt)
    
    # Get user timezone (default to UTC if not set)
    user_tz = env.user.tz or 'UTC'
    
    # Ensure tzinfo is set to UTC first (Odoo stores Datetime fields in UTC without tzinfo)
    if not dt.tzinfo:
        dt = pytz.utc.localize(dt)
        
    return dt.astimezone(pytz.timezone(user_tz))

def check_outside_working_hours(dt, env, start_hour=8, end_hour=17):
    """
    Evaluate if a datetime falls outside standard working hours or on weekends in the user's local timezone.
    Returns:
        (is_outside, reason)
    """
    local_dt = get_local_datetime(dt, env)
    if not local_dt:
        return False, ""

    # Check weekend (Saturday = 5, Sunday = 6)
    if local_dt.weekday() >= 5:
        day_name = local_dt.strftime('%A')
        return True, f"Access on weekend ({day_name})"
        
    # Check hours (before 08:00 or after 17:00)
    if local_dt.hour < start_hour or local_dt.hour >= end_hour:
        time_str = local_dt.strftime('%H:%M')
        return True, f"Access outside working hours ({time_str})"
        
    return False, ""
