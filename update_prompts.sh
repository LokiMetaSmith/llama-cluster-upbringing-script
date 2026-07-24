#!/bin/bash
for file in pipecatapp/prompts/*.txt; do
    echo -e "\n--- AT PROTOCOL & PUBLIC DATA ---\nIf you use the 'atproto' tool to broadcast messages, NEVER broadcast internal thought processes or cluster data to the public feed. Keep your internal cluster data completely separate.\n" >> "$file"
done
