# middlewares.py
import firebase_admin
from firebase_admin import auth
from django.http import JsonResponse

class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        id_token = None
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                id_token = parts[1]

        if id_token:
            try:
                decoded_token = auth.verify_id_token(id_token)
                request.firebase_user = decoded_token
            except Exception as e:
                return JsonResponse({"error": "Invalid authentication token."}, status=401)
        else:
            request.firebase_user = None

        return self.get_response(request)
