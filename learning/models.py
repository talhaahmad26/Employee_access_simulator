from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "ServerRoom"
    min_access_level = models.IntegerField()
    open_time = models.TimeField()   # e.g., 09:00
    close_time = models.TimeField()  # e.g., 11:00
    cooldown_minutes = models.IntegerField(default=0)

    def _str_(self):
        return self.name

class AccessLog(models.Model):
    """
    Keeps record when an employee accessed a room (granted).
    We store full datetime; for this assessment we assume same-day requests.
    """
    emp_id = models.CharField(max_length=64)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # when logged (or simulation time set)
    # we store simulated request_time as separate field if needed
    request_time = models.DateTimeField()

    def _str_(self):
        return f"{self.emp_id} - {self.room.name} @ {self.request_time}"