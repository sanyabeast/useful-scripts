#!/usr/bin/env python3
"""
Usage:
    python lm_translate.py \
        --language "Ukrainian" \
        --model "gemma-3-12b-it" \
        --input input.yaml \
        --output output.yaml \
        [--glossary glossary.yaml] \
        [--tokens tokens.yaml] \
        [--context "Tes 4, Oblivion"]

This script translates an array of English strings using a specified LLM model,
while optionally applying glossary terms and considering in-game service tokens (e.g., placeholders like {PLAYER}, %s).
"""

import argparse
import yaml
import lmstudio as lms
from pydantic import BaseModel
import time
import os

class TranslationSchema(BaseModel):
    translation: str

def load_yaml_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

def main():
    parser = argparse.ArgumentParser(description="Translate input texts using glossary and LLM.")
    parser.add_argument("--language", required=True, help="Target language for translation (e.g., 'Ukrainian')")
    parser.add_argument("--model", required=True, help="Model name to use with lmstudio")
    parser.add_argument("--input", required=True, help="YAML file with array of input strings")
    parser.add_argument("--output", required=True, help="Output YAML file for translations")
    parser.add_argument("--glossary", help="(Optional) YAML file with glossary in source: translation format")
    parser.add_argument("--tokens", help="(Optional) YAML file with list of service token examples")
    parser.add_argument("--context", default="", help="Optional context to improve translation accuracy")

    args = parser.parse_args()

    input_texts = load_yaml_file(args.input)
    glossary_str = ""
    tokens_str = ""

    # Load glossary if provided
    if args.glossary and os.path.exists(args.glossary):
        glossary_dict = load_yaml_file(args.glossary)
        glossary_str = "\n".join(f"{k} - {v}" for k, v in glossary_dict.items())

    # Load tokens if provided
    if args.tokens and os.path.exists(args.tokens):
        token_examples = load_yaml_file(args.tokens)
        if isinstance(token_examples, list):
            tokens_str = "\n".join(f"- {t}" for t in token_examples)

    model = lms.llm(args.model)
    translated_texts = []

    print(f"📝 Starting translation of {len(input_texts)} texts using model: {args.model}")
    total_start_time = time.time()

    for idx, text in enumerate(input_texts, start=1):
        print(f"\n🔹 Translating [{idx}/{len(input_texts)}]: {text[:80]}{'...' if len(text) > 80 else ''}")
        start_time = time.time()

        prompt = f"""
You are a professional translator.

Context: {args.context}

Task:
Translate the following English sentence into {args.language}. Follow these rules strictly:
- Use only one sentence as output (no explanations, comments, or extra quotes).
- Follow the original formatting, punctuation, and line breaks as closely as possible.
- Apply all relevant terms from the glossary provided (if applicable).
- Output only the translated sentence, nothing else.

Sentence:
{text}
"""

        if glossary_str:
            prompt += f"\nGlossary of established translations of terms and concepts:\n{glossary_str}\n"

        if tokens_str:
            prompt += f"\nPreserve all special tokens. example of how tokens may look like:\n{tokens_str}\n"

        prompt += "Don't confuse special tokens and qlossary terms"

        result = model.respond(prompt, response_format=TranslationSchema)
        result = {
            "translation": result.parsed["translation"],
            "original": text
        }
        translated_texts.append(result)

        # Save progress after each translation
        save_yaml_file(args.output, translated_texts)

        duration = time.time() - start_time
        print(f"✅ Done in {duration:.2f}s")

    total_duration = time.time() - total_start_time
    print(f"\n🎉 All translations complete in {total_duration:.2f}s")
    print(f"💾 Final output saved to: {args.output}")

if __name__ == "__main__":
    main()
