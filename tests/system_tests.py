from unittest import IsolatedAsyncioTestCase
import aiohttp
from company_storage import Employee
from server import ResourceId


BASE_URL = 'http://0.0.0.0:8000/employees'
EMPLOYEE_A = Employee(name="John", title="manager", salary=60000)
EMPLOYEE_B = Employee(name="Jane", title="engineer", salary=70000)


class SystemTests(IsolatedAsyncioTestCase):
    """
        Для запуска тестов должны быть запущены сервер и PostgreSQL
    """

    async def _get(self, id: int) -> Employee:
        url = f"{BASE_URL}/{id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                self.assertEqual(response.status, 200)
                r = await response.json()
                return r

    async def _get_status(self, id: int) -> int:
        url = f"{BASE_URL}/{id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status

    async def _post(self, employee: Employee) -> int:
        url = f"{BASE_URL}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=employee.dict()) as response:
                self.assertEqual(response.status, 200)
                body = await response.json()
                return ResourceId.parse_obj(body).id

    async def _put(self, id: int, employee: Employee):
        url = f"{BASE_URL}/{id}"
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=employee.dict()) as response:
                self.assertEqual(response.status, 200)

    async def _delete(self, id: int):
        url = f"{BASE_URL}/{id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                self.assertEqual(response.status, 200)

    async def test_create(self):
        employee_id = await self._post(EMPLOYEE_A)
        employee = await self._get(employee_id)
        self.assertEqual(employee, EMPLOYEE_A)

    async def test_update(self):
        employee_id = await self._post(EMPLOYEE_A)
        await self._put(employee_id, EMPLOYEE_B)
        employee = await self._get(employee_id)
        self.assertEqual(employee, EMPLOYEE_B)
    
    async def test_delete(self):
        employee_id = await self._post(EMPLOYEE_A)
        await self._delete(employee_id)
        status_code = await self._get_status(employee_id)
        self.assertEqual(status_code, 404)
