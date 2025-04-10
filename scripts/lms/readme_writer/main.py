#!/usr/bin/env python3
"""
Usage:
    python describe_scripts_with_llm.py --input-folder "path/to/scripts" --output-folder "path/to/output" --model "gemma-3-4b-it"

This script recursively processes script files from the input folder and uses an LLM to generate
a detailed README for each one. It mirrors the input folder structure in the output directory.
"""

import argparse
from pathlib import Path
import lmstudio as lms
from pydantic import BaseModel

SCRIPT_EXTENSIONS = {".ts", ".js", ".py", ".bat", ".sh"}

class ScriptDescription(BaseModel):
    description: str

def is_script_file(path: Path):
    return path.is_file() and path.suffix.lower() in SCRIPT_EXTENSIONS

def generate_markdown(script_path: Path, description: str) -> str:
    return f"""# {script_path.name}

{description.strip()}
"""

def main():
    parser = argparse.ArgumentParser(description="Generate detailed README files for script files using an LLM.")
    parser.add_argument("--input-folder", required=True, help="Path to the folder containing scripts")
    parser.add_argument("--output-folder", required=True, help="Path to the output folder")
    parser.add_argument("--model", required=True, help="LLM model name to use")
    args = parser.parse_args()

    input_folder = Path(args.input_folder)
    output_folder = Path(args.output_folder)
    model = lms.llm(args.model)

    if not input_folder.exists() or not input_folder.is_dir():
        print("❌ Error: Input folder does not exist or is not a directory.")
        return

    print(f"📁 Input folder: {input_folder.resolve()}")
    print(f"📂 Output folder: {output_folder.resolve()}")
    print("🔍 Scanning for script files...\n")

    script_files = [f for f in input_folder.rglob("*") if is_script_file(f)]
    total_scripts = len(script_files)

    if total_scripts == 0:
        print("⚠️ No script files found.")
        return

    print(f"📄 Found {total_scripts} script(s). Starting generation...\n")

    for idx, script_path in enumerate(script_files, start=1):
        try:
            print(f"🔄 [{idx}/{total_scripts}] Processing: {script_path}")

            script_text = script_path.read_text(encoding='utf-8', errors='ignore')
            script_name = script_path.name

            chat = lms.Chat()

            chat.add_user_message(f"""
You are a senior software engineer reviewing the script named "{script_name}". Your task is to generate a **comprehensive and well-structured README** for this file.

Please include the following:
- An overview of what the script does.
- A breakdown of the main components or logic.
- Any assumptions, requirements, or limitations.
- Example use cases, if relevant.
- Anything else a developer or user might want to know.
- Usage examples

Here is the script content:
`
{script_text}
`
""")
            chat.add_user_message(script_text)

            prediction = model.respond(chat, response_format=ScriptDescription)
            description = prediction.parsed["description"]

            relative_path = script_path.relative_to(input_folder)
            output_readme_path = output_folder / relative_path.with_suffix(".md")
            output_readme_path.parent.mkdir(parents=True, exist_ok=True)
            output_readme_path.write_text(generate_markdown(script_path, description), encoding='utf-8')

            print(f"✅ Created: {output_readme_path}\n")

        except Exception as e:
            print(f"❌ [{idx}/{total_scripts}] Error processing {script_path.name}: {e}\n")

    print("🎉 All done!")

if __name__ == "__main__":
    main()
