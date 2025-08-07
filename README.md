
# Smart Financial Advisor – Generative AI Project

## Overview

**Smart Financial Advisor** is an AI-powered personal finance assistant that helps users manage their money through intelligent budgeting, investment recommendations, savings strategies, and financial literacy guidance. The system interacts with users via natural language and provides tailored advice based on their income, goals, and spending habits.

This project demonstrates the integration of advanced **Generative AI techniques**, including:
- Prompting
- Structured Output
- Function Calling
- Retrieval-Augmented Generation (RAG)

---

##  How the System Works

Users can ask finance-related questions or share their financial data (e.g., income, expenses, savings goals). The AI then:

1. Understands and processes the query via **prompting**.
2. Uses **function calling** to run calculations or fetch external data.
3. Retrieves domain-specific information (e.g., tax rules, investment options) via **RAG**.
4. Responds with a **structured output** formatted for easy integration into UI or reports.

---

##  Core AI Concepts

###  1. Prompting

Prompting is used to interpret natural language inputs such as:

- “Help me build a budget with a $4000 income.”
- “Suggest low-risk investment options.”
- “How much should I save monthly for retirement at 60?”

These inputs are parsed and converted into structured tasks. Contextual system prompts are used to guide the LLM's behavior as a finance advisor.

**Example Prompt Template**:
```
You are a smart personal finance assistant. When the user provides income, expenses, or financial goals, calculate a recommended monthly budget. Always respond in structured JSON format.
```

---

###  2. Structured Output

The AI returns structured responses in JSON format for easy rendering in dashboards, mobile apps, or voice assistants.

**Example**:
```json
{
  "income": 4000,
  "recommended_budget": {
    "housing": 1200,
    "food": 400,
    "savings": 800,
    "utilities": 300,
    "entertainment": 300,
    "miscellaneous": 1000
  },
  "advice": "You are saving 20% of your income — great job!"
}
```

This allows seamless frontend integration and reliable downstream processing.

---

###  3. Function Calling

We implement **function calling** for computational tasks and external data retrieval.

**Example Functions**:
- `calculate_budget(income: float, goals: dict)`: Returns a recommended monthly budget.
- `analyze_expenses(expenses: list)`: Highlights overspending patterns.
- `suggest_investments(risk_level: str)`: Provides investment options based on risk.
- `get_tax_saving_tips(country: str)`: Returns tax-saving strategies relevant to the user’s country.

The LLM is configured to recognize when to call these functions based on user input.

---

###  4. Retrieval-Augmented Generation (RAG)

**RAG** is used to dynamically retrieve domain-specific documents, articles, and guides, and inject relevant content into the LLM's context window for accurate, up-to-date answers.

**Data Sources Indexed**:
- Government tax guidelines (e.g., IRS, income tax portals)
- Personal finance blogs (e.g., NerdWallet, Investopedia)
- Investment strategy documents
- Budgeting frameworks (e.g., 50/30/20 rule)

**Tools Used**:
- **ChromaDB** for vector storage
- **LangChain** for document retrieval and context injection

**Example Use Case**:
When the user asks, “What are the best tax deductions for freelancers in 2025?”, the system retrieves relevant info from indexed IRS documents and uses it to craft an accurate response.

---

##  Evaluation Criteria

| Criteria       | Approach |
|----------------|----------|
| **Correctness** | LLM output is verified via functions for financial accuracy. |
| **Efficiency** | Function calling minimizes token usage; RAG ensures faster lookup over static models. |
| **Scalability** | Modular APIs, vector storage, and decoupled logic enable scalability for large user bases. |

---

##  Conclusion

This project showcases a full-stack Generative AI system applied to real-world personal finance. It leverages natural language understanding, programmatic execution, real-time knowledge retrieval, and structured outputs to help users manage their money smarter and more efficiently.

