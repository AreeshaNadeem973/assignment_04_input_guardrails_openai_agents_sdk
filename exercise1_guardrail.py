import asyncio, os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, trace
import rich
from pydantic import BaseModel, Field

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Enable tracing
set_tracing_disabled(disabled=False)

# Gemini client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Guardrail output model
class TimeQueryCheck(BaseModel):
   reasoning: str = Field(description="Reason why the query is considered about class timings or not.")
   is_time_query: bool = Field(description="True if user is asking about changing class timings, else False.")


# Teacher agent → detect timing query
teacher_agent = Agent(
    name="teacher_agent",
    instructions="Check if query is about class timings.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    output_type=TimeQueryCheck
)

# Guardrail function
@input_guardrail
async def class_timings_guardrail(ctx:RunContextWrapper, agent:Agent, input:str|list[TResponseInputItem]) -> GuardrailFunctionOutput:
    res = await Runner.run(teacher_agent, input, context=ctx)
    return GuardrailFunctionOutput(
        output_info=res.final_output.reasoning,
        tripwire_triggered=res.final_output.is_time_query
    )

# Student agent with guardrail
student_agent = Agent(
    name="student_agent",
    instructions="Help with class issues.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    input_guardrails=[class_timings_guardrail]
)

# Run main
async def main():
   with trace("ClassTimings Guardrail Trace"):
       result = await Runner.run(student_agent, input="I want to change my class timings 😭😭")
       rich.print(result.final_output)

if __name__ == "__main__":
   asyncio.run(main())
