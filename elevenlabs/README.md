# ElevenLabs Agent Configuration

This folder contains the ElevenLabs configuration artifacts for the
**Unify Product Intelligence** voice AI system.

The system uses an ElevenLabs conversational AI agent with
workflow-based routing to direct product-health questions to specialized
analyst agents and retrieve data through backend APIs.

## Files

   File                                Purpose
  
  `agent.json`                        Exported configuration of the
                                      **Unify Product Intelligence**
                                      ElevenLabs agent, including agent
                                      settings, prompts, RAG/Knowledge
                                      Base references, workflow nodes,
                                      routing conditions, workflow edges,
                                      and tool references.
                                      
  `tools.json`                        Source-controlled definitions of
                                      all **three webhook tools** used
                                      by the agent/workflow.
                                                                            
  `SampleConversationTranscript.txt`  User conversation transcript with
                                      agent. It indicates a smooth transition
                                      between 3 specialized agents, groundness,
                                      reliability.
                                      
`Support_Ticket_Knowledge_Base.txt`  Knowledge base for Support Ticket Analyst
                                     agent. It has summary of support tickets.

`Customer_Feedback_Knowledge_Base.docx`  Knowledge base for Customer Feedback Analyst agent.
                                       It has customer feedbacks in JSON format.

                                      
------------------------------------------------------------------------

## 1. `agent.json`

`agent.json` contains the exported configuration of the **Unify Product
Intelligence** ElevenLabs agent.

The configuration includes:

-   Agent ID and name
-   ASR configuration
-   TTS and voice configuration
-   LLM configuration
-   System prompt
-   RAG configuration
-   Knowledge Base references
-   Tool references
-   Conversation settings
-   Workflow definition
-   Workflow nodes
-   Workflow routing conditions
-   Workflow edges
-   End node
-   Platform settings

### Workflow

The workflow routes questions to specialized analyst agents:

``` text
User
  |
  v
Greeter / Intake Router
  |
  +--> User Feedback Analyst
  |
  +--> Support Ticket Analyst
  |
  +--> Product Metrics Analyst
```

The workflow can also route between analyst nodes when the user's topic
changes during an ongoing conversation.

### Greeter / Intake Router

The Greeter Agent determines which product-health area the user is
asking about:

-   User feedback / NPS
-   Support tickets
-   Product metrics

The Greeter does not answer product-health questions itself. Its primary
responsibility is to understand the user's intent and route the
conversation to the appropriate analyst.

### User Feedback Analyst

Handles questions related to:

-   NPS
-   App reviews
-   User sentiment
-   User interviews
-   Feature requests
-   In-app feedback

The workflow node references the customer-feedback knowledge base.

### Support Ticket Analyst

Handles questions related to:

-   Support ticket volume
-   Ticket categories
-   Priority
-   Resolution times
-   Escalations
-   Churn-risk accounts
-   Support-team capacity

The workflow node references the support-ticket knowledge base and two
support-related webhook tools (`query_support_tickets` and `support_august_summary`).

### Product Metrics Analyst

Handles questions related to:

-   DAU / WAU
-   Engagement
-   Conversion
-   Retention
-   Revenue / MRR
-   Product usage
-   Page-load performance
-   Error rates
-   Competitive win/loss metrics

The workflow node uses the `query_product_metrics` webhook tool.

------------------------------------------------------------------------

## 2. `tools.json`

`tools.json` contains the complete source-controlled definitions of the
three webhook tools used by the Unify Product Intelligence system.

### Tool 1: `query_support_tickets`

**Purpose:** Retrieve support-ticket information for a requested period
and optional filters.

**Backend endpoint:**

``` text
POST /api/v1/support/query
```

Supported request information includes:

-   Start month
-   End month
-   Category
-   Priority
-   Churn risk
-   Account ID

### Tool 2: `support_august_summary`

**Purpose:** Retrieve the predefined support-ticket summary for August
2026.

**Backend endpoint:**

``` text
POST /api/v1/support/august-summary
```

This tool does not require meaningful user-supplied parameters.

Note: `query_support_tickets` tool can satisfy the requirement of this tool. 
This tool `support_august_summary` is intentionally integrated to 
indicate overriding of a generalized tool by a specialized tool.

### Tool 3: `query_product_metrics`

**Purpose:** Retrieve product-health metrics for a specified period.

**Backend endpoint:**

``` text
POST /api/v1/product-metrics/query
```

Supported metrics include:

-   `free_to_paid_conversion_pct`
-   `nps`
-   `monthly_active_users`
-   `mobile_active_users`
-   `retention_30d_pct`
-   `avg_session_minutes`
-   `p95_api_latency_ms`

The tool accepts:

-   `metric`
-   `start_month`
-   `end_month`

as request parameters.

------------------------------------------------------------------------

# Important distinction

**`agent.json` and `tools.json` serve different purposes.**

The ElevenLabs exported `agent.json` does **not necessarily contain the
complete definition of every tool used by every workflow node**.

In this project, the exported agent configuration contains complete
definitions for two tools in its embedded `tools` section:

