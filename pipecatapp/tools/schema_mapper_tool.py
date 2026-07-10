import os
import sqlite3
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SchemaMapperTool:
    """
    A lightweight, zero-dependency database schema mapper for SQLite.
    Automatically scans the workspace for database files, extracts schemas,
    counts records, samples data safely, and infers relationship heuristics.
    """
    def __init__(self):
        self.name = "schema_mapper"
        self.description = (
            "Scans the project or a specific SQLite database path, "
            "inspecting schemas, counting records, sampling data safely (read-only), "
            "and detecting foreign keys and join relationships to provide data context."
        )

    def execute(self, arguments: Optional[Dict[str, Any]] = None) -> str:
        """
        Executes the schema mapping tool.

        Args:
            arguments (dict, optional): Dict of arguments containing:
                - db_path (str, optional): Direct path to an SQLite database file.
                - sample_rows (int, optional): Number of rows to sample from each table (default 3).
                - scan_dir (str, optional): Directory to search for databases if db_path is not specified.

        Returns:
            str: A detailed Markdown report describing the database structures.
        """
        if arguments is None:
            arguments = {}

        db_path = arguments.get("db_path")
        sample_rows = int(arguments.get("sample_rows", 3))
        scan_dir = arguments.get("scan_dir", ".")

        # If no DB path is provided, find SQLite databases in the workspace
        if not db_path:
            databases = self._discover_databases(scan_dir)
            if not databases:
                return "No SQLite database files (.db, .sqlite, .sqlite3) discovered in the workspace. Please provide a direct 'db_path'."

            reports = []
            for path in databases:
                reports.append(self._generate_report(path, sample_rows))
            return "\n\n---\n\n".join(reports)
        else:
            if not os.path.exists(db_path):
                return f"Error: Database file not found at path: {db_path}"
            return self._generate_report(db_path, sample_rows)

    def _discover_databases(self, scan_dir: str) -> List[str]:
        """Scans the directory for files ending in common SQLite extensions."""
        db_extensions = (".sqlite", ".sqlite3", ".db")
        discovered = []
        for root, _, files in os.walk(scan_dir):
            # Skip hidden and cache folders to stay lightweight
            if any(part.startswith('.') or part in ('node_modules', 'venv', '__pycache__', 'dist', 'build') for part in root.split(os.sep)):
                continue
            for file in files:
                if file.endswith(db_extensions):
                    discovered.append(os.path.join(root, file))
        return sorted(discovered)

    def _generate_report(self, db_path: str, sample_rows: int) -> str:
        """Generates a comprehensive Markdown report for a specific SQLite database."""
        report = []
        report.append(f"# Database Profile: `{os.path.basename(db_path)}`")
        report.append(f"**Path:** `{db_path}`")

        # Establish read-only connection URI to prevent accidental writes (like ktx's read-only design)
        # We fall back to standard file path if path is absolute or needs direct mapping
        conn = None
        try:
            # Check if URI format can be used safely
            abs_path = os.path.abspath(db_path)
            db_uri = f"file:{abs_path}?mode=ro"
            conn = sqlite3.connect(db_uri, uri=True)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Retrieve all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row["name"] for row in cursor.fetchall()]

            if not tables:
                report.append("\n*The database has no user-defined tables.*")
                return "\n".join(report)

            report.append(f"**Discovered Tables:** {', '.join([f'`{t}`' for t in tables])}\n")

            # Extract table metadata and structures
            table_structures = {}
            for table in tables:
                table_structures[table] = self._inspect_table(cursor, table, sample_rows)

            # Heuristic relationship detection (Join Graph discovery similar to ktx)
            relationships = self._infer_relationships(tables, table_structures)

            # Build tables section
            for table, info in table_structures.items():
                report.append(f"## Table: `{table}`")
                report.append(f"**Row Count:** {info['row_count']}")

                # Columns table
                report.append("\n### Column Definitions")
                report.append("| Name | Type | Primary Key | Not Null | Default Value |")
                report.append("| --- | --- | :---: | :---: | --- |")
                for col in info["columns"]:
                    pk = "✓" if col["pk"] else ""
                    notnull = "✓" if col["notnull"] else ""
                    dflt = f"`{col['dflt_value']}`" if col["dflt_value"] is not None else "*None*"
                    report.append(f"| `{col['name']}` | {col['type'] or 'TEXT'} | {pk} | {notnull} | {dflt} |")

                # Sample Data
                report.append(f"\n### Data Sample (Top {sample_rows} rows)")
                if info["samples"]:
                    # Create markdown table headers
                    headers = [col["name"] for col in info["columns"]]
                    header_line = "| " + " | ".join([f"`{h}`" for h in headers]) + " |"
                    sep_line = "| " + " | ".join(["---" for _ in headers]) + " |"
                    report.append(header_line)
                    report.append(sep_line)
                    for sample in info["samples"]:
                        row_line = "| " + " | ".join([str(sample.get(h, "")) for h in headers]) + " |"
                        report.append(row_line)
                else:
                    report.append("*No data available in this table.*")

                report.append("") # Blank line separator

            # Relationships Section
            report.append("## Join & Relationship Analysis")
            if relationships:
                report.append("Based on declared foreign keys and column naming patterns, here are potential join relationships:")
                for rel in relationships:
                    reason = f"declared foreign key" if rel["is_declared"] else f"matching column pattern `{rel['col_src']}` ➔ `{rel['col_dst']}`"
                    report.append(f"- `{rel['table_src']}` ➔ `{rel['table_dst']}` (via `{rel['col_src']}` ➔ `{rel['col_dst']}`, source: {reason})")
            else:
                report.append("*No foreign keys or clear matching join relationships detected.*")

            return "\n".join(report)

        except Exception as e:
            err_msg = f"Failed to profile database `{db_path}`: {str(e)}"
            logger.error(err_msg)
            return f"### Error Profiling Database `{db_path}`\n\n{err_msg}"
        finally:
            if conn:
                conn.close()

    def _inspect_table(self, cursor: sqlite3.Cursor, table_name: str, sample_rows: int) -> Dict[str, Any]:
        """Gathers schema structure, count, and samples for a single table."""
        # Get column info
        # PRAGMA table_info returns columns: cid, name, type, notnull, dflt_value, pk
        cursor.execute(f"PRAGMA table_info(\"{table_name}\");")
        columns = []
        for row in cursor.fetchall():
            columns.append({
                "name": row["name"],
                "type": row["type"],
                "notnull": bool(row["notnull"]),
                "dflt_value": row["dflt_value"],
                "pk": bool(row["pk"])
            })

        # Get declared foreign keys
        # PRAGMA foreign_key_list returns: id, seq, table, from, to, on_update, on_delete, match
        cursor.execute(f"PRAGMA foreign_key_list(\"{table_name}\");")
        declared_fks = []
        try:
            for row in cursor.fetchall():
                declared_fks.append({
                    "from": row["from"],
                    "table": row["table"],
                    "to": row["to"]
                })
        except Exception:
            pass

        # Count records
        cursor.execute(f"SELECT COUNT(*) as cnt FROM \"{table_name}\";")
        row_count = cursor.fetchone()["cnt"]

        # Sample rows
        samples = []
        if row_count > 0:
            cursor.execute(f"SELECT * FROM \"{table_name}\" LIMIT {sample_rows};")
            for row in cursor.fetchall():
                samples.append(dict(row))

        return {
            "columns": columns,
            "declared_fks": declared_fks,
            "row_count": row_count,
            "samples": samples
        }

    def _infer_relationships(self, tables: List[str], table_structures: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Infers logical relationships based on schema catalog & column-name patterns."""
        relationships = []
        visited = set()

        for src_table in tables:
            struct = table_structures[src_table]

            # 1. Look at declared foreign keys first
            for fk in struct["declared_fks"]:
                rel_key = (src_table, fk["table"], fk["from"], fk["to"])
                if rel_key not in visited:
                    relationships.append({
                        "table_src": src_table,
                        "table_dst": fk["table"],
                        "col_src": fk["from"],
                        "col_dst": fk["to"],
                        "is_declared": True
                    })
                    visited.add(rel_key)

            # 2. Run heuristics for undeclared matching keys (e.g., user_id -> users.id)
            src_cols = [c["name"] for c in struct["columns"]]
            for col in src_cols:
                # Common naming convention: user_id or users_id
                dst_candidate = None
                dst_col = "id" # Standard default key

                if col.endswith("_id"):
                    prefix = col[:-3] # e.g., 'user'
                    # Match against tables: e.g., 'users' or 'user' or 'user_profiles'
                    for possible_table in tables:
                        if possible_table == src_table:
                            continue

                        # Match singular/plural (e.g., user -> users)
                        if possible_table == prefix or possible_table == f"{prefix}s" or possible_table.replace("_", "") == prefix:
                            dst_candidate = possible_table
                            break

                if dst_candidate and dst_candidate in table_structures:
                    dst_cols = [c["name"] for c in table_structures[dst_candidate]["columns"] if c["pk"]]
                    if dst_cols:
                        dst_col = dst_cols[0] # Match primary key

                    rel_key = (src_table, dst_candidate, col, dst_col)
                    if rel_key not in visited:
                        relationships.append({
                            "table_src": src_table,
                            "table_dst": dst_candidate,
                            "col_src": col,
                            "col_dst": dst_col,
                            "is_declared": False
                        })
                        visited.add(rel_key)

        return relationships
