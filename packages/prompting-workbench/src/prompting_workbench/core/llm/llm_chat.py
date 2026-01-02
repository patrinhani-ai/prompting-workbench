from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel


class LLMChatModelParams(BaseModel):
    llm_provider: str = "openai"
    llm_model: str = "gpt-4.1-mini"
    temperature: float = 0.7


class LLMRunConfig(BaseModel):
    run_name: str = "default_run"


def llm_chat_invoke(
    system_msg_text: str,
    human_msg_text: str,
    model_params: LLMChatModelParams = LLMChatModelParams(),
    run_config: LLMRunConfig = LLMRunConfig(),
) -> Any:
    system_msg = SystemMessage(system_msg_text)
    human_msg = HumanMessage(human_msg_text)

    prompt_template = ChatPromptTemplate(
        messages=[
            system_msg,
            human_msg,
        ]
    )

    llm_provider = model_params.llm_provider
    llm_model_name = model_params.llm_model
    temperature = model_params.temperature

    llm_model = init_chat_model(
        model_provider=str(llm_provider) if llm_provider is not None else None,
        model=str(llm_model_name) if llm_model_name is not None else None,
        temperature=float(temperature) if temperature is not None else None,
    )

    llm_chain = prompt_template | llm_model

    run_cfg__run_name = run_config.run_name

    llm_result = llm_chain.invoke(
        input={},
        config=RunnableConfig(
            run_name=run_cfg__run_name,
        ),
    )

    return llm_result
