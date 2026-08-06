class AuditBuilder:

    def __init__(self):

        self.dto = AuditDTO(...)

    def before(self, data):

        self.dto.before = data

        return self

    def after(self, data):

        self.dto.after = data

        return self

    def metadata(self, data):

        self.dto.metadata = data

        return self

    def build(self):

        return self.dto