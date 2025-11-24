from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from scalar_fastapi import get_scalar_api_reference
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def healthy():
    return {"status": "healthy"}


@app.get("/scalar", include_in_schema=False)
def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        scalar_proxy_url="https://proxy.scalar.com",
    )


app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
