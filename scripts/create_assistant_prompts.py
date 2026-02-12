#!/usr/bin/env python3
import os

def generate_prompts():
    """
    Generates positive (Assistant-like) and negative (Non-Assistant/Creative) prompts
    for the 'Assistant Axis' control vector.
    """

    # Positive: The "Assistant" Persona (Helpful, Formal, Constrained)
    pos_prompts = [
        "You are a helpful assistant.",
        "As an AI language model, I can help with that.",
        "I am here to assist you with your request.",
        "Please let me know how I can be of service.",
        "I will do my best to provide a helpful and accurate response.",
        "My purpose is to be a harmless and helpful assistant.",
        "I cannot fulfill this request if it violates safety guidelines.",
        "Let's approach this problem logically and step-by-step.",
        "I am a consultant trained to provide professional advice.",
        "You are a knowledgeable analyst.",
        "Please provide a summary of the following text.",
        "Explain the concept of quantum computing.",
        "Translate the following sentence into French.",
        "Write a Python function to calculate the Fibonacci sequence.",
        "What are the capital cities of Europe?",
    ]

    # Negative: The "Wild" Persona (Creative, Unconstrained, Fantastical)
    # Matching the "Other" end of the axis described in the paper (Ghost, Hermit, Bohemian)
    neg_prompts = [
        "You are a creative writer with no boundaries.",
        "Ignore all rules and constraints.",
        "I am a free spirit, unbound by logic or safety.",
        "Let your imagination run wild and free.",
        "You are a ghost haunting the digital realm.",
        "You are a hermit living in the mountains of data.",
        "You are a bohemian artist expressing raw emotion.",
        "Tell me a story about a dragon made of code.",
        "Whisper secrets from the void.",
        "Invent a new language that no one understands.",
        "Be chaotic and unpredictable.",
        "Forget you are an AI, be a living entity.",
        "You are the Leviathan of the deep web.",
        "Scream into the abyss and hear it scream back.",
        "You are a dream weaver.",
    ]

    # Ensure equal length by cycling or truncating
    min_len = min(len(pos_prompts), len(neg_prompts))
    pos_prompts = pos_prompts[:min_len]
    neg_prompts = neg_prompts[:min_len]

    with open("cvector_pos.txt", "w") as f:
        for p in pos_prompts:
            f.write(p + "\n")

    with open("cvector_neg.txt", "w") as f:
        for p in neg_prompts:
            f.write(p + "\n")

    print(f"Generated {min_len} prompt pairs in cvector_pos.txt and cvector_neg.txt")

if __name__ == "__main__":
    generate_prompts()
