import os
import pandas as pd


def extract_prompt_examples(transcript_folder: str, max_files=None):
    examples = []
    files = [f for f in os.listdir(transcript_folder) if f.endswith("_Transcript.csv")]

    if max_files:
        files = files[:max_files]

    for filename in files:
        file_path = os.path.join(transcript_folder, filename)
        try:
            df = pd.read_csv(file_path, sep="\t")
            lines = []

            for _, row in df.iterrows():
                speaker = row.get("speaker", "").strip()
                text = row.get("value", "").strip()
                if speaker and text:
                    if speaker.lower() == "ellie":
                        speaker = "Psychiatrist"
                    lines.append(f"{speaker}: {text}")

            full_dialogue = "\n".join(lines)
            examples.append(full_dialogue)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return examples
