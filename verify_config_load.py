import yaml
import os
import json

def load_config():
    try:
        with open('group_vars/external_experts.yaml', 'r') as f:
            ext_experts = yaml.safe_load(f)

        with open('group_vars/all.yaml', 'r') as f:
            all_vars = yaml.safe_load(f)

        llm_config = ext_experts['external_experts_config']['openai_gpt4']
        llm_config['api_key_plaintext'] = all_vars.get('openai_api_key')

        print("Successfully loaded config:")
        print(json.dumps(llm_config, indent=2))
        return llm_config
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_config()
