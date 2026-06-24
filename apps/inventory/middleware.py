from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def log_action(user, action, target_type, target_id, details='', ip_address=None):
        try:
            AuditLog.objects.create(
                user=user,
                action=action,
                target_type=target_type,
                target_id=str(target_id),
                details=details,
                ip_address=ip_address
            )
        except Exception as e:
            print(f"Audit log error: {e}")
