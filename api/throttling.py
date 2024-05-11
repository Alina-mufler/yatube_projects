from rest_framework import throttling
import datetime


class LunchBreakThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        now = datetime.datetime.now().hour
        if now >= 9 and now <= 10:
            return False
        return True