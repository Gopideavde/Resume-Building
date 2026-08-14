from payments.models import PremiumAccess

def user_can_use_template(user, template):
    """
    Checks if a user is authorized to use a template.
    A user can use a template if it is free, or if they have an active PremiumAccess record.
    """
    if not template.is_premium:
        return True
    
    if not user.is_authenticated:
        return False
        
    return PremiumAccess.objects.filter(user=user, template=template).exists()
