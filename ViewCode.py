"""Run this model in Python

> pip install azure-ai-inference azure.identity
"""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage, ToolMessage
from azure.ai.inference.models import ImageContentItem, ImageUrl, TextContentItem
from azure.identity import InteractiveBrowserCredential #DefaultAzureCredential
# from azure.identity import AzureCliCredential


Tenant_id="d5e769b0-fd19-45e4-a4a8-b73545450234"

credential = InteractiveBrowserCredential(
    tenant_id=Tenant_id
)

client = ChatCompletionsClient(
    endpoint = "https://real-time-aaf-resource.services.ai.azure.com/models",
    credential=credential,
    credential_scopes=["https://cognitiveservices.azure.com/.default"],
    api_version = "2024-05-01-preview",
)

messages = [
    SystemMessage(content = "You area senior data engineer who have mastered Microsoft fabroc, PySpark, Scala, Python and all the advanced Data Engineering best practices"),
    UserMessage(content = [
        TextContentItem(text = "What happenned in WWII?"),
    ]),
]

tools = []

while True:
    response = client.complete(
        messages = messages,
        model = "Llama-3.3-70B-Instruct",
        tools = tools,
        max_tokens = 2048,
    )

    if response.choices[0].message.tool_calls:
        print(response.choices[0].message.tool_calls)
        messages.append(response.choices[0].message)
        for tool_call in response.choices[0].message.tool_calls:
            messages.append(ToolMessage(
                content=locals()[tool_call.function.name](),
                tool_call_id=tool_call.id,
            ))
    else:
        print(f"[Model Response] {response.choices[0].message.content}")
        break
