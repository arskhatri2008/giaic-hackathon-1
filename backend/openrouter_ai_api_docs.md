# OpenRouter API Documentation

OpenRouter provides a unified API to access hundreds of AI models through a single endpoint. The platform normalizes requests and responses across different model providers, automatically handles fallbacks when providers are unavailable, and optimizes routing for cost and performance. OpenRouter uses a credit-based billing system where you pay the same price as going directly to providers, plus a small platform fee only when purchasing credits.

The API is fully compatible with the OpenAI SDK and supports all major features including streaming, tool calling, multimodal inputs, and advanced provider routing. With OpenRouter, you can switch between models like GPT-4, Claude, Gemini, Llama, and hundreds of others without changing your code. The platform provides automatic load balancing, intelligent fallbacks for high availability, and transparent pricing across all providers.

## Chat Completion

Send a chat completion request to any available model using the OpenAI-compatible format.

```python
import requests
import json

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "HTTP-Referer": "https://yourapp.com",  # Optional, for rankings
    "X-Title": "Your App Name",  # Optional, for rankings
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-4o",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()

    print("Model used:", result["model"])
    print("Response:", result["choices"][0]["message"]["content"])
    print("Tokens used:", result["usage"]["total_tokens"])
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if hasattr(e.response, 'json'):
        print(f"Details: {e.response.json()}")
```

## Streaming Responses

Enable real-time streaming for any model by setting the stream parameter to true.

```typescript
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "anthropic/claude-3.5-sonnet",
    messages: [{ role: "user", content: "Write a short story about a robot." }],
    stream: true,
  }),
});

if (!response.ok) {
  const error = await response.json();
  throw new Error(`API error: ${error.error.message}`);
}

const reader = response.body?.getReader();
if (!reader) throw new Error("No response body");

const decoder = new TextDecoder();
let buffer = "";

try {
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    while (true) {
      const lineEnd = buffer.indexOf("\n");
      if (lineEnd === -1) break;

      const line = buffer.slice(0, lineEnd).trim();
      buffer = buffer.slice(lineEnd + 1);

      if (line.startsWith("data: ")) {
        const data = line.slice(6);
        if (data === "[DONE]") break;

        try {
          const parsed = JSON.parse(data);

          // Handle mid-stream errors
          if (parsed.error) {
            console.error(`Stream error: ${parsed.error.message}`);
            break;
          }

          const content = parsed.choices[0].delta.content;
          if (content) {
            process.stdout.write(content);
          }
        } catch (e) {
          // Ignore parsing errors for comments
        }
      }
    }
  }
} finally {
  reader.cancel();
}
```

## List Available Models

Retrieve all available models with pricing, capabilities, and provider information.

```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

```python
import requests

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

models = response.json()["data"]

# Filter by capabilities
vision_models = [
    m for m in models
    if "image" in m["architecture"]["input_modalities"]
]

# Filter by price (under $1 per million tokens)
affordable_models = [
    m for m in models
    if float(m["pricing"]["prompt"]) < 0.000001
]

# Find models supporting tool calling
tool_models = [
    m for m in models
    if "tools" in m.get("supported_parameters", [])
]

print(f"Vision models: {len(vision_models)}")
print(f"Affordable models (<$1/M): {len(affordable_models)}")
print(f"Tool calling models: {len(tool_models)}")

# Print details for a specific model
gpt4 = next(m for m in models if m["id"] == "openai/gpt-4o")
print(f"\nModel: {gpt4['name']}")
print(f"Context: {gpt4['context_length']} tokens")
print(f"Price: ${float(gpt4['pricing']['prompt']) * 1000000:.2f}/M prompt tokens")
```

## Get Account Credits

Check your current credit balance and usage.

```javascript
const url = "https://openrouter.ai/api/v1/credits";
const options = {
  method: "GET",
  headers: { Authorization: "Bearer YOUR_API_KEY" },
};

