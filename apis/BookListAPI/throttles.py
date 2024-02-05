from rest_framework.throttling import UserRateThrottle

class TenCallsPerMinuteThrottle(UserRateThrottle):
    scope = 'ten'