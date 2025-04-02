from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue, RabbitRouter

from profiles.application.operations.write.create_profile import CreateProfile
from profiles.application.operations.write.delete_profile import DeleteProfile
from profiles.presentation.stream.request_models import UserCreated, UserDeleted

PROFILE_ROUTER = RabbitRouter()


@PROFILE_ROUTER.subscriber(
    RabbitQueue(
        name="user_delete_profile",
        routing_key="UserDeleted",
        auto_delete=False,
        durable=True,
    ),
    RabbitExchange(
        name="auth_exchange", type=ExchangeType.DIRECT, durable=True, auto_delete=False
    ),
    retry=True,
)
@inject
async def delete_user_comments(msg: UserDeleted, *, sender: FromDishka[Sender]) -> None:
    await sender.send(DeleteProfile(user_id=msg.user_id))


@PROFILE_ROUTER.subscriber(
    RabbitQueue(
        name="user_create_profile",
        routing_key="UserCreated",
        auto_delete=False,
        durable=True,
    ),
    RabbitExchange(
        name="auth_exchange", type=ExchangeType.DIRECT, durable=True, auto_delete=False
    ),
    retry=True,
)
@inject
async def create_user_profile(msg: UserCreated, *, sender: FromDishka[Sender]) -> None:
    await sender.send(CreateProfile(user_id=msg.user_id))
