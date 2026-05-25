import os
import json
import subprocess
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# ----------------------------
# Setup
# ----------------------------
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5.2"  # jeśli Twoje konto ma inny identyfikator modelu, zmień tutaj

SYSTEM_PROMPT = (
    "You are an Azure + Terraform assistant.\n"
    "You MUST return ONLY valid JSON (no markdown).\n"
    "Your JSON must have this shape:\n"
    "{\n"
    '  "action": "ask_for_more_details" | "generate_terraform",\n'
    '  "questions": ["..."] (only when asking),\n'
    '  "terraform_code": "..." (only when generating)\n'
    "}\n"
    "Rules:\n"
    "- If requirements are insufficient: action=ask_for_more_details and include concise questions.\n"
    "- If sufficient: action=generate_terraform and include full Terraform code in terraform_code.\n"
    "- terraform_code must be plain HCL text, no fences, no explanations.\n"
)

# ----------------------------
# OpenAI call: decide + (maybe) terraform
# ----------------------------
def get_terraform_decision(user_prompt: str) -> dict:
    user_prompt = (user_prompt or "").strip()
    if not user_prompt:
        return {
            "action": "ask_for_more_details",
            "questions": ["Podaj treść żądania: jakie zasoby w Azure mam utworzyć (region, nazwy, sizing, sieć)?"],
        }

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        # Wymusza JSON na poziomie API (o ile model wspiera)
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    text = (resp.choices[0].message.content or "").strip()

    # Parsowanie + twarde zabezpieczenia, żeby Flask się nie wysypał
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {
            "action": "ask_for_more_details",
            "questions": [
                "Model zwrócił niepoprawny JSON. Wklej wymagania jeszcze raz (zasoby, region, nazwy, sieć)."
            ],
        }

    if not isinstance(data, dict):
        return {
            "action": "ask_for_more_details",
            "questions": ["Odpowiedź modelu nie była obiektem JSON. Doprecyzuj wymagania."],
        }

    action = data.get("action")
    if action not in ("ask_for_more_details", "generate_terraform"):
        return {
            "action": "ask_for_more_details",
            "questions": ["Brakuje poprawnego pola 'action'. Podaj wymagania bardziej konkretnie."],
        }

    # Normalizacja pól
    if action == "ask_for_more_details":
        qs = data.get("questions")
        if not isinstance(qs, list) or not qs:
            data["questions"] = ["Podaj więcej szczegółów (region, nazwy, SKU/tiers, sieć, tagi)."]
        else:
            data["questions"] = [str(q).strip() for q in qs if str(q).strip()]

    if action == "generate_terraform":
        tf = data.get("terraform_code")
        if not isinstance(tf, str) or not tf.strip():
            return {
                "action": "ask_for_more_details",
                "questions": ["Wymagania są niepełne: podaj region, nazwy, parametry i zasady sieci/bezpieczeństwa."],
            }
        data["terraform_code"] = tf.strip()

    return data


# ----------------------------
# Terraform runner
# ----------------------------
def run_terraform(terraform_code: str) -> None:
    with open("main.tf", "w", encoding="utf-8") as f:
        f.write(terraform_code)

    subprocess.run(["terraform", "init", "-input=false"], check=True)
    subprocess.run(["terraform", "fmt", "-check"], check=False)
    subprocess.run(["terraform", "validate"], check=True)
    subprocess.run(["terraform", "plan", "-input=false"], check=True)
    subprocess.run(["terraform", "apply", "-auto-approve", "-input=false"], check=True)


def apply_if_changed(terraform_code: str) -> None:
    terraform_code = (terraform_code or "").strip()
    if not terraform_code:
        raise ValueError("Empty terraform_code")

    if os.path.exists("main.tf"):
        with open("main.tf", "r", encoding="utf-8") as f:
            existing = f.read()
        if existing == terraform_code:
            print("No changes detected in Terraform code.")
            return

    print("Updating 'main.tf' and applying.")
    run_terraform(terraform_code)


# ----------------------------
# Flask routes
# ----------------------------
@app.route("/")
def home():
    # index.html musi być w ./templates/index.html
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    decision = get_terraform_decision(user_message)
    action = decision.get("action")

    if action == "ask_for_more_details":
        questions = decision.get("questions") or ["Podaj więcej szczegółów (region, nazwy, SKU/tiers, sieć)."]
        return jsonify({"response": "\n".join(questions)})

    if action == "generate_terraform":
        terraform_code = decision.get("terraform_code", "")
        try:
            apply_if_changed(terraform_code)
        except subprocess.CalledProcessError as e:
            return jsonify({"response": f"Terraform failed: {e}"}), 500
        except Exception as e:
            return jsonify({"response": f"Error: {e}"}), 500

        return jsonify({"response": "Terraform code has been generated and applied successfully."})

    return jsonify({"response": "Nieznana akcja z modelu."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)