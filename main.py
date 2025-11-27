import os
from flask import Flask, render_template, request, flash
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# Initialize OpenAI client
client = OpenAI()

# ---------- LLM HELPERS ---------- #
def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """
    Generic helper to call the LLM. Assumes OPENAI_API_KEY is set.
    You can swap model as needed.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling LLM: {e}"


def generate_claim_summary(claim_text: str) -> str:
    system_prompt = (
        "You are a precise assistant for Property & Casualty (P&C) insurance claims. "
        "You summarize claims in a structured way for adjusters. "
        "Use only information from the input text. If something is unknown, say 'Unknown'."
    )

    user_prompt = f"""
Summarize the following claim description into the structure below.

Claim text:
\"\"\"{claim_text}\"\"\"

Return your answer under these headings:

1. Claim Overview
2. Cause of Loss
3. Damages (property, bodily injury, other)
4. Parties Involved
5. Potential Liability Indicators
6. Coverage Concerns / Notes
7. Missing or Ambiguous Information (list as bullets)
"""
    return call_llm(system_prompt, user_prompt)


def generate_claim_followup_email(claim_text: str) -> str:
    system_prompt = (
        "You are a professional P&C claims representative. "
        "You write short, clear, polite emails to customers to request missing information. "
        "Keep tone friendly and professional."
    )

    user_prompt = f"""
Based ONLY on the following claim description, first identify what information is missing
or unclear for proper claim handling. Then write a short email to the policyholder
requesting that information.

Claim text:
\"\"\"{claim_text}\"\"\"

Format your answer as:

Missing information:
- ...

Email:
[email body here]
"""
    return call_llm(system_prompt, user_prompt)


def generate_underwriting_summary(report_text: str) -> str:
    system_prompt = (
        "You are an underwriting assistant for Property & Casualty (P&C) insurance. "
        "You extract risk-relevant information from inspection reports or applications. "
        "Use only information from the input text. If something is unknown, say 'Unknown'."
    )

    user_prompt = f"""
Analyze the following text, which may be an inspection report, application,
or narrative about a property or business. Summarize it for an underwriter.

Text:
\"\"\"{report_text}\"\"\"

Return your answer under these headings:

1. Risk Overview
2. Property / Operations Description
3. Hazards & Exposures
4. Protections (e.g., sprinklers, alarms, security, fire services)
5. Past Losses or Incidents (if any)
6. Overall Risk Level (Low / Medium / High) with 1–2 sentence justification
7. Missing Information or Recommended Follow-Up Questions
"""
    return call_llm(system_prompt, user_prompt)


def generate_underwriting_followup_email(report_text: str) -> str:
    system_prompt = (
        "You are an underwriting assistant for a P&C insurer. "
        "You write concise, professional emails to agents or insureds to clarify "
        "missing information needed to complete underwriting."
    )

    user_prompt = f"""
Based ONLY on the following text, identify the key pieces of missing information
or unclear areas for underwriting. Then draft a concise email to the agent or insured
requesting that information.

Text:
\"\"\"{report_text}\"\"\"

Format your answer as:

Missing information:
- ...

Email:
[email body here]
"""
    return call_llm(system_prompt, user_prompt)


# ---------- ROUTES ---------- #

@app.route("/", methods=["GET", "POST"])
def index():
    mode = "claim"
    input_text = ""
    summary_output = ""
    email_output = ""

    if request.method == "POST":
        mode = request.form.get("mode", "claim")
        input_text = request.form.get("input_text", "").strip()

        if not input_text:
            flash("Please paste some text to analyze.", "error")
        else:
            if mode == "claim":
                summary_output = generate_claim_summary(input_text)
                email_output = generate_claim_followup_email(input_text)
            else:  # underwriting
                summary_output = generate_underwriting_summary(input_text)
                email_output = generate_underwriting_followup_email(input_text)

    return render_template(
        "index.html",
        mode=mode,
        input_text=input_text,
        summary_output=summary_output,
        email_output=email_output,
    )


if __name__ == "__main__":
    app.run(debug=True)
