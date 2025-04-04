from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, cast

from dishka.integrations.fastapi import (
    setup_dishka as add_container_to_fastapi,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from profiles.application.common.application_error import ApplicationError
from profiles.bootstrap.config import get_database_config, get_rabbitmq_config
from profiles.bootstrap.container import bootstrap_api_container
from profiles.bootstrap.entrypoints.stream import bootstrap_stream
from profiles.infrastructure.persistence.sql_tables import (
    map_outbox_table,
    map_profile_table,
)
from profiles.presentation.api.exception_handlers import (
    application_error_handler,
)
from profiles.presentation.api.routers.healthcheck import HEALTHCHECK_ROUTER
from profiles.presentation.api.routers.profiles import PROFILE_ROUTER

if TYPE_CHECKING:
    from dishka import AsyncContainer
    from starlette.types import HTTPExceptionHandler


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    map_profile_table()
    map_outbox_table()
    stream = bootstrap_stream()
    dishka_container = cast("AsyncContainer", application.state.dishka_container)
    await stream.start()
    yield
    await stream.stop()
    await dishka_container.close()


def add_middlewares(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


def add_api_routers(application: FastAPI) -> None:
    application.include_router(HEALTHCHECK_ROUTER)
    application.include_router(PROFILE_ROUTER)


def add_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(
        ApplicationError,
        cast("HTTPExceptionHandler", application_error_handler),
    )


def bootstrap_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    dishka_container = bootstrap_api_container(
        get_rabbitmq_config(),
        get_database_config(),
    )

    add_middlewares(application)
    add_api_routers(application)
    add_exception_handlers(application)
    add_container_to_fastapi(dishka_container, application)

    return application
