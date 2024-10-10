"""
GeminiChad
Copyright (c) 2024 @notV3NOM

See the README.md file for licensing and disclaimer information.
"""
from collections import defaultdict

from .config import DEFAULT_SYSTEM_MESSAGE
from .llm import new_session
from .tools import web_search, calculate, image_generation, clock

CHAT_SESSION = "CHAT_SESSION"
SYSTEM_MESSAGE = "SYSTEM_MESSAGE"
TOOLS = "TOOLS"

TOOL_OPTIONS = { 
    "Web Search" : web_search, 
    "Calculate": calculate , 
    "Image Generation": image_generation, 
    "Clock": clock
}

default_tools = [TOOL_OPTIONS[tool] for tool in TOOL_OPTIONS]

def session_default_factory():
    return {
        SYSTEM_MESSAGE: DEFAULT_SYSTEM_MESSAGE,
        CHAT_SESSION: new_session(tools=default_tools),
        TOOLS: default_tools
    }

SESSIONS = defaultdict(session_default_factory)