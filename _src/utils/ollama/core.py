# This is a work in progress.
# The testing phase will continue until the config development is complete.

import dataclasses
import typing
from ollama import AsyncClient


@dataclasses.dataclass
class Context:
    system: str | None = None
    user: dict[int, str | None] = dataclasses.field(default_factory=dict)
    assistant: dict[int, str | None] = dataclasses.field(default_factory=dict)
    memory: str | None = None
    search: str | None = None

@dataclasses.dataclass
class Config:
    model: str = "huihui_ai/deepseek-r1-abliterated:8b"
    messages: list[dict[str, str]] = dataclasses.field(default_factory=list)
    tools: list | None = None
    stream: bool = False
    think: str = "high"
    format: str | None = None
    options: dict[str, typing.Any] = dataclasses.field(default_factory=lambda: {
        'num_ctx': 4096,                      # 上下文長度
        'num_batch': 32,
        'use_mmap': True,
        'use_mlock': True,
        'num_thread': 4,
        'num_keep': 512,                      # 保留長度
        'num_predict': 1024,                   # 輸出長度
        'top_k': 80,
        'top_p': 0.85,
        'typical_p': 0.7,
        'repeat_last_n': 24,
        'temperature': 0.95,
        'repeat_penalty': 1.1,
        'presence_penalty': 0.1,
        'penalize_newline': True,
        'stop':["<｜begin▁of▁sentence｜>", "<｜end▁of▁sentence｜>", "<｜System｜>", "<｜Search｜>", "<｜Memory｜>", "<｜User｜>", "<｜Assistant｜>"]
    })
    keep_alive: int = 1048576

@dataclasses.dataclass
class Ai:
    config: Config = dataclasses.field(default_factory=Config)
    context: dict[int, Context] = dataclasses.field(default_factory=dict)
    ollama = AsyncClient()

    async def chat(self, session: int) -> str:
        self.config.messages.clear()
        context = self.context[session]
        if context.system: self.config.messages.append({'role': 'system', 'content': f"<｜System｜> \n{context.system}"})
        if context.search: self.config.messages.append({'role': 'system', 'content': f"<｜Search｜> \n{context.search}"})
        if context.memory: self.config.messages.append({'role': 'system', 'content': f"<｜Memory｜> \n{context.memory}"})
        keys = sorted(set(context.user) | set(context.assistant))
        for i in keys:
            if context.user.get(i): self.config.messages.append({'role': 'user', 'content': f"<｜User｜> \n{context.user[i]}"})
            if context.assistant.get(i): self.config.messages.append({'role': 'assistant', 'content': f"<｜Assistant｜> \n{context.assistant[i]}"})
        try:
            response = await self.ollama.chat(
                model = self.config.model,
                messages = self.config.messages,
                tools = self.config.tools,
                stream = self.config.stream,
                think = self.config.think,
                format = self.config.format,
                options = self.config.options,
                keep_alive = self.config.keep_alive
            )
        except Exception as e:
            raise RuntimeError("Failed to call Ollama") from e
        if not response:
            raise ValueError("No response received from Ollama")
        try:
            response = response.message.content
        except Exception as e:
            raise ValueError("Response does not contain expected content") from e
        if not isinstance(response, str):
            raise TypeError("Response content is not a string")
        response = response.strip()
        if response == "":
            raise ValueError("Response content is empty")
        return response