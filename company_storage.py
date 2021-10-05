import asyncpg
from pydantic import BaseModel
import asyncio
import os


class NotFoundException(Exception):
    """
        Ошибка поиска сотрудника в базе данных
    """
    def __init__(self, message: str):
        self.message = message


class Employee(BaseModel):
    """
        Данные о сотруднике
    """
    name: str
    title: str
    salary: int


class CompanyStorage:
    """
        Хранилище данных о сотрудниках в PostgreSQL
    """

    def __init__(self, connection: asyncpg.Connection):
        """
        :param connection: подключение к базе данных
        """
        self.connection = connection

    async def create_table(self):
        """
            Создаст необходимую таблицу в SQLite базе данных. Таблица будет пустой.
        """
        await self.connection.execute('''
                  CREATE TABLE IF NOT EXISTS employees(
                      id serial primary key,
                      name varchar(100) NOT NULL,
                      title varchar(40) NOT NULL,
                      salary integer NOT NULL
                  )
              ''')

    async def add_employee(self, employees: Employee) -> int:
        """
            Добавляет содрудника в базу данных
        :param employees: сотрудник
        """
        return await self.connection.fetchval("""
                    INSERT INTO EMPLOYEES(name, title, salary) VALUES($1, $2, $3) RETURNING id
                """, employees.name, employees.title, employees.salary)

    async def get_employee(self, id: int) -> Employee:
        """
            Получает содрудника из базы данных
        :param id: идентификатор
        :return: данные о сотруднике
        """
        data = await self.connection.fetch('SELECT * FROM employees WHERE ID=$1', id)
        if data:
            return Employee(name=data[0][1], title=data[0][2], salary=data[0][3])
        else:
            raise NotFoundException(f"Id - {id} not found")

    async def put_employee(self, id: int, employee: Employee):
        """
            Обновляет запись о сотруднике в базе данных
        :param id: идентификатор
        :param employee: данные о сотруднике
        """
        await self.connection.execute('UPDATE EMPLOYEES set NAME=$1, TITLE=$2, SALARY=$3 where ID=$4',
                                      employee.name, employee.title, employee.salary, id
                                      )

    async def delete_employee(self, id: int):
        """
            Удаляет сотрудника из базы данных
        :param id: идентификатор
        """
        await self.connection.execute('DELETE FROM employees WHERE ID=$1', id)


async def get_connection(host: str, port: int, database: str) -> asyncpg.Connection:
    """
        Создает соединение в базу. Бескончно повторяет запрос на соединение пока успешно не получится.
    """
    while True:
        try:
            return await asyncpg.connect(
                user=os.environ["PG_USER"],
                password=os.environ["PG_PASSWORD"],
                database=database,
                host=host,
                port=port
            )
        except ConnectionError:
            print('PostgreSQL is not ready. ConnectionError')
        except Exception as e:
            print(f'PostgreSQL is not ready. {e}')

        await asyncio.sleep(1)
