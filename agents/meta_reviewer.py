import requests
import json

class MetaReviewer:
    def __init__(self, model="llama3"):
        self.model = model

    def review(self, interview_text: str, qualitative_assessment: str, quantitative_assessment: str):
        prompt = f"""
You are an expert psychiatrist AI assistant. Given the interview transcript, the qualitative assessment, and the quantitative PHQ-8 assessment, synthesize all information to produce a final diagnostic suggestion focusing on depression.

Interview transcript:
{interview_text}

Qualitative assessment:
{qualitative_assessment}

Quantitative assessment:
{quantitative_assessment}

Please provide a clear, concise, and structured diagnostic summary, mentioning confidence levels and any recommendations for further clinical evaluation.
"""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt.strip()
            },
            stream=True
        )

        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = line.decode("utf-8")
                data = json.loads(chunk)
                piece = data.get("response", "")
                full_response += piece

        return full_response
