from django import template
import math

register = template.Library()

@register.filter
def rupee_paise(value):
    try:
        val = float(value)
        rupees = int(val)
        paise = int(round((val - rupees) * 100))
        
        # Handle formatting
        result = f"{rupees} Rupees"
        if paise > 0:
            result += f" & {paise} Paise"
        elif paise == 0 and rupees == 0:
             # Handle 0 case if needed, maybe just 0 Rupees
             pass
             
        return result
    except (ValueError, TypeError):
        return value
