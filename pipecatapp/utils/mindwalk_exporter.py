import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class MindwalkTraceExporter:
    """
    Adapter/Trace Exporter that serializes agent workflow and tool execution logs
    into the normalized schema format expected by cosmtrek/mindwalk (trace.schema.json v1).
    """

    @staticmethod
    def calculate_stats(
        events: List[Dict[str, Any]],
        marks: List[Dict[str, Any]],
        files_in_repo: int = 0
    ) -> Dict[str, Any]:
        """
        Dynamically calculates the exact statistical metrics required by trace.schema.json.
        """
        # Initialize counts
        actions = {
            "search": 0,
            "read": 0,
            "edit": 0,
            "exec": 0,
            "verify": 0,
            "other": 0
        }
        errors = {
            "search": 0,
            "read": 0,
            "edit": 0,
            "exec": 0,
            "verify": 0,
            "other": 0
        }

        # Track file touches for fovea, parafovea, and edits
        fovea_files = set()      # Read or edited
        parafovea_files = set()  # Hit only (not read or edited)
        edited_files = set()     # Edited
        edit_counts_per_file = {}  # File path -> edit count

        events_before_first_edit = 0
        has_edited = False

        total_result_bytes = 0
        last_verify_idx = -1
        edit_events_positions = []  # indices of edit events

        for idx, event in enumerate(events):
            action = event.get("action", "other")
            if action in actions:
                actions[action] += 1
                if event.get("isError", False):
                    errors[action] += 1

            total_result_bytes += event.get("resultBytes", 0)

            # Check edit-before-first-edit
            if action == "edit" and not has_edited:
                events_before_first_edit = idx
                has_edited = True

            if action == "edit":
                edit_events_positions.append(idx)

            if action == "verify":
                last_verify_idx = idx

            # Process targets to analyze visual attention states (fovea, parafovea)
            for target in event.get("targets", []):
                path = target.get("path")
                touch = target.get("touch", "hit")
                if not path:
                    continue

                if touch == "edit":
                    edited_files.add(path)
                    fovea_files.add(path)
                    edit_counts_per_file[path] = edit_counts_per_file.get(path, 0) + 1
                elif touch == "read":
                    fovea_files.add(path)
                elif touch == "hit":
                    parafovea_files.add(path)

        # Parafovea files are only hit, never read or edited
        parafovea_files = parafovea_files - fovea_files

        # Churn files: Edited in 3 or more separate events
        churn_files = sum(1 for path, count in edit_counts_per_file.items() if count >= 3)
        max_edits_per_file = max(edit_counts_per_file.values()) if edit_counts_per_file else 0

        # Edits after last verify: Every edit event occurring after the last verify event
        if last_verify_idx == -1:
            # If never verified, it is every edit event
            edits_after_last_verify = len(edit_events_positions)
        else:
            edits_after_last_verify = sum(1 for pos in edit_events_positions if pos > last_verify_idx)

        # If there were no edit events at all, eventsBeforeFirstEdit should be 0 (or length of events)
        if not has_edited:
            events_before_first_edit = len(events)

        # Regression Rate: verify errors / verify actions
        verify_actions = actions["verify"]
        regression_rate = float(errors["verify"]) / verify_actions if verify_actions > 0 else 0.0

        # Error Rate: total errors / total actions
        total_actions = sum(actions.values())
        error_rate = float(sum(errors.values())) / total_actions if total_actions > 0 else 0.0

        # User turns, compactions, and subagents counts from timeline marks
        user_turns = sum(1 for m in marks if m.get("type") == "user-message")
        compactions = sum(1 for m in marks if m.get("type") == "compaction")
        subagents = sum(1 for m in marks if m.get("type") == "subagent")

        return {
            "filesInRepo": files_in_repo,
            "fovea": len(fovea_files),
            "parafovea": len(parafovea_files),
            "edited": len(edited_files),
            "eventsBeforeFirstEdit": events_before_first_edit,
            "regressionRate": regression_rate,
            "errorRate": error_rate,
            "actions": actions,
            "errors": errors,
            "maxEditsPerFile": max_edits_per_file,
            "churnFiles": churn_files,
            "userTurns": user_turns,
            "compactions": compactions,
            "subagents": subagents,
            "resultBytes": total_result_bytes,
            "editsAfterLastVerify": edits_after_last_verify,
            "observability": {
                "reads": "exact",
                "errors": "exact"
            }
        }

    def export_trace(
        self,
        session_id: str,
        harness: str,
        events: List[Dict[str, Any]],
        marks: List[Dict[str, Any]],
        model: Optional[str] = None,
        title: Optional[str] = None,
        cwd: Optional[str] = None,
        commit: Optional[str] = None,
        started_at: Optional[str] = None,
        ended_at: Optional[str] = None,
        files_in_repo: int = 0
    ) -> Dict[str, Any]:
        """
        Converts the provided telemetry lists into a fully compliant mindwalk trace dictionary.
        """
        # Ensure correct sequences are assigned
        normalized_events = []
        for i, ev in enumerate(events):
            event_copy = ev.copy()
            event_copy["seq"] = i
            # Ensure required fields have valid defaults
            if "ts" not in event_copy:
                event_copy["ts"] = datetime.now(timezone.utc).isoformat()
            if "tool" not in event_copy:
                event_copy["tool"] = "unknown"
            if "action" not in event_copy:
                event_copy["action"] = "other"
            if "targets" not in event_copy:
                event_copy["targets"] = []
            if "resultBytes" not in event_copy:
                event_copy["resultBytes"] = 0
            if "isError" not in event_copy:
                event_copy["isError"] = False
            if "summary" not in event_copy:
                event_copy["summary"] = ""
            normalized_events.append(event_copy)

        normalized_marks = []
        for i, mk in enumerate(marks):
            mark_copy = mk.copy()
            mark_copy["seq"] = i
            normalized_marks.append(mark_copy)

        # Create session metadata block
        session_data = {
            "id": session_id,
            "harness": harness,
            "eventCount": len(normalized_events)
        }
        if model:
            session_data["model"] = model
        if title:
            session_data["title"] = title
        if cwd:
            session_data["cwd"] = cwd
        if commit:
            session_data["commit"] = commit
        if started_at:
            session_data["startedAt"] = started_at
        if ended_at:
            session_data["endedAt"] = ended_at

        # Calculate exact metrics
        stats = self.calculate_stats(normalized_events, normalized_marks, files_in_repo=files_in_repo)

        return {
            "version": 1,
            "session": session_data,
            "events": normalized_events,
            "marks": normalized_marks,
            "stats": stats
        }

    def export_trace_to_file(
        self,
        filepath: str,
        session_id: str,
        harness: str,
        events: List[Dict[str, Any]],
        marks: List[Dict[str, Any]],
        model: Optional[str] = None,
        title: Optional[str] = None,
        cwd: Optional[str] = None,
        commit: Optional[str] = None,
        started_at: Optional[str] = None,
        ended_at: Optional[str] = None,
        files_in_repo: int = 0
    ) -> None:
        """
        Exports the mindwalk-compliant trace directly into a JSON file.
        """
        trace_data = self.export_trace(
            session_id=session_id,
            harness=harness,
            events=events,
            marks=marks,
            model=model,
            title=title,
            cwd=cwd,
            commit=commit,
            started_at=started_at,
            ended_at=ended_at,
            files_in_repo=files_in_repo
        )
        with open(filepath, "w") as f:
            json.dump(trace_data, f, indent=2)
