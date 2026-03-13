from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import InteractiveBrowserCredential

from config import FOUNDRY_ENDPOINT, MODEL_NAME, TENANT_ID
from load_blob import load_latest_pq


df = load_latest_pq()

data_sample = df.head(50).to_string()


credential = InteractiveBrowserCredential(
    tenant_id=TENANT_ID
)

client = ChatCompletionsClient(
    endpoint=FOUNDRY_ENDPOINT,
    credential=credential,
)

messages = [
    SystemMessage(content="""
You are a Formula 1 race analytics assistant.
You analyze race statistics, drivers, and lap data.
"""),

    UserMessage(content=f"""
Here is the latest race data:

{data_sample}

Question:
Which driver had the fastest lap?
""")
]


response = client.complete(
    messages=messages,
    model=MODEL_NAME,
    max_tokens=1000
)

print(response.choices[0].message.content)