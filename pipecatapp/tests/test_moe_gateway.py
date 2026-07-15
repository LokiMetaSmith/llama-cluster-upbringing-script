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

def test_bonsai_expert_scores():
    # Verify both models are in the external experts dictionary
    assert "together_ternary_bonsai_27b" in gateway.EXTERNAL_EXPERTS
    assert "together_1bit_bonsai_27b" in gateway.EXTERNAL_EXPERTS

    test_db = "/tmp/test_bonsai_metrics.db"
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
    # Log equal successes and latency for ternary and 1-bit Bonsai
    for i in range(5):
        c.execute('''
            INSERT INTO requests (request_id, timestamp, user_input, response, status_code, latency, expert_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (f"req-ternary-{i}", now - i * 60, "hi", "response", 200, 0.5, "together_ternary_bonsai_27b"))
        c.execute('''
            INSERT INTO requests (request_id, timestamp, user_input, response, status_code, latency, expert_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (f"req-1bit-{i}", now - i * 60, "hi", "response", 200, 0.5, "together_1bit_bonsai_27b"))

    conn.commit()
    conn.close()

    # Mock sample_beta to return exactly expected values for precise comparison
    original_sample_beta = gateway.sample_beta
    try:
        # Mock sample_beta to return a constant 1.0 (perfect reliability) for predictable scoring
        gateway.sample_beta = lambda a, b: 1.0
        scores = gateway.get_expert_scores(test_db, gateway.EXTERNAL_EXPERTS)

        assert "together_ternary_bonsai_27b" in scores
        assert "together_1bit_bonsai_27b" in scores

        # ternary should have score higher than 1bit because of higher intelligence score (0.8 > 0.75)
        # score = 0.5 * reliability (1.0) + 0.25 * speed + 0.25 * intel
        assert scores["together_ternary_bonsai_27b"] > scores["together_1bit_bonsai_27b"]
        assert scores["together_ternary_bonsai_27b"] - scores["together_1bit_bonsai_27b"] == pytest.approx(0.25 * (0.8 - 0.75))
    finally:
        gateway.sample_beta = original_sample_beta

    if os.path.exists(test_db):
        os.remove(test_db)
