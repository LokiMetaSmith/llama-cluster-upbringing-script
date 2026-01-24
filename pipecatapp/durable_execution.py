import sqlite3
import pickle
import functools
import logging
import time
import os
import inspect
from enum import Enum

logger = logging.getLogger(__name__)

class InvocationStatus(Enum):
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"

class DurableExecutionEngine:
    def __init__(self, db_path="~/.config/pipecat/durable_execution.db"):
        self.db_path = os.path.expanduser(db_path)
        self._ensure_db_dir()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.create_table()

    def _ensure_db_dir(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                logger.error(f"Could not create directory for durable execution DB: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS execution_log (
                    flowId TEXT NOT NULL,
                    step_sequence INTEGER NOT NULL,
                    step_name TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    args BLOB,
                    return_value BLOB,
                    PRIMARY KEY (flowId, step_sequence)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error creating durable execution table: {e}")

    def get_invocation(self, flow_id, step_sequence):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT status, return_value FROM execution_log
                WHERE flowId = ? AND step_sequence = ?
            """, (flow_id, step_sequence))
            row = cursor.fetchone()
            if row:
                status_str, return_value_blob = row
                try:
                    return_value = pickle.loads(return_value_blob) if return_value_blob else None
                    return {"status": InvocationStatus(status_str), "return_value": return_value}
                except (pickle.UnpicklingError, EOFError) as e:
                    logger.error(f"Error unpickling return value for flow {flow_id} step {step_sequence}: {e}")
                    return None
            return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving invocation: {e}")
            return None

    def log_invocation_start(self, flow_id, step_sequence, step_name, args):
        print(f"DEBUG: log_invocation_start {flow_id} seq {step_sequence} step {step_name}")
        try:
            cursor = self.conn.cursor()
            try:
                args_blob = pickle.dumps(args)
            except Exception as e:
                logger.error(f"Error pickling args for step {step_name}: {e}")
                args_blob = pickle.dumps(f"<unpickleable: {str(e)}>")

            timestamp = int(time.time() * 1000)
            cursor.execute("""
                INSERT OR REPLACE INTO execution_log (flowId, step_sequence, step_name, timestamp, status, args, return_value)
                VALUES (?, ?, ?, ?, ?, ?, NULL)
            """, (flow_id, step_sequence, step_name, timestamp, InvocationStatus.PENDING.value, args_blob))
            self.conn.commit()
            print("DEBUG: log_invocation_start committed")
        except sqlite3.Error as e:
            print(f"DEBUG: log_invocation_start error: {e}")
            logger.error(f"Error logging invocation start: {e}")

    def log_invocation_completion(self, flow_id, step_sequence, result):
        print(f"DEBUG: log_invocation_completion {flow_id} seq {step_sequence}")
        try:
            cursor = self.conn.cursor()
            try:
                result_blob = pickle.dumps(result)
            except Exception as e:
                logger.error(f"Error pickling result for flow {flow_id} step {step_sequence}: {e}")
                result_blob = pickle.dumps(f"<unpickleable_result: {str(e)}>")

            cursor.execute("""
                UPDATE execution_log
                SET status = ?, return_value = ?
                WHERE flowId = ? AND step_sequence = ?
            """, (InvocationStatus.COMPLETE.value, result_blob, flow_id, step_sequence))
            self.conn.commit()
            print("DEBUG: log_invocation_completion committed")
        except sqlite3.Error as e:
            print(f"DEBUG: log_invocation_completion error: {e}")
            logger.error(f"Error logging invocation completion: {e}")

def _pre_execution(instance, func_name, args, kwargs):
    """Helper to handle pre-execution logic (checking cache, logging start)."""
    print(f"DEBUG: _pre_execution {func_name}")
    if not hasattr(instance, 'durable_engine') or not instance.durable_engine:
        print("DEBUG: No durable_engine")
        return None, False
    if not hasattr(instance, 'current_flow_id') or not instance.current_flow_id:
        print("DEBUG: No current_flow_id")
        return None, False

    flow_id = instance.current_flow_id

    if not hasattr(instance, 'step_counter'):
        instance.step_counter = 0

    current_step_seq = instance.step_counter
    instance.step_counter += 1

    invocation = instance.durable_engine.get_invocation(flow_id, current_step_seq)

    if invocation and invocation['status'] == InvocationStatus.COMPLETE:
        logger.info(f"Durable: Replaying step {func_name} (seq {current_step_seq}) for flow {flow_id}")
        return invocation['return_value'], True

    call_args = (args, kwargs)
    instance.durable_engine.log_invocation_start(flow_id, current_step_seq, func_name, call_args)

    return (flow_id, current_step_seq), False

def _post_execution(instance, context, result):
    """Helper to handle post-execution logic (logging completion)."""
    print("DEBUG: _post_execution")
    flow_id, current_step_seq = context
    instance.durable_engine.log_invocation_completion(flow_id, current_step_seq, result)

def durable_step(func):
    """
    Decorator to make a method execution durable.
    Supports both sync and async methods.
    """
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            cached_result, is_cached = _pre_execution(self, func.__name__, args, kwargs)
            if is_cached:
                return cached_result

            # Execute original async function
            result = await func(self, *args, **kwargs)

            # Only log completion if we had a valid context (meaning logging started)
            # We need to re-check/re-calculate context or return it from pre_execution.
            # But _pre_execution returns None as context if skipped.
            # Wait, _pre_execution returns (context, is_cached).
            # If skipped, context is None.
            # But if I call _pre_execution again, it increments counter!
            # So I need to capture the return value of _pre_execution.
            # I did: cached_result, is_cached = ...
            # But cached_result IS the context if not cached? No.
            # Refactor _pre_execution to return (result_or_context, status_enum)?

            # Let's inline the check to avoid confusion or return a structured object.
            pass # see below for better logic flow

            # Re-implementing wrapper logic using local variables correctly
            return result

        # Correct async implementation
        @functools.wraps(func)
        async def async_wrapper_corrected(self, *args, **kwargs):
            context_or_result, is_cached = _pre_execution(self, func.__name__, args, kwargs)
            if is_cached:
                return context_or_result

            context = context_or_result
            result = await func(self, *args, **kwargs)

            if context:
                _post_execution(self, context, result)
            return result

        return async_wrapper_corrected

    else:
        @functools.wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            context_or_result, is_cached = _pre_execution(self, func.__name__, args, kwargs)
            if is_cached:
                return context_or_result

            context = context_or_result
            result = func(self, *args, **kwargs)

            if context:
                _post_execution(self, context, result)
            return result

        return sync_wrapper
