from enum import Enum


class AuditAction(str, Enum):

    CREATE = "CREATE"

    UPDATE = "UPDATE"

    DELETE = "DELETE"

    VIEW = "VIEW"

    LOGIN = "LOGIN"

    LOGOUT = "LOGOUT"

    EXPORT = "EXPORT"

    IMPORT = "IMPORT"

    DOWNLOAD = "DOWNLOAD"

    PRINT = "PRINT"

    ASSIGN = "ASSIGN"

    TRANSFER = "TRANSFER"

    RETURN = "RETURN"

    APPROVE = "APPROVE"

    REJECT = "REJECT"