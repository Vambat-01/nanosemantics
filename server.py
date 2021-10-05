import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from company_storage import CompanyStorage, Employee, NotFoundException, get_connection
from uvicorn import Config, Server
import typer
from pydantic import BaseModel


# Я не стал создавать отдельный файл для моделей сервера, т.к. пока тут только эта простая модель.
class ResourceId(BaseModel):
    id: int


def main(server_host: str, server_port: int, postgres_host: str, postgres_port: int):
    async def do_main():
        app = FastAPI()
        connection = await get_connection(postgres_host, postgres_port, 'postgres')
        company_storage = CompanyStorage(connection)
        await company_storage.create_table()

        @app.exception_handler(NotFoundException)
        async def on_not_found_exception(request: Request, exception: NotFoundException):
            return JSONResponse(status_code=404, content=exception.message)

        @app.get("/employees/{id}")
        async def get_employee(id: int):
            response = await company_storage.get_employee(id)
            return response

        @app.post("/employees")
        async def post_employee(employee: Employee):
            employee_id = await company_storage.add_employee(employee)
            return ResourceId(id=employee_id)

        @app.put("/employees/{id}")
        async def update_employee(id: int, employee: Employee):
            await company_storage.put_employee(id, employee)

        @app.delete("/employees/{id}")
        async def delete_employee(id: int):
            await company_storage.delete_employee(id)

        config = Config(app=app, host=server_host, port=server_port)
        server = Server(config)
        await server.serve()
        await connection.close()

    asyncio.run(do_main())


if __name__ == "__main__":
    typer.run(main)
