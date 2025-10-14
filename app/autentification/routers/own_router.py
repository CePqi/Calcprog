from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

template = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/own", tags=["root_page"])


@router.get("/page/view")
async def own_page(request: Request):
    return template.TemplateResponse(name="own_page.html", context={"request": request})
