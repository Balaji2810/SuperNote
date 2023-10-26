from enum import Enum


class UserEnum(Enum):
    student = "student"
    instructor = "instructor"
    sub_admin = "sub_admin"
    admin = "admin"


class StatusEnum(Enum):
    completed = "completed"
    rescheduled = "rescheduled"
    cancled = "cancled"
    active = "active"
    dropped = "dropped"
    accepted = "accepted"
    rejected = "rejected"

