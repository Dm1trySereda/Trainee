from typing import Sequence

from sqlalchemy import and_, asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Book, BooksHistory


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class DeleteEntity(BaseRepository):
    def __init__(self, model, session):
        super().__init__(session)
        self.model = model

    async def delete(self, **kwargs):
        delete_values = [
            getattr(self.model, key) == value
            for key, value in kwargs.items()
            if value is not None
        ]
        stmt = delete(self.model).where(and_(*delete_values))
        await self.async_session.execute(stmt)


class SearchBook(BaseRepository):

    async def select_book(
        self, book_id: int, book_num: int, title: str
    ) -> Sequence[Book]:
        select_values = list()

        if book_id:
            select_values.append(Book.id == book_id)
        if book_num:
            select_values.append(Book.book_num == book_num)
        if title:
            select_values.append(Book.title.contains(title))

        stmt = select(Book).where(and_(*select_values))
        result = await self.async_session.execute(stmt)

        return result.scalars().all()


class UpdateBook(BaseRepository):
    async def update_book(
        self,
        book_num: int,
        new_title: str = None,
        new_author: str = None,
        new_price: float = None,
        new_rating: float = None,
        new_image: str = None,
    ) -> None:
        update_values = dict()
        if new_title is not None:
            update_values["title"] = new_title
        if new_author is not None:
            update_values["author"] = new_author
        if new_price is not None:
            update_values["price_new"] = new_price
        if new_rating is not None:
            update_values["rating"] = new_rating
        if new_image is not None:
            update_values["image"] = new_image
        stmt = update(Book).where(Book.book_num == book_num).values(**update_values)
        await self.async_session.execute(stmt)


class InsertBook(BaseRepository):
    async def insert_new_book(
        self,
        book_num: int,
        title: str,
        author: str,
        price: float,
        rating: float,
        image: str,
    ) -> None:
        stmt = select(Book).where(Book.book_num == book_num)
        result = await self.async_session.execute(stmt)
        existing_book = result.scalars().first()
        if existing_book is None:
            new_book = Book(
                book_num=book_num,
                title=title,
                author=author,
                price_new=price,
                rating=rating,
                image=image,
            )
            self.async_session.add(new_book)
        else:
            book_updater = UpdateBook(self.async_session)
            await book_updater.update_book(
                book_num=book_num,
                new_title=title,
                new_author=author,
                new_price=price,
                new_rating=rating,
                new_image=image,
            )


class DeleteBook(DeleteEntity):
    def __init__(self, session):
        super().__init__(Book, session)


class DeleteBookHistory(DeleteEntity):
    def __init__(self, session):
        super().__init__(BooksHistory, session)

    async def delete_book_history(self, book_id=None, book_num=None):
        await self.delete(book_id=book_id, book_num=book_num)
        book_deleter = DeleteBook(self.async_session)
        await book_deleter.delete(book_id=book_id, book_num=book_num)


class Paginate(BaseRepository):
    async def select_books(
        self, page: int, books_quantity: int, sort_by: str, order_asc: bool
    ) -> Sequence[Book]:
        books_quantity = books_quantity or 10
        books_offset = (page - 1) * books_quantity
        sort_params = getattr(Book, sort_by) if hasattr(Book, sort_by) else Book.title
        sort_order = asc(sort_params) if order_asc else desc(sort_params)
        stmt = (
            select(Book).limit(books_quantity).offset(books_offset).order_by(sort_order)
        )
        result = await self.async_session.execute(stmt)
        return result.scalars().all()


class RepetitiveBook(BaseRepository):
    async def select_book_history(self):
        stmt = (
            select(BooksHistory.book_num)
            .group_by(BooksHistory.book_num)
            .having(func.count(BooksHistory.book_num) > 1)
        )
        result = await self.async_session.execute(stmt)

        duplicate_book_nums = result.scalars().all()
        duplicated_books = list()
        for book_num in duplicate_book_nums:
            stmt = select(BooksHistory).where(BooksHistory.book_num == book_num)
            result = await self.async_session.execute(stmt)
            duplicated_books.extend(result.scalars().all())

        return duplicated_books