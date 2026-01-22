import os
import json
from typing import Any, Optional
import requests
import openai
from app.models.schemas import MarksheetOutput
from app.core.config import settings

# Configure OpenAI if used
openai.api_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY

PROMPT = """
You are given raw OCR text of an academic marksheet. Extract fields into a JSON object matching the schema described.
Return only valid JSON.
Schema keys: candidate (with name,father_name,mother_name,roll_no,registration_no,dob,exam_year,board,institution) each with value and confidence (0-1),
subjects: list of {subject, max_marks, obtained_marks, grade?} each with value+confidence,
overall_result {value, confidence}, issue_date {value, confidence}, issue_place {value, confidence}.
Also include raw_text and confidence_explanation.
"""


def _try_parse_json_from_text(text: str) -> Optional[dict]:
    text = text.strip()
    # Try to locate a JSON substring if the model returned extra text
    if text.startswith("{"):
        try:
            return json.loads(text)
        except Exception:
            pass
    # Attempt to find first { .. } block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            pass
    return None


def _call_openai(raw_text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts structured student marksheet data."},
        {"role": "user", "content": PROMPT + "\n\nOCR_TEXT:\n" + raw_text}
    ]
    resp = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=messages,
        temperature=0.0,
        max_tokens=1500,
    )
    return resp["choices"][0]["message"]["content"]


def _call_gemini(raw_text: str) -> str:
    """Call a Gemini-compatible HTTP endpoint.

    The implementation expects the environment variables `GEMINI_ENDPOINT` and
    `GEMINI_API_KEY` to be set. The `GEMINI_ENDPOINT` should be a full URL for
    the model generate endpoint (for example a Google generative models endpoint).
    This adapter is intentionally generic: different Gemini-style endpoints may
    vary in request/response shape.
    """
    endpoint = os.getenv("GEMINI_ENDPOINT")
    api_key = os.getenv("GEMINI_API_KEY")
    if not endpoint or not api_key:
        raise RuntimeError("GEMINI_ENDPOINT and GEMINI_API_KEY must be set for Gemini provider")

    payload = {"prompt": PROMPT + "\n\nOCR_TEXT:\n" + raw_text}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    # Try multiple common response shapes
    body = r.json()
    # Common pattern: {"candidates": [{"content": "..."}]}
    if isinstance(body, dict):
        if "candidates" in body and isinstance(body["candidates"], list):
            return body["candidates"][0].get("content", "")
        if "output" in body:
            # e.g., {output: "text"}
            return body.get("output")
        # Try output_text
        if "output_text" in body:
            return body.get("output_text")
        # Try nested outputs
        if "outputs" in body and isinstance(body["outputs"], list):
            for o in body["outputs"]:
                if isinstance(o, dict):
                    if "text" in o:
                        return o["text"]
                    if "content" in o:
                        return o["content"]
    # Fallback to raw text
    return r.text


def parse_with_llm(raw_text: str) -> MarksheetOutput:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    try:
        if provider == "gemini":
            content = _call_gemini(raw_text)
        else:
            content = _call_openai(raw_text)

        parsed = _try_parse_json_from_text(content)
        if parsed is None:
            raise ValueError("Could not parse JSON from LLM response")
        return MarksheetOutput.parse_obj(parsed)
    except Exception as e:
        return MarksheetOutput(
            candidate={
                "name": {"value": None, "confidence": 0.0},
                "father_name": {"value": None, "confidence": 0.0},
                "mother_name": {"value": None, "confidence": 0.0},
                "roll_no": {"value": None, "confidence": 0.0},
                "registration_no": {"value": None, "confidence": 0.0},
                "dob": {"value": None, "confidence": 0.0},
                "exam_year": {"value": None, "confidence": 0.0},
                "board": {"value": None, "confidence": 0.0},
                "institution": {"value": None, "confidence": 0.0},
            },
            subjects=[],
            overall_result={"value": None, "confidence": 0.0},
            raw_text=raw_text,
            confidence_explanation=f"llm_error: {str(e)[:200]}"
        )
