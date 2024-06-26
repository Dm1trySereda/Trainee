from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.history import UpdateHistory
from src.services.update_history_service.abc import AbstractUpdateHistoryService


class RepositoryUpdateHistoryService(AbstractUpdateHistoryService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.history_updater = UpdateHistory(session)

    async def update_history(self):
        return await self.history_updater.update_books_history()
