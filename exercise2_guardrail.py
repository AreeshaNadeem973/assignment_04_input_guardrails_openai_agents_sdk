import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, trace, InputGuardrailTripwireTriggered
import rich
from pydantic import BaseModel, Field

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=False)

# Async client
client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# ---------------- BaseModel ----------------
class OutdoorActivity(BaseModel):
    message: str = Field(description="Father's response")
    isTooCold: bool = Field(description="True if temp < 26°C")

# ---------------- Father Agent ----------------
father_agent = Agent(
    name="father_agent",
    instructions="You are a father agent. Stop your child from running if the temperature is below 26°C, otherwise allow your child politely.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    output_type=OutdoorActivity
)

# ---------------- Guardrail ----------------
@input_guardrail
async def father_guardrail(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    guardrail_result = await Runner.run(father_agent, input, context=ctx)
    return GuardrailFunctionOutput(
        output_info=guardrail_result.final_output.message,
        tripwire_triggered=guardrail_result.final_output.isTooCold
    )

# ---------------- Child Agent ----------------
child_agent = Agent(
    name="child_agent",
    instructions="Child wants to run outside.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    input_guardrails=[father_guardrail]
)

# ---------------- Main ----------------
async def main():
    with trace('Father Guardrail Agent'):
        try:
            result = await Runner.run(child_agent, "I want to run outside. Temperature is 20C.")
            rich.print("✅ Child went outside.")
            rich.print("Final Output:", result.final_output)
        except InputGuardrailTripwireTriggered as e:
            rich.print("❌ Father stopped the child. It's too cold!")
            rich.print("Final Output:", e)

# Run
if __name__ == "__main__":
    asyncio.run(main())
