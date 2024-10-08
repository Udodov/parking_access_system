from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.access_control.access_manager import AccessManager
from src.database.database import get_db
from src.utils.logger import web_logger

# Создаем экземпляр AccessManager
access_manager = AccessManager()


def create_app() -> FastAPI:
    new_app = FastAPI()

    # Настройка Jinja2Templates с указанием директории для шаблонов
    templates = Jinja2Templates(directory="src/web/templates")

    @new_app.get("/check_access/{license_plate}", response_class=HTMLResponse)
    async def check_vehicle_access(
        license_plate: str, request: Request, db: AsyncSession = Depends(get_db)
    ):
        web_logger.info(
            f"Получен запрос на проверку доступа для номера: {license_plate}"
        )

        # Проверяем доступ с помощью метода check_access из AccessManager
        has_access = await access_manager.check_access(license_plate, db)

        # Рендеринг шаблона и передача данных в контекст
        return templates.TemplateResponse(
            "access_result.html",
            {
                "request": request,
                "license_plate": license_plate,
                "access_granted": has_access,
            },
        )

    @new_app.post("/check_access", response_model=dict)
    async def check_access(
        plate_number: str = Form(...), db: AsyncSession = Depends(get_db)
    ):
        web_logger.info(
            f"Получен POST-запрос на проверку доступа для номера: {plate_number}"
        )

        # Проверяем доступ с помощью метода check_access из AccessManager
        result = await access_manager.check_access(plate_number, db)

        return {"access_granted": result}

    return new_app


app = create_app()
