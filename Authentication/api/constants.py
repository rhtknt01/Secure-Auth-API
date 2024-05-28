#api/constants.py (all constants are defined here)
# api/error_codes.py

# Error Codes
ACCESS_TOKEN_NOT_FOUND = 1001
ACCESS_TOKEN_BLACKLISTED = 1002
ACCESS_TOKEN_EXPIRED = 1003
REFRESH_TOKEN_NOT_FOUND = 1004
REFRESH_TOKEN_BLACKLISTED = 1005
REFRESH_TOKEN_EXPIRED = 1006
USER_NOT_EXISTS = 1007
INVALID_CREDENTIALS = 1008
DISSIMILAR_PASSWORD = 1009
SERIALIZER_DATA_INVALID = 1010

# Success Codes
REGISTRATION_SUCCESS = 2001
LOGIN_SUCCESS = 2002
PASSWORD_CHANGED_SUCCESS = 2003
PASSWORD_RESET_SUCCESS = 2004
EMAIL_SEND_SUCCESS = 2005
OTP_SEND_SUCCESS = 2006
LOGOUT_SUCCESS = 2007
TOKEN_REFRESH_SUCCESS = 2008

# Error Messages
ERROR_MESSAGES = {
    ACCESS_TOKEN_NOT_FOUND: "Access token not found in cookies.",
    ACCESS_TOKEN_BLACKLISTED: "Access token blacklisted. You need to login again.",
    ACCESS_TOKEN_EXPIRED: "Access token expired. Please refresh the token.",
    REFRESH_TOKEN_NOT_FOUND: "Refresh token not found in cookies.",
    REFRESH_TOKEN_BLACKLISTED: "Refresh token blacklisted. You need to login again.",
    REFRESH_TOKEN_EXPIRED: "Refresh token expired. You need to login again.",
    USER_NOT_EXISTS: "User does not exist. Invalid credentials.",
    INVALID_CREDENTIALS: "Invalid credentials provided.",
    DISSIMILAR_PASSWORD: "Re-entered password does not match the original.",
    SERIALIZER_DATA_INVALID: "serializer data is not invalid"
}

# Success Messages
SUCCESS_MESSAGES = {
    REGISTRATION_SUCCESS: "User registration successful.",
    LOGIN_SUCCESS: "Login successful.",
    PASSWORD_CHANGED_SUCCESS: "Password changed successfully.", #login again after password changed
    PASSWORD_RESET_SUCCESS: "Password reset successful.",
    EMAIL_SEND_SUCCESS: "Email sent successfully.",
    OTP_SEND_SUCCESS: "OTP sent successfully.",
    LOGOUT_SUCCESS: "Logout successful.",
    TOKEN_REFRESH_SUCCESS: "Token refreshed successfully.",
}
