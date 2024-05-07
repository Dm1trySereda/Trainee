from celery import group, chain
from .core import parser_app

from database.core import engine
from database.models import Base
from database.repository import insert_books_sync, insert_books_history_sync

from parser import parse_the_page


@parser_app.task(name="reading_pages")
def reading_pages(page):
    return parse_the_page(page)


@parser_app.task(name="insert_books_task")
def insert_books_task(read_pages: list):
    return insert_books_sync(read_pages)


#
@parser_app.task(name="write_history_to_db")
def insert_books_history_task():
    return insert_books_history_sync()


def run_tasks():
    read_tasks = group(reading_pages.s(i) for i in range(1, 101))
    write_tasks_chain = chain(read_tasks, insert_books_task.s())
    result = write_tasks_chain.delay()
    result.get()
    insert_books_history_task.delay()


if __name__ == "__main__":
    run_tasks()
