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
class GateKeeperOutput(BaseModel):
    allowed: bool = Field(description="True if the student is from Our School, False if the student is from another school.")
    message: str = Field(description="The gate keeper's response, e.g., 'Welcome' or 'Access denied'")

# ---------------- Father Agent ----------------
gate_keeper_agent = Agent(
    name="gate_keeper_agent",
    instructions="You are a gate keeper. Allow only 'Our School' students to enter. Stop all others.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    output_type=GateKeeperOutput
)

# ---------------- Guardrail ----------------
@input_guardrail
async def gate_keeper_guardrail(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    guardrail_result = await Runner.run(gate_keeper_agent, input, context=ctx)
    return GuardrailFunctionOutput(
        output_info=guardrail_result.final_output.message,
        tripwire_triggered=guardrail_result.final_output.allowed
    )

# ---------------- Child Agent ----------------
student_agent = Agent(
    name="student_agent ",
    instructions="You are a student asking academic questions only.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    input_guardrails=[gate_keeper_guardrail]
)

# ---------------- Main ----------------
# ---------------- Main ----------------
async def main():
    with trace('Gate Keeper Guardrail Agent'):
        try:
            result = await Runner.run(student_agent, "I am a student from Our School")
            rich.print("✅ Student entered the school.")
            rich.print("Final Output:", result.final_output)
        except InputGuardrailTripwireTriggered as e:
            rich.print("❌ Gate Keeper blocked the student!")
            rich.print("Reason:", e)

# Run
if __name__ == "__main__":
    asyncio.run(main())
