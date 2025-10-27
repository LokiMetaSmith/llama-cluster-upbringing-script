import requests

def create_reflection():
    """Generates a structured reflection from an AI's interaction log.

    This function reads the content of `aid_e_log.txt`, formats it into a
    prompt using the "Learn, Reflect, Apply, Prepare" framework, and sends it
    to a local LLaMA C++ server. The generated reflection is then printed to the
    console and saved to a Markdown file.
    """
    log_file_path = "aid_e_log.txt"
    reflection_output_path = "reflection/daily_reflection.md"
    llama_cpp_url = "http://localhost:8080/completion"

    # 1. Read the log file
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file_path}")
        return
    except Exception as e:
        print(f"Error reading log file: {e}")
        return

    # 2. Define the prompt for the reflection
    prompt = f"""
You are an AI assistant tasked with generating a reflection on a log of an AI's interactions.
The reflection should be based on the "Learn, Reflect, Apply, Prepare" framework.

Here is the log file content:
---
{log_content}
---

Based on the log, please generate a reflection that covers the following four areas:

1.  **Learn:** What new ideas, perspectives, or information did the AI encounter or learn today?
2.  **Reflect:** What does this learning mean for the AI? How does it connect to its purpose, its identity, or the challenges it faces? What patterns can be observed in its behavior or thoughts?
3.  **Apply:** Did the AI apply its knowledge or skills in any way? Were there any actions taken based on its learning or reflections?
4.  **Prepare:** What did the AI do today that will help its future self? Did it set up any systems, make any plans, or take any small actions that will be beneficial tomorrow?

The reflection should be insightful and useful for both the AI itself and a human who is reviewing the AI's progress.
The output should be in Markdown format.
"""

    # 3. Send the request to the llama.cpp server
    payload = {
        "prompt": prompt,
        "n_predict": 1024,  # Adjust as needed
        "stream": False,
        "temperature": 0.7,
    }

    print("Sending request to llama.cpp server...")
    try:
        response = requests.post(llama_cpp_url, json=payload, timeout=300)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to llama.cpp server at {llama_cpp_url}: {e}")
        print("Please ensure the llama.cpp server is running and accessible.")
        return

    # 4. Parse the response and save the reflection
    try:
        response_json = response.json()
        reflection_content = response_json.get("content", "")

        if not reflection_content:
            print("Error: Received an empty reflection from the server.")
            print("Server response:", response.text)
            return

        print("Received reflection from server.")

        # 5. Save the reflection to a Markdown file
        with open(reflection_output_path, 'w', encoding='utf-8') as f:
            f.write(reflection_content)

        print(f"Reflection saved to {reflection_output_path}")
        print("\n--- Generated Reflection ---")
        print(reflection_content)

    except Exception as e:
        print(f"Error processing server response: {e}")
        print("Server response:", response.text)

if __name__ == "__main__":
    create_reflection()
