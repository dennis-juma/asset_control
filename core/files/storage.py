from django.core.files.storage import default_storage


class FileStorageService:

    @staticmethod
    def save(uploaded_file, folder):

        filename = default_storage.save(
            f"{folder}/{uploaded_file.name}",
            uploaded_file,
        )

        return filename

    @staticmethod
    def url(path):

        return default_storage.url(path)