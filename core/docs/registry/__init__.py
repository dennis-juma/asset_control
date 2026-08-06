from .registry import DocumentationRegistry
from .document import DocumentMetadata

registry = DocumentationRegistry()

# Import document modules after the singleton exists so their registration
# side-effects populate it before any documentation route is resolved.
from core.docs.documents import datagrid, form_builder  # noqa: F401, E402

__all__ = [
    "registry",
    "DocumentMetadata",
    "datagrid",
    "form_builder",
    
]