``` text
query_support_tickets
support_august_summary
```

However, the third tool:

``` text
query_product_metrics
```

is used by the **Product Metrics Analyst** workflow node through its
tool ID:

``` text
tool_6301m0m07y3qfb9v634kkw06x8k8
```

Its complete definition is maintained separately in:

``` text
tools.json
```

Therefore:

> **Do not interpret the `tools` array inside `agent.json` as the
> complete inventory of tools used by the entire workflow.**

The relationship is:

``` text
                    agent.json
                         |
                         v
              Unify Product Intelligence
                         |
                         v
                      Workflow
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Feedback        Support       Product Metrics
      Analyst         Analyst          Analyst
                         |              |
                    +----+----+         |
                    |         |         |
                    v         v         v
                  Tool 1    Tool 2    Tool 3
```

Where:

``` text
Tool 1 = query_support_tickets
Tool 2 = support_august_summary
Tool 3 = query_product_metrics
```

All three complete tool definitions are therefore maintained in
`tools.json`.

This separation provides a clearer source-controlled representation of
the ElevenLabs configuration and avoids treating the embedded `tools`
array in the exported agent configuration as the authoritative list of
every workflow-level tool.

------------------------------------------------------------------------

## Relationship with the FastAPI Backend

The ElevenLabs configuration does not contain the product-health data or
backend business logic.

The overall architecture is:

``` text
User Voice Question
        |
        v
ElevenLabs Conversational Agent
        |
        v
Workflow / Analyst Routing
        |
        +----------------------+
        |                      |
        v                      v
Webhook Tools             Knowledge Bases
        |
        v
FastAPI Backend
        |
        v
Product Health Data
        |
        v
JSON Response
        |
        v
ElevenLabs Agent
        |
        v
Voice Response
```

The FastAPI implementation is maintained separately in this repository.

The webhook tool definitions in `tools.json` provide the API contract
between ElevenLabs and the FastAPI backend.

------------------------------------------------------------------------

## Webhook URLs and Development Environment

The tool configurations were developed using an `ngrok` endpoint for
local development.

The webhook URLs therefore use an endpoint similar to:

``` text
https://<ngrok-domain>/api/...
```

An ngrok URL should be considered a **development/testing endpoint**,
not a permanent production endpoint.

For deployment, update the webhook URLs to point to the deployed FastAPI
service.

------------------------------------------------------------------------

## Project Structure

The relevant project structure is:

``` text
unify-product-intelligence-elevenlabs/
|
+-- elevenlabs/
|   |
|   +-- agent.json
|   +-- tools.json
|   +-- README.md
|
+-- fastapi/
|   +-- ...
|
+-- README.md
```

### ElevenLabs layer

The `elevenlabs/` folder contains:

-   `agent.json`
-   `tools.json`
-   This README

Responsibilities:

-   Voice interaction
-   Conversational AI
-   Workflow orchestration
-   Analyst routing
-   Tool selection
-   Knowledge Base integration

### FastAPI layer

The FastAPI implementation is maintained separately in the repository.

Responsibilities:

-   REST API endpoints
-   Backend business logic
-   Product-health data retrieval
-   SQLite/data-source integration
-   JSON responses to ElevenLabs webhook tools

------------------------------------------------------------------------

## Configuration Dependencies

The ElevenLabs configuration references resources that exist in the
ElevenLabs environment, including:

-   ElevenLabs agent configuration
-   ElevenLabs workflow configuration
-   Knowledge Bases
-   Standalone webhook tools
-   Tool IDs
-   Knowledge Base IDs

The JSON files therefore represent the project's **source-controlled
configuration**, but they should not be considered a fully
self-contained export of every external ElevenLabs resource.

When moving the configuration to another ElevenLabs workspace or
environment, the referenced resources may need to be recreated or
remapped.

------------------------------------------------------------------------

## Summary

The **Unify Product Intelligence** system demonstrates a multi-agent
voice AI architecture in which ElevenLabs provides the conversational
and workflow layer while the FastAPI backend provides the data-access
layer.

``` text
                    +----------------------+
                    |         User         |
                    |    Voice Question    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      ElevenLabs      |
                    | Unify Product        |
                    | Intelligence Agent   |
                    +----------+-----------+
                               |
                               v
                  +--------------------------+
                  |         Workflow         |
                  |Intake / Routing / Greeter|
                  +------------+-------------+
                               |
             +-----------------+-----------------+
             |                 |                 |
             v                 v                 v
        User Feedback     Support Ticket    Product Metrics
           Analyst           Analyst           Analyst
             |                 |                 |
             |            +----+----+            |
             |            |         |            |
             |            v         v            v
             |          Tool 1    Tool 2        Tool 3
             |                 \    /
             |                  \  /
             +-------------------+-------------------+
                                 |
                                 v
                         +---------------+
                         |    FastAPI    |
                         |    Backend    |
                         +-------+-------+
                                 |
                                 v
                         Product Health Data
```

This separation keeps **conversation orchestration, tool definitions,
backend APIs, and product-health data** independently maintainable while
allowing them to operate together as a single voice-based product
intelligence system.
