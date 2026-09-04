# Unify Product Intelligence — ElevenLabs + FastAPI

A proof-of-concept **voice-based Product Intelligence system** using ElevenLabs Conversational AI, workflow-based agent routing, Webhook tools, FastAPI APIs, and product-health data.

The project demonstrates how a user can ask product-health questions using natural language and receive answers through a voice conversation.

## Architecture

```text
                         User
                    Voice Question
                           |
                           v
                +----------------------+
                |      ElevenLabs      |
                | Conversational Agent |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |      Workflow        |
                |   Intent / Routing   |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     User Feedback    Support Ticket    Product Metrics
       Analyst          Analyst           Analyst
          |                |                |
          |           +----+----+           |
          |           |         |           |
          |           v         v           v
          |         Tool 1    Tool 2       Tool 3
          |                \    /           |
          +-----------------+--+------------+
                            |
                            v
                    +---------------+
                    |    FastAPI    |
                    |    Backend    |
                    +-------+-------+
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

## Project Overview

The solution is intentionally separated into two primary layers:

- **ElevenLabs** — voice interaction, conversational AI, workflow orchestration, specialist-agent routing, and tool invocation.
- **FastAPI** — backend APIs and access to the product-health data.

The repository contains separate README files for each layer:

- [`elevenlabs/README.md`](./elevenlabs/README.md) — ElevenLabs agent, workflow, and tool configuration.
- [`fastapi/README.md`](./fastapi/README.md) — FastAPI application, APIs, data, setup, and execution.

This README provides the overall architecture, design rationale, and possible future evolution of the solution.

---

## Repository Structure

```text
unify-product-intelligence-elevenlabs/
|
+-- elevenlabs/
|   +-- Customer_Feedback_Knowledge_Base.docx
|   +-- Support_Ticket_Knowledge_Base.txt
|   +-- SampleConversationTranscript.txt
|   +-- agent.json
|   +-- tools.json
|   +-- README.md
|
+-- fastapi/
|   +-- app/
|   +-- data/
|   +-- tests/
|   +-- requirements.txt
|   +-- README.md
|
+-- LICENSE
+-- README.md
```

### ElevenLabs

The `elevenlabs/` folder contains the configuration artifacts for the conversational agent, including the exported agent/workflow configuration, tool definitions, knowledge bases, and sample conversation transcript.

For details, see [`elevenlabs/README.md`](./elevenlabs/README.md).

### FastAPI

The `fastapi/` folder contains the backend implementation, SQLite product-health data, tests, dependencies, and API documentation.

For setup and implementation details, see [`fastapi/README.md`](./fastapi/README.md).

---

# Why FastAPI + Webhooks?

For this proof of concept, **FastAPI was intentionally used directly to explore and demonstrate its integration with ElevenLabs through Webhook tools.**

The objective was to understand the complete integration flow:

```text
ElevenLabs Agent
       |
       | Webhook
       v
    FastAPI
       |
       v
 Product Health Data
```

ElevenLabs Webhook tools are designed to call external APIs and can dynamically supply query, body, and path parameters based on the conversation. This makes a REST API such as FastAPI a straightforward integration point for this POC. 

The current FastAPI implementation exposes defined endpoints for product metrics, support, customer health, feedback, and executive overview. The backend README documents the endpoint list. Only 3 apis are integrated for demonstration. 

The agent is deliberately **not** given arbitrary SQL access. Instead, the voice agent calls controlled API endpoints, and the backend performs the required data access. 

This approach is useful for exploring:

- ElevenLabs Webhook configuration
- LLM-generated tool parameters
- REST API integration
- FastAPI request validation
- Backend business logic
- SQLite/data access
- JSON responses to an AI agent
- Voice responses based on backend data

**FastAPI + Webhook is therefore an intentional implementation choice for this POC.**

It should not be interpreted as the only, or necessarily the final, integration architecture for a production implementation.

---

# MCP as a Possible Integration Layer

The same backend API capabilities can also be made available through an **MCP (Model Context Protocol)** layer.

A possible future architecture is:

### Possible MCP Architecture

```text
ElevenLabs
     |
     | MCP
     v
  MCP Server
     |
     v
 FastAPI / Services
     |
     v
 Product Data
