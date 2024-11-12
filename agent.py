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

from db.session import SessionLocal
from functions.answer_company_question import AnswerCompanyQuestion
from functions.consult import PaloConsultFunction
from functions.get_pptx_context import GetPPTXContext
from models.document import Document
from utils.pdf import extract_and_store_pdf_content

load_dotenv()

logger = logging.getLogger("multi-function-assistant")
logger.setLevel(logging.INFO)

# Initialize database
# init_db()

# Start a new session
session = SessionLocal()

# Directory containing PDF files to process
PDF_DIRECTORY = "assets/pdf/company"

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

async def process_pdf_files_on_startup():
    """Process all unprocessed PDF files in the PDF_DIRECTORY."""
    print("Processing PDF files on startup...")

    for filename in os.listdir(PDF_DIRECTORY):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIRECTORY, filename)

            # Check if this PDF has already been processed
            document = session.query(Document).filter_by(file_path=pdf_path).first()
            if document:
                logger.info(f"PDF '{filename}' already processed, skipping.")
                continue

            # Process and store the PDF content
            try:
                logger.info(f"Processing PDF '{filename}'...")
                await extract_and_store_pdf_content(pdf_path, title=filename, db=session)
                logger.info(f"Successfully processed and stored '{filename}'.")
            except Exception as e:
                logger.error(f"Failed to process '{filename}': {e}")

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # # Initialize Deepgram STT with Thai language support
    # stt = deepgram.STT(language="th")

    await process_pdf_files_on_startup()

    fnc_ctx = AssistantFnc()  # Create the function context instance
    initial_chat_ctx = llm.ChatContext().append(
        text=(
            "You are a multi-functional assistant created by LiveKit. "
            "You can provide information about the company information based on documents, and consulting about IT solutions."
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
        "Hello! I can answer questions about company information from documents, and consulting about IT solutions. What would you like to know?"
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm_process,
        ),
    )