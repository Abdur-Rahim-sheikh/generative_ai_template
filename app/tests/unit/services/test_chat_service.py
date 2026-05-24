from unittest.mock import AsyncMock

import pytest

from ....schemas.chat import ChatResponse, EnhancedTextList
from ....services import BillingService, ChatService
from ...dummies import DummyLLM
from ...fakes import FakeUnitOfWork
from .conftest import SeedDbFactory


@pytest.fixture
def llm() -> DummyLLM:
    return DummyLLM()


@pytest.fixture
def chat_service(llm: DummyLLM, billing_service: BillingService) -> ChatService:
    return ChatService(llm=llm, billing=billing_service)


@pytest.mark.parametrize("format", ["monologue", "dialogue"])
async def test_make_script_returns_chat_response(
    chat_service: ChatService, format: str, seeded_db: SeedDbFactory
):
    await seeded_db()

    response = await chat_service.make_script(
        wallet_id="test-wallet-id",
        product_title="test-product-id",
        product="SuperApp",
        goal="increase downloads",
        audience="millennials",
        platform="Instagram",
        tone="energetic",
        language="en",
        duration="short",
        format=format,
    )
    assert isinstance(response, ChatResponse)


async def test_make_script_monologue_has_single_dialogue_entry(
    chat_service: ChatService, seeded_db: SeedDbFactory
):
    await seeded_db()
    response = await chat_service.make_script(
        wallet_id="test-wallet-id",
        product_title="test-product-id",
        product="X",
        goal="Y",
        audience="Z",
        platform="W",
        tone="casual",
        language="en",
        duration="short",
        format="monologue",
    )
    assert len(response.dialogue) == 1


@pytest.mark.parametrize(
    ("format", "used_method"), [("monologue", "ask"), ("dialogue", "formatted_ask")]
)
async def test_make_script_uses_respective_methods(
    chat_service: ChatService,
    llm: DummyLLM,
    format: str,
    used_method: str,
    seeded_db: SeedDbFactory,
):
    await seeded_db()
    await chat_service.make_script(
        wallet_id="test-wallet-id",
        product_title="test-product-id",
        product="X",
        goal="Y",
        audience="Z",
        platform="W",
        tone="casual",
        language="en",
        duration="short",
        format=format,
    )
    assert llm.call_history[0]["method"] == used_method


@pytest.mark.parametrize("format", ["monologue", "dialogue"])
async def test_system_prompt_is_sent(
    chat_service: ChatService, llm: DummyLLM, format: str, seeded_db: SeedDbFactory
):
    await seeded_db()
    await chat_service.make_script(
        wallet_id="test-wallet-id",
        product_title="test-product-id",
        product="X",
        goal="Y",
        audience="Z",
        platform="W",
        tone="casual",
        language="en",
        duration="short",
        format=format,
    )
    call = llm.call_history[0]
    assert len(call["instruction"]) > 0


@pytest.mark.parametrize("format", ["monologue", "dialogue"])
async def test_generated_prompt_contains_all_fields(
    chat_service: ChatService, llm: DummyLLM, format: str, seeded_db: SeedDbFactory
):
    await seeded_db()
    await chat_service.make_script(
        wallet_id="test-wallet-id",
        product_title="test-product-id",
        product="MyCoolProduct",
        goal="Y",
        audience="Z",
        platform="W",
        tone="casual",
        language="en",
        duration="short",
        format=format,
    )
    text = llm.call_history[0]["text"]
    assert all(
        x in text for x in ["MyCoolProduct", "Y", "W", "casual", "en", "short", format]
    )


async def test_enhance_returns_enhanced_text_list(
    chat_service: ChatService, llm: DummyLLM, seeded_db: SeedDbFactory
):
    await seeded_db()
    result = await chat_service.enhance_script_text(
        segments=["Buy now!", "Limited offer."],
        language_id="en",
    )

    assert isinstance(result, EnhancedTextList)
    history = llm.call_history[0]
    assert history["method"] == llm.formatted_ask.__name__


# Below method cannot be tested here, as this depends on pure ai
# and we have dummies here, so this need to be tested in
# integration or end2end or AI specific tests i guess

# async def test_enhance_system_prompt_returns_exact_segment_count(
#     chat_service: ChatService, llm: DummyLLM
# ):
#     segs = ["Line one", "Line two", "Line three"]
#     enhanced_scripts = await chat_service.enhance_script_text(
#         segments=segs, language_id="en"
#     )
#     print(enhanced_scripts.enhanced_texts)

#     assert len(segs) == len(enhanced_scripts.enhanced_texts)


async def test_enhance_prompt_returns_string(
    chat_service: ChatService, seeded_db: SeedDbFactory
):
    await seeded_db()
    result = await chat_service.enhance_realistic_image_prompt("a cat on a table")
    assert isinstance(result, str)


async def test_enhance_prompt_uses_llm_ask(
    chat_service: ChatService, llm: DummyLLM, seeded_db: SeedDbFactory
):
    await seeded_db()
    await chat_service.enhance_realistic_image_prompt("a dog in the park")
    assert llm.call_history[0]["method"] == llm.ask.__name__


async def test_generator_failure_does_not_revert_billing(
    chat_service: ChatService, fake_uow: FakeUnitOfWork, seeded_db: SeedDbFactory
):

    COIN_BALANCE = 50
    FREE_USES_REMAINING = 5
    COIN_COST = 30
    wallet, product = await seeded_db(
        coin_balance=COIN_BALANCE,
        free_uses_remaining=FREE_USES_REMAINING,
        coin_cost=COIN_COST,
    )

    # mocking the generator
    chat_service.llm.ask = AsyncMock(side_effect=Exception("Inappropriate prompt"))
    with pytest.raises(Exception, match="Inappropriate prompt"):
        await chat_service.make_script(
            wallet_id=wallet.id,
            product_title=product.id,
            product="MyCoolProduct",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
    current_wallet = await fake_uow.wallets.get(wallet.id)
    assert current_wallet.coin_balance == COIN_BALANCE - COIN_COST
    assert current_wallet.free_uses_remaining == FREE_USES_REMAINING