```

---

# Multi-Agent Product Intelligence Workflow

The ElevenLabs configuration uses workflow-based specialist agents for different product-health domains. The repository's ElevenLabs configuration documents the agent/workflow and tool relationships. 

Typical responsibilities include:

### User Feedback Analyst

Handles questions related to customer feedback and sentiment, such as:

- NPS
- App reviews
- User sentiment
- Feature requests
- Customer feedback

### Support Ticket Analyst

Handles questions related to support operations, such as:

- Support ticket volume
- Ticket categories
- Priority
- Resolution information
- Support trends
- Churn-risk information

### Product Metrics Analyst

Handles product-health questions such as:

- Conversion
- Activation
- Retention
- Monthly active users
- Mobile usage
- Session duration
- API latency
- Other product performance metrics

The workflow determines the appropriate specialist based on the user's question and invokes the required tool or knowledge source.

---

# Backend Integration

The FastAPI backend acts as the controlled interface between the ElevenLabs agent and the product-health data.

The intended flow is:

```text
Natural-language question
        |
        v
ElevenLabs Workflow
        |
        v
Specialist Agent
        |
        v
Webhook Tool
        |
        v
FastAPI Endpoint
        |
        v
Validated Backend Query
        |
        v
Product Health Data
        |
        v
JSON Response
        |
        v
ElevenLabs
        |
        v
Voice Answer
```

The backend README documents the current API endpoints and explicitly recommends not exposing arbitrary SQL to the voice agent. 

---

# Development Environment

For local development, the FastAPI application can be exposed to ElevenLabs using an HTTPS tunnel such as ngrok.

The repository's FastAPI documentation uses the following development pattern: `ngrok http 8000`, followed by configuring the resulting HTTPS forwarding URL in the ElevenLabs tool/webhook. 

```text
ElevenLabs Cloud
       |
       | HTTPS Webhook
       v
     ngrok
       |
       v
localhost:8000
       |
       v
    FastAPI
```

The tunnel is intended for development/testing. For production, the FastAPI backend should be deployed behind a stable HTTPS endpoint with appropriate authentication, authorization, monitoring, and security controls.

---

# Security Considerations

This repository is a proof of concept and should not automatically be considered production-ready.

Before production deployment, consider:

- Authentication between ElevenLabs and backend APIs
- HTTPS
- Request validation
- Rate limiting
- API authorization
- Secret management
- Request IDs and audit logging
- CORS restrictions where applicable
- Query timeouts
- Monitoring and alerting
- Database access controls
- Production database selection
- Tool-level permissions
- MCP server security if MCP is introduced

The existing FastAPI README also recommends authentication, HTTPS, rate limiting, request IDs, audit logging, CORS restrictions, query timeouts, and moving from SQLite to PostgreSQL for larger concurrent workloads. 

---

# Future Evolution

Possible future enhancements include:

1. **MCP integration**
   - Add an MCP server in front of selected backend capabilities.
   - Expose product-health APIs as MCP tools.
   - Connect the MCP server to the ElevenLabs agent.

2. **Production API deployment**
   - Deploy FastAPI to a stable cloud endpoint.
   - Add authentication and authorization.

3. **Production data layer**
   - Evaluate PostgreSQL or another production database for higher concurrency and scalability.

4. **Observability**
   - Add structured logging.
   - Add request tracing.
   - Monitor tool execution and agent performance.

5. **Additional AI capabilities**
   - More product-health tools.
   - Advanced RAG.
   - Product-health trend analysis.
   - Automated anomaly detection.
   - Cross-domain insights combining feedback, support, and product metrics.

---

# Design Intent

This project is intentionally an **exploration / proof of concept**.

The current implementation demonstrates:

**ElevenLabs + Workflow + Webhook + FastAPI + Product Health Data**

---

# Documentation

Component-specific documentation is intentionally maintained inside each folder.

- **ElevenLabs configuration:** [`elevenlabs/README.md`](./elevenlabs/README.md)
- **FastAPI backend:** [`fastapi/README.md`](./fastapi/README.md)

The folder-level READMEs contain the detailed implementation and configuration information for their respective components.

---

## License

This project is licensed under the MIT License. See [`LICENSE`](./LICENSE).
