import enum


class UserRole(str, enum.Enum):
    TRAINEE = "TRAINEE"
    EMPLOYER = "EMPLOYER"
    ADMIN = "ADMIN"


class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW = "INTERVIEW"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
