import requests
import json

class InterviewSimulator:
    def __init__(self, model="llama3"):
        self.model = model

    def simulate(self, topic: str, mode: int = 0):
        if mode == 1:
            # One-shot prompt
            example = (
                f"Topic: sleep quality\n"
                f"Psychiatrist: How have you been sleeping lately?\n"
                f"Patient: Not very well, I keep waking up during the night.\n"
                f"Psychiatrist: That must be exhausting. Has this been going on for a while?\n"
                f"Patient: Yeah, for a couple of weeks now.\n\n"
            )
        else:
            example = ""

        prompt = (
            f"{example}"
            f"Now simulate an interview on the topic: {topic}.\n"
            f"Generate a realistic, clear, 3-turn conversation:\n"
            f"Psychiatrist: ...\nPatient: ...\nPsychiatrist: ...\nPatient: ...\n"
            f"Include natural follow-up questions."
        )

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt
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
