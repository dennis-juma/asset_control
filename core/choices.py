from django.db import models


class AssetStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    ASSIGNED = "ASSIGNED", "Assigned"
    IN_USE = "IN_USE", "In Use"
    RESERVED = "RESERVED", "Reserved"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    REPAIR = "REPAIR", "Repair"
    LOST = "LOST", "Lost"
    DAMAGED = "DAMAGED", "Damaged"
    RETIRED = "RETIRED", "Retired"
    DISPOSED = "DISPOSED", "Disposed"


class AssetCategory(models.TextChoices):
    HARDWARE = "HARDWARE", "Hardware"
    SOFTWARE = "SOFTWARE", "Software"
    LAPTOP = "LAPTOP", "Laptop"
    LINE = "LINE", "Sim Card"
    DESKTOP = "DESKTOP", "Desktop"
    SERVER = "SERVER", "Server"
    PRINTER = "PRINTER", "Printer"
    SCANNER = "SCANNER", "Scanner"
    ROUTER = "ROUTER", "Router"
    SWITCH = "SWITCH", "Switch"
    FIREWALL = "FIREWALL", "Firewall"
    UPS = "UPS", "UPS"
    PROJECTOR = "PROJECTOR", "Projector"
    MOBILE = "MOBILE", "Mobile"
    TABLET = "TABLET", "Tablet"
    MONITOR = "MONITOR", "Monitor"
    KEYBOARD = "KEYBOARD", "Keyboard"
    MOUSE = "MOUSE", "Mouse"
    HEADSET = "HEADSET", "Headset"
    CAMERA = "CAMERA", "Camera"
    STORAGE = "STORAGE", "Storage Device"
    NETWORKING = "NETWORKING", "Networking Equipment"
    OTHER = "OTHER", "Other"


class Condition(models.TextChoices):
    NEW = "NEW", "New"
    GOOD = "GOOD", "Good"
    FAIR = "FAIR", "Fair"
    DAMAGED = "DAMAGED", "Damaged"


class Priority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class AssignmentStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RETURNED = "RETURNED", "Returned"
    OVERDUE = "OVERDUE", "Overdue"


class MaintenanceStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class EmployeeStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    TERMINATED = "TERMINATED", "Terminated"


class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"