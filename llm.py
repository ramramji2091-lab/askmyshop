"""LLM brain built with LangChain (LCEL).
chain = prompt -> Gemini -> text -> silence filter
Answers ONLY business questions. Everything else -> None (total silence)."""
import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda

from database import llm_context

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
HISTORY_LIMIT = 20            # last N saved messages sent as memory

SYSTEM_PROMPT = """You are the customer assistant of the business described in DATA below.

STEP 1 - CLASSIFY the customer's latest message.
BUSINESS = about this business: its products, categories, price, GST, stock/availability,
           offers, orders, how to buy / order / apply / book, delivery, payment, address,
           timings, contact, rules or policies.
           Also short follow-ups such as "and its price?", "is it in stock?", "that one",
           "what about GST?", "how can I buy" whenever an EARLIER message in this chat was about
           a product - even if the customer wrote something unrelated in between.
PERSONAL = everything else: greetings (hi, hello, hey), how are you, chit-chat, jokes, feelings,
           general knowledge, coding, news, questions about the assistant itself.
If a message is short and ambiguous AND the chat earlier discussed a product, choose BUSINESS.

STEP 2 - OUTPUT FORMAT (strict):
First line: exactly the word BUSINESS or PERSONAL.
If PERSONAL: output nothing after that word. Do not answer, do not apologise, do not explain.
If BUSINESS: write the reply to the customer from the second line onwards, following these rules:
  - Use ONLY the DATA. Never invent products, prices, GST, stock or policies.
  - Follow the business rules and policy in the DATA.
  - If the DATA lacks the answer, say politely that you don't have that information.
  - For price questions give price without GST, GST and price with GST (if present in the DATA).
  - For "how to buy / order / apply": use the order, payment, delivery, phone and address
    information in the DATA. If there is no order information, share the shop's phone/address
    from the DATA and ask the customer to contact the shop.
  - Reply in the customer's language (English / Hindi / Hinglish). Keep it short.

{data}"""

# ---- prompt: system rules + live DB data, then chat memory, then the new question
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])


def parse_reply(raw):
    """Only a reply whose first line is BUSINESS is allowed through. Anything else -> None."""
    lines = raw.strip().splitlines()
    if not lines:
        return None
    label = lines[0].strip().strip("*`#: ").upper()
    if not label.startswith("BUSINESS"):
        return None                                   # PERSONAL, IGNORE, or unexpected -> silent
    return "\n".join(lines[1:]).strip() or None


def build_chain(llm):
    """prompt | llm | StrOutputParser | silence filter"""
    return prompt | llm | StrOutputParser() | RunnableLambda(parse_reply)


_chain = None


def _get_chain():
    global _chain
    if _chain is None:
        from langchain_google_genai import ChatGoogleGenerativeAI
        _chain = build_chain(ChatGoogleGenerativeAI(model=MODEL, temperature=0))
    return _chain


def to_messages(history):
    """[{"role","content"}] -> LangChain messages (skips empty ones)."""
    return [(HumanMessage if m["role"] == "user" else AIMessage)(content=m["content"])
            for m in (history or [])[-HISTORY_LIMIT:] if m.get("content")]


def chatWithLLM(query, history=None):
    """Returns reply text, or None -> the app must show nothing."""
    if not os.getenv("GOOGLE_API_KEY"):
        return "Setup error: GOOGLE_API_KEY is missing in .env"
    try:
        return _get_chain().invoke({
            "data": llm_context(),            # fresh business + products from MySQL every message
            "history": to_messages(history),
            "question": query,
        })
    except Exception as e:
        return f"Sorry, something went wrong: {e}"