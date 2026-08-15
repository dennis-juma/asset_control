import csv
import io

from ..base import BaseImporter
from ..exceptions import ImportFileError


class CSVImporter(BaseImporter):

    def read(self, uploaded_file):

        try:
            content = uploaded_file.read()

            if isinstance(content, bytes):
                content = content.decode("utf-8-sig")

            reader = csv.DictReader(
                io.StringIO(content)
            )

            if not reader.fieldnames:
                raise ImportFileError(
                    "The CSV file does not contain headers."
                )

            return list(reader)

        except UnicodeDecodeError as exc:
            raise ImportFileError(
                "The CSV file must use UTF-8 encoding."
            ) from exc