try {
  const response = await fetch(url, options);
  const data = await response.json();

  const totalCredits = data.data.total_credits;
  const totalUsage = data.data.total_usage;
  const remaining = totalCredits - totalUsage;

  console.log(`Total credits: $${totalCredits.toFixed(2)}`);
  console.log(`Used: $${totalUsage.toFixed(2)}`);
  console.log(`Remaining: $${remaining.toFixed(2)}`);
} catch (error) {
  console.error("Error fetching credits:", error);
}
```

## Provider Routing

Control which providers handle your requests with custom routing preferences.

```python
import requests
import json

# Route to fastest providers
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "meta-llama/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": "Hello"}],
        "provider": {
            "sort": "throughput",  # or "price" or "latency"
            "allow_fallbacks": True,
            "data_collection": "deny"  # Only use providers that don't store data
        }
    }
)

# Route to specific providers in order
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [{"role": "user", "content": "Hello"}],
        "provider": {
            "order": ["anthropic", "aws-bedrock"],
            "allow_fallbacks": False,  # Only use specified providers
            "require_parameters": True  # Only use providers supporting all params
        }
    }
)

# Filter by quantization and max price
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": "Hello"}],
        "provider": {
            "quantizations": ["fp16", "bf16"],  # Only full precision
            "max_price": {
                "prompt": 0.0000005,  # Max $0.50 per million tokens
                "completion": 0.000001
            }
        }
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

## Tool Calling

Enable models to request external tool execution with standardized function calling.

```python
import json
import requests
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_API_KEY"
)

# Define a tool
def get_weather(location: str, unit: str = "celsius") -> dict:
    # In production, call a real weather API
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "conditions": "sunny"
    }

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
}]

messages = [
    {"role": "user", "content": "What's the weather in Paris?"}
]

# Initial request with tools
response = client.chat.completions.create(
    model="google/gemini-2.0-flash-001",
    messages=messages,
    tools=tools
)

response_message = response.choices[0].message
messages.append(response_message)

# Process tool calls
if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Execute the tool
        if function_name == "get_weather":
            tool_result = get_weather(**function_args)

        # Add tool result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

    # Get final response
    final_response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001",
        messages=messages,
        tools=tools
    )

    print(final_response.choices[0].message.content)
```

## Multimodal Input

Send images alongside text for vision-capable models.

```typescript
import OpenAI from "openai";
import fs from "fs";

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});

async function analyzeImage() {
  // Option 1: Using image URL
  const urlResponse = await openai.chat.completions.create({
    model: "google/gemini-2.0-flash-001",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "What is in this image?" },
          {
            type: "image_url",
            image_url: {
              url: "https://example.com/image.jpg",
              detail: "high", // or 'low' or 'auto'
            },
          },
        ],
      },
    ],
  });

  console.log("URL Analysis:", urlResponse.choices[0].message.content);

  // Option 2: Using base64 encoded image
  const imageBuffer = fs.readFileSync("./image.jpg");
  const base64Image = imageBuffer.toString("base64");
  const mimeType = "image/jpeg";

  const base64Response = await openai.chat.completions.create({
    model: "anthropic/claude-3.5-sonnet",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Describe this image in detail." },
          {
            type: "image_url",
            image_url: {
              url: `data:${mimeType};base64,${base64Image}`,
            },
          },
        ],
      },
    ],
  });

  console.log("Base64 Analysis:", base64Response.choices[0].message.content);
}

analyzeImage().catch(console.error);
```

## User Tracking

Track individual users for improved caching and detailed analytics.

```python
import requests
import json

def make_request_for_user(user_id: str, message: str):
    """Make a request with user tracking enabled"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o",
            "messages": [{"role": "user", "content": message}],
            "user": user_id  # Stable identifier for your end-user
        }
    )
    return response.json()

# Use consistent user IDs across requests
user_sessions = {
    "alice": "user_12345",
    "bob": "user_67890"
}

# Alice's request (will be cached to same provider)
alice_response = make_request_for_user(
    user_sessions["alice"],
    "What is machine learning?"
)

# Another request from Alice (benefits from sticky caching)
alice_response2 = make_request_for_user(
    user_sessions["alice"],
    "Can you explain neural networks?"
)

# Bob's request (can be load balanced to different provider)
bob_response = make_request_for_user(
    user_sessions["bob"],
    "What is quantum computing?"
)

print(f"Alice: {alice_response['choices'][0]['message']['content']}")
print(f"Bob: {bob_response['choices'][0]['message']['content']}")
```

## Error Handling

Handle API errors gracefully with proper status code checking and retry logic.

```python
import requests
import time
import json
from typing import Optional

def make_request_with_retry(
    messages: list,
    model: str = "openai/gpt-4o",
    max_retries: int = 3
) -> Optional[dict]:
    """
    Make API request with exponential backoff retry logic
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                headers=headers,
                json={"model": model, "messages": messages},
                timeout=30
            )

            # Handle HTTP errors
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error = response.json()
                print(f"Bad request: {error['error']['message']}")
                return None  # Don't retry bad requests
            elif response.status_code == 401:
                print("Invalid API key")
                return None  # Don't retry auth errors
            elif response.status_code == 402:
                print("Insufficient credits")
                return None  # Don't retry payment errors
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 2 ** attempt))
                print(f"Rate limited. Retrying after {retry_after}s...")
                time.sleep(retry_after)
            elif response.status_code >= 500:
                wait_time = 2 ** attempt
                print(f"Server error. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Unexpected error: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print(f"Request timeout (attempt {attempt + 1}/{max_retries})")
            time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(2 ** attempt)

    print("Max retries reached")
    return None

# Usage
result = make_request_with_retry(
    messages=[{"role": "user", "content": "Hello!"}],
    model="openai/gpt-4o"
)

if result:
    print("Success:", result["choices"][0]["message"]["content"])
else:
    print("Request failed after retries")
```

## Generation Tracking

Query generation statistics including native token counts and actual costs.

```javascript
const fetch = require("node-fetch");

async function trackGeneration() {
  // Make a completion request
  const completionResponse = await fetch(
    "https://openrouter.ai/api/v1/chat/completions",
    {
      method: "POST",
      headers: {
        Authorization: "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "openai/gpt-4o",
        messages: [
          { role: "user", content: "Write a haiku about programming." },
        ],
      }),
    }
  );

  const completion = await completionResponse.json();
  const generationId = completion.id;

  console.log("Generation ID:", generationId);
  console.log("Response:", completion.choices[0].message.content);

  // Wait a moment for generation to be processed
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Query generation details for precise cost information
  const statsResponse = await fetch(
    `https://openrouter.ai/api/v1/generation?id=${generationId}`,
    {
      headers: {
        Authorization: "Bearer YOUR_API_KEY",
      },
    }
  );

  const stats = await statsResponse.json();

  console.log("\nGeneration Statistics:");
  console.log("Native prompt tokens:", stats.data.native_tokens_prompt);
  console.log("Native completion tokens:", stats.data.native_tokens_completion);
  console.log("Total cost: $", stats.data.total_cost);
  console.log("Provider used:", stats.data.provider_name);
  console.log("Latency:", stats.data.latency, "ms");
}

trackGeneration().catch(console.error);
```

## Summary

OpenRouter simplifies AI model integration by providing a single, unified API that works with hundreds of models from dozens of providers. The platform handles the complexity of provider-specific APIs, rate limits, and authentication while giving you full control over routing, cost optimization, and performance tuning. Key use cases include building applications that need access to multiple models, implementing fallback strategies for high availability, optimizing costs by routing to the cheapest available provider, and comparing model outputs across different providers.

The API supports advanced features like streaming responses for real-time interaction, tool calling for agentic workflows, multimodal inputs for vision models, and fine-grained provider routing controls. With transparent pricing, detailed usage analytics, and automatic retry mechanisms, OpenRouter provides a production-ready foundation for AI applications. Integration is straightforward using the OpenAI SDK or any HTTP client, and you can switch between models by simply changing the model parameter without modifying your application code.