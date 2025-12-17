from typing import Dict
from uuid import UUID
from .models import Application
from .errors import NotFoundError

class InMemoryApplicationStore:
    def __init__(self) -> None:
        self._items: Dict[UUID, Application] = {}

    def create(self, app: Application) -> Application:
        self._items[app.id] = app
        return app

    def get(self, app_id: UUID) -> Application:
        found = self._items.get(app_id)
        if not found:
            raise NotFoundError(message="Application not found", details={"id": str(app_id)})
        return found
