from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.autentification.auth.enc_dec_f import encoded_func, decoded_func
from app.core.models import UserDao, db_helper
from app.schemas import RegistertUser, LoginUser, SearchUserById, SearchUserByEmail
from app.autentification.auth.hash_p import hash_password, check_password


template = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/auth", tags=["user"])


@router.get("/register/view")
async def root(request: Request):
    return template.TemplateResponse(name="register.html", context={"request": request})


@router.post("/register")
async def register_user(
    request: Request,
    user_form: RegistertUser,
    session: AsyncSession = Depends(db_helper.get_async_session),
):
    person = await UserDao.find_one_or_none(
        SearchUserByEmail(email=user_form.email), session=session
    )

    if person is None:
        user_dict = user_form.model_dump()
        user_dict["password"] = hash_password(user_dict["password"])
        await UserDao.add(user_dict, session=session)
    return {"message": "Вы зарегестрировались"}


@router.get("/login/view")
async def login_page(request: Request):
    return template.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_user(response: Response, user_form: LoginUser, session: AsyncSession = Depends(db_helper.get_async_session)):


    user_dict = user_form.model_dump()
    user_data = await UserDao.find_one_or_none(SearchUserByEmail(email=user_dict["email"]), session=session)

    token = encoded_func(data={"user_id": user_data.id})


    flag = check_password(str(user_dict["password"]), user_data.password)
    response.set_cookie("user_cookie_pswrd", value=token)
    if flag:
        return {"message": "Вы вошли"}
    return ''


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="user_cookie_pswrd")
    return {"message": "Куки удалены"}


async def get_user_id(request: Request):
    user_token = request.cookies.get("user_cookie_pswrd", None)

    user_id = decoded_func(user_token)

    if user_id.get("user_id", None) is None:
        return None
    return user_id.get("user_id")

async def get_current_user(user_id: int = Depends(get_user_id), session: AsyncSession = Depends(db_helper.get_async_session)):
    current_user = await UserDao.find_one_or_none(SearchUserById(id=user_id), session=session)
    return current_user

@router.get("/me")
async def get_page_by_my_profile(request: Request, current_user = Depends(get_current_user)):
    return template.TemplateResponse("user_page.html", {"request": request, "user_data": current_user})
