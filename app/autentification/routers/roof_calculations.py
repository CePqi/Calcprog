from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.schemas import FormRoofFirst

template = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/calcul", tags=["roof"])

@router.post("/load_on_the_roof")
async def get_load_on_the_roof(request: Request, data: FormRoofFirst, session: AsyncSession = Depends(db_helper.get_async_session)):
    form = data.model_dump()

    q_s = int(form.get("q_s"))
    g_k = int(form.get("g_k"))
    g_u = int(form.get("g_u"))
    q_w = int(form.get("q_w"))
    l = int(form.get("L"))
    e = int(form.get("E")) * 1_000_000
    b = int(form.get("b"))
    h = int(form.get("h"))
    q_dop = int(form.get("q_dop"))

    i = round((b / 1000) * (h / 1000)**3 / 12, 7)

    q = (q_s + g_k + g_u + q_w) * 10


    f = (5 * q * l**4) / (384 * e * i)
    f_mm = round(f * 1000, 2)

    f_dop_mm = (l / 200) * 1000

    b_m = b / 1000
    h_m = h / 1000

    calc = 4 * b_m * h_m**2

    if not calc:
        return {"message":"Вы отправили некоректные данные, в одном из подсчетов получилось деление на ноль"}

    ku = round((3 * q * l ** 2) / calc / 1_000_000, 2)

    return {
        "message": f"σ = {ku} МПа (Допустимо до {q_dop} МПа), "
                   f"f = {f_mm} мм (Допустимо до {round(f_dop_mm, 2)})"
    }

@router.get("/get_roof_form_first")
async def get_roof_form(request: Request):
    return template.TemplateResponse("own_page.html", context={"request": request})