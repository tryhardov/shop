from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
print("CORS ORIGINS:", settings.cors_origins)
from database import init_db, engine
from app.routes import cart_router, category_router, product_router, user_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()
    
    
app = FastAPI(
    title = settings.app_name,
    lifespan=lifespan,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')


app.include_router(category_router)
app.include_router(cart_router)
app.include_router(product_router)
app.include_router(user_router)