import sys
import os
import pytest
import sqlite3
import time

# Append the directory containing gateway.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ansible/roles/moe_gateway/files")))

import gateway

def test_marsaglia_tsang_math():
    # Verify that sampling works without errors and stays in [0, 1]
    for _ in range(50):
        val = gateway.sample_beta(5.0, 5.0)
        assert 0.0 <= val <= 1.0

def test_select_best_expert():
    # Mock some metrics in a temp database
    test_db = "/tmp/test_gateway_metrics.db"
    if os.path.exists(test_db):
        os.remove(test_db)

    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            request_id TEXT PRIMARY KEY,
            timestamp REAL,
            user_input TEXT,
            response TEXT,
            status_code INTEGER,
            latency REAL,
            expert_name TEXT DEFAULT 'default'
        )
    ''')

    now = time.time()
    # Log 10 successes for openai_gpt4 (should have high score)
    for i in range(10):
        c.execute('''
            INSERT INTO requests (request_id, timestamp, user_input, response, status_code, latency, expert_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (f"req-{i}", now - i * 60, "hi", "response", 200, 0.2, "openai_gpt4"))

    # Log 10 failures for openrouter_gemini_flash (should have low score)
    for i in range(10):
        c.execute('''
            INSERT INTO requests (request_id, timestamp, user_input, response, status_code, latency, expert_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (f"req-fail-{i}", now - i * 60, "hi", "error", 500, 1.0, "openrouter_gemini_flash"))

    conn.commit()
    conn.close()

    # Check that scores reflect the feedback
    scores = gateway.get_expert_scores(test_db, gateway.EXTERNAL_EXPERTS)

    assert "openai_gpt4" in scores
    assert "openrouter_gemini_flash" in scores
    # Due to reliability sampling, gpt4 should beat gemini_flash (as gemini has all 500s)
    assert scores["openai_gpt4"] > scores["openrouter_gemini_flash"]

    if os.path.exists(test_db):
        os.remove(test_db)
