import asyncio
import logging
import os

from dotenv import load_dotenv
from livekit.agents import (AutoSubscribe, JobContext, JobProcess,
                            WorkerOptions, cli, llm)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import deepgram
from livekit.plugins import openai as openai_plugin
from livekit.plugins import silero

from db.session import SessionLocal, init_db
from functions.answer_company_question import AnswerCompanyQuestion
from functions.consult import PaloConsultFunction
from functions.get_pptx_context import GetPPTXContext
from utils.pdf import extract_and_store_pdf_content

load_dotenv()

logger = logging.getLogger("multi-function-assistant")
logger.setLevel(logging.INFO)

# Initialize database
init_db()

# Start a new session
session = SessionLocal()

class AssistantFnc(AnswerCompanyQuestion, GetPPTXContext, PaloConsultFunction):
    """Combines individual function contexts into one for the assistant."""


def prewarm_process(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

# Utility function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_knowledge_base():
    """Process the knowledge base."""

    # Path to your PDF file
    pdf_path = "assets/pdf/company/Palo_IT_2024_Public_Holiday.pdf"
    title = "Palo IT 2024 Public Holiday"

    # Start database session
    db = SessionLocal()
    try:
        # Extract and store content
        await extract_and_store_pdf_content(pdf_path, title, db)
        print("PDF content extracted and stored successfully.")

        # Here you can start your server logic
        # e.g., initialize FastAPI or other web frameworks if needed
        logger.info("Server has started and all PDFs have been processed.")
        
        # Simulate a server run loop
        while True:
            pass  # Replace with actual server loop (e.g., FastAPI)

    finally:
        db.close()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Process the knowledge base
    # await process_knowledge_base()

    # # Initialize Deepgram STT with Thai language support
    # stt = deepgram.STT(language="th")

    fnc_ctx = AssistantFnc()  # Create the function context instance
    initial_chat_ctx = llm.ChatContext().append(
        text=(
            "You are a multi-functional assistant created by LiveKit. "
            "You can provide information about the weather, news, and company details based on documents."
        ),
        role="system",
    )
    participant = await ctx.wait_for_participant()
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(language="en"),
        llm=openai_plugin.LLM(model="gpt-4o-mini"),
        tts=openai_plugin.TTS(),
        fnc_ctx=fnc_ctx,
        chat_ctx=initial_chat_ctx,
    )
    agent.start(ctx.room, participant)
    await asyncio.sleep(0.5)  # Add a delay if needed
    await agent.say(
        "Hello! I can answer questions about company information from documents, and consulting. What would you like to know?"
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm_process,
        ),
    )