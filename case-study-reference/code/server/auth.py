"""Sign-in for the example server.

A real service checks a signed token from its identity provider. This one accepts three fixed demo
tokens, so you can try every rule: one homeowner and two contractors.
"""

DEMO_USERS = {
    "homeowner-token": {"user_id": "u_homeowner", "display_name": "Hana Okafor"},
    "contractor-token": {"user_id": "u_contractor", "display_name": "Acme Renovations"},
    "second-contractor-token": {"user_id": "u_second_contractor", "display_name": "Bright Kitchen & Bath"},
}


def user_for_token(token):
    """Returns the user for a token, or None when the token is missing or unknown."""
    if not token:
        return None
    return DEMO_USERS.get(token)


def user_from_authorization_header(header_value):
    """Reads "Bearer <token>" from an Authorization header or gRPC metadata value."""
    if not header_value or not header_value.startswith("Bearer "):
        return None
    return user_for_token(header_value[len("Bearer "):].strip())
