# 🧾 AI Underwriting & Claims Assistant  
A lightweight Flask web application that uses LLMs to generate **structured underwriting summaries**, **claims analyses**, and **follow-up emails** for missing information.  
Designed as a quick-win AI prototype that mirrors real business workflows in **Property & Casualty (P&C) insurance**.

---

## 🚀 Overview

Insurance workflows are full of repetitive, document-heavy tasks:  
- Adjusters must summarize claim narratives  
- Underwriters review inspection reports and risk descriptions  
- Both groups repeatedly request missing information from customers or agents

This tool demonstrates how **Generative AI + well-designed prompts** can automate parts of these workflows by:

✔ Extracting structured insights from unstructured text  
✔ Highlighting missing or unclear information  
✔ Drafting professional follow-up emails  
✔ Supporting both claims and underwriting modes  
✔ Providing a foundation for future agentic workflows  

This is similar to the type of “quick-win” prototype an Enterprise AI team would build for operational teams.

---

## ✨ Features

### 🧾 **Claim Analysis Mode**
- Summarizes a claim narrative into:
  - Claim overview  
  - Cause of loss  
  - Damages  
  - Parties involved  
  - Liability indicators  
  - Coverage concerns  
  - Missing information  
- Auto-generates a follow-up email for the insured

### 🏢 **Underwriting Mode**
- Extracts key risk details from inspection reports or business descriptions
- Provides:
  - Risk overview  
  - Hazards & exposures  
  - Protections  
  - Past losses  
  - Recommended follow-up questions  
  - Risk classification (Low / Medium / High)
- Generates an underwriter-style follow-up email

### 🎨 **Modern UI**
- Clean lavender-themed interface  
- Responsive design  
- Easy text input and structured output display  

### 🧠 **LLM-Powered**
Built using `openai` Python SDK (supports GPT-4o-mini, GPT-4.1-mini, etc.)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Flask** – lightweight web framework
- **OpenAI API** – LLM inference
- **HTML/CSS** – no build tools required  
- **Jinja2 templates** – simple templating engine  
