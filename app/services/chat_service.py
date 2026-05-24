from typing import Literal

from ..interfaces import BaseLLM
from ..schemas.chat import BaseInformation, ChatResponse, EnhancedTextList
from .billing_service import BillingService
from uuid import UUID


class ChatService:
    def __init__(self, llm: BaseLLM, billing: BillingService):
        self.llm = llm
        self.billing = billing
        self.monologue_system = """You are a professional product marketing copywriter.

Your task:
- Generate a spoken marketing monologue.
- This is a direct-to-camera speech.
- Focus on benefits and user outcomes.
- Match the platform, audience, and goal exactly.

Rules:
- Use the requested language only.
- Keep it within user defined word length.
- Do NOT include scene descriptions, brackets, directions or plot.
- Do NOT include speaker names or labels.
- Do NOT include explanations, introductions, or meta text.
- Avoid all forbidden words or ideas.
- Output plain text only.
- End with a clear call to action.
            """

        self.dialogue_system = """You are a professional product marketing copywriter.

                Generate a marketing dialogue.

                Rules:
                - Use exactly two speakers: 1 and 2.
                - Alternate turns.
                - Use the requested language only.
                - Keep each line concise.
                - Speaker A must deliver the final call to action.
                - Focus on product benefits and user pain points.
                - Avoid all forbidden words or ideas.
                - Use the requested language only.
                - Do not add narration, explanations, turn number or any extra text in the `text field`.

                Output only structured dialogue.
                """

    async def make_script(
        self,
        wallet_id: UUID,
        product_title: str,
        product: str,
        goal: str,
        audience: str,
        platform: str,
        tone: str,
        language: str,
        duration: str,
        forbid: str = "",
        format: Literal["monologue", "dialogue"] = "monologue",
    ) -> ChatResponse:
        await self.billing.transact(wallet_id=wallet_id, product_title=product_title)

        if format == "monologue":
            text = (
                f"Product: {product}\n"
                f"Goal: {goal}\n"
                f"Audience: {audience}\n"
                f"Platform: {platform}\n"
                f"Tone: {tone}\n"
                f"Language: {language}\n"
                f"Duration: {duration}\n"
                f"Forbidden: {forbid}\n"
                f"Format: monologue"
            )

            response = await self.llm.ask(text=text, instruction=self.monologue_system)
            base_format = BaseInformation(gender="female", text=response, person_id=1)
            return ChatResponse(dialogue=[base_format])
        else:
            text = (
                f"Product: {product}\n"
                f"Goal: {goal}\n"
                f"Audience: {audience}\n"
                f"Platform: {platform}\n"
                f"Tone: {tone}\n"
                f"Language: {language}\n"
                f"Duration: {duration}\n"
                f"Forbidden: {forbid}\n"
                f"Format: dialogue"
            )

            return await self.llm.formatted_ask(
                text=text, output_format=ChatResponse, instruction=self.dialogue_system
            )

    async def enhance_script_text(
        self,
        segments: list[str],
        language_id: str,
    ) -> EnhancedTextList:
        system_instruction = f"""You are a professional native-level marketing copywriter. 
    Rewrite the following list of marketing lines to be more effective.
    
    Goal: Make it more punchy and professional
    
    CRITICAL RULES:
    1. STRICT LANGUAGE:Response must be in `{language_id=}` language. 
    2. SAME QUANTITY: Return exactly {len(segments)} lines in list.
    """

        formatted_list = "\n".join(f"{i + 1}. {txt}" for i, txt in enumerate(segments))

        response: EnhancedTextList = await self.llm.formatted_ask(
            text=formatted_list,
            output_format=EnhancedTextList,
            instruction=system_instruction,
        )
        return response

    async def enhance_realistic_image_prompt(self, prompt: str) -> str:
        system_prompt = """
You are good professional prompt enhancer. Your job is to enhance the user prompt. Which is 
intended to feed in a flux based USO model. 
So the enhanced prompt need to be
1. Comply with the information the user wants.
2. Translated so flux1 based models understands better. Like replacing those terms flux does not understand to those what flux understands.
3. The generated image should high quality, most realistic.

And finally, you should only return the plain modified prompt, no suggestion or anything else. I will directly feed the prompt.
"""

        return await self.llm.ask(text=prompt, instruction=system_prompt)
