import os
import sys
import json
import argparse
import requests
import time

def get_prometheus_metrics(prom_url, window):
    # Query: max by (exported_job, task_group, task) (max_over_time(nomad_client_allocs_memory_usage[24h]))
    # Note: exported_job usually corresponds to the Job ID.
    query = f'max by (exported_job, task_group, task) (max_over_time(nomad_client_allocs_memory_usage[{window}]))'
    print(f"Querying Prometheus: {prom_url} with {query}")
    try:
        resp = requests.get(f"{prom_url}/api/v1/query", params={'query': query}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data['status'] != 'success':
            print(f"Error querying Prometheus: {data}")
            return []
        return data['data']['result']
    except Exception as e:
        print(f"Failed to query Prometheus: {e}")
        return []

def get_job_spec(nomad_url, job_id):
    try:
        resp = requests.get(f"{nomad_url}/v1/job/{job_id}", timeout=10)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Failed to get job {job_id}: {e}")
        return None

def update_job_memory(nomad_url, job_spec, modifications):
    job_id = job_spec['ID']

    # Create a deep copy of the job spec to modify
    # We strip operational fields that shouldn't be submitted back
    job_payload = job_spec.copy()

    # Fields to potentially strip to avoid conflicts
    # job_payload.pop('Version', None)
    # job_payload.pop('SubmitTime', None)
    # job_payload.pop('CreateIndex', None)
    # job_payload.pop('ModifyIndex', None)
    # job_payload.pop('JobModifyIndex', None)

    changed = False

    # Iterate through task groups and tasks
    # We use a loop index approach or match by name
    if 'TaskGroups' in job_payload:
        for tg in job_payload['TaskGroups']:
            tg_name = tg['Name']
            if 'Tasks' in tg:
                for task in tg['Tasks']:
                    task_name = task['Name']

                    # Check if we have a modification for this task
                    for mod_tg, mod_task, new_mem in modifications:
                        if mod_tg == tg_name and mod_task == task_name:
                            resources = task.get('Resources', {})
                            old_mem = resources.get('MemoryMB', 0)

                            # Only update if the difference is significant (> 1MB)
                            if abs(old_mem - new_mem) > 1:
                                print(f"  [PATCH] {job_id}.{tg_name}.{task_name}: Memory {old_mem}MB -> {new_mem}MB")

                                # Ensure Resources dict exists
                                if 'Resources' not in task:
                                    task['Resources'] = {}

                                task['Resources']['MemoryMB'] = int(new_mem)
                                changed = True

    if changed:
        print(f"Updating Job {job_id}...")
        try:
            # The API expects {"Job": {...}}
            payload = {'Job': job_payload}
            resp = requests.post(f"{nomad_url}/v1/job/{job_id}", json=payload, timeout=10)
            resp.raise_for_status()
            print(f"Successfully updated job {job_id}")
            return True
        except Exception as e:
            print(f"Failed to update job {job_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
    else:
        print(f"No changes applied to {job_id} (values were already close).")
        return False

def main():
    parser = argparse.ArgumentParser(description='Audit and Optimize Nomad Memory Usage')
    parser.add_argument('--prometheus-url', default=os.environ.get('PROMETHEUS_URL', 'http://localhost:9090'), help='Prometheus URL')
    parser.add_argument('--nomad-url', default=os.environ.get('NOMAD_ADDR', 'http://localhost:4646'), help='Nomad URL')
    parser.add_argument('--window', default='24h', help='Prometheus query window (e.g., 24h, 7d)')
    parser.add_argument('--apply', action='store_true', help='Apply changes to Nomad jobs')
    parser.add_argument('--dry-run', action='store_true', help='Do not apply changes (default unless --apply is set)')

    args = parser.parse_args()

    # Safety check: if dry-run is set, unset apply
    if args.dry_run:
        args.apply = False

    print(f"Starting Memory Audit (Window: {args.window})")
    print(f"Prometheus: {args.prometheus_url}")
    print(f"Nomad: {args.nomad_url}")

    results = get_prometheus_metrics(args.prometheus_url, args.window)

    if not results:
        print("No metrics found.")
        sys.exit(0)

    audit_log = []
    job_modifications = {} # {job_id: {'spec': job_spec, 'mods': []}}

    for res in results:
        metric = res['metric']
        job_id = metric.get('exported_job')
        tg_name = metric.get('task_group')
        task_name = metric.get('task')

        if not job_id or not tg_name or not task_name:
            continue

        try:
            peak_bytes = float(res['value'][1])
        except (ValueError, IndexError):
            continue

        peak_mb = peak_bytes / (1024 * 1024)

        # Calculate target memory: Peak * 1.05 (5% buffer)
        target_mb = int(peak_mb * 1.05)
        # Enforce a minimum safety floor (e.g. 32MB) to prevent choking tiny processes
        if target_mb < 32:
            target_mb = 32

        # Fetch Job Spec if not already fetched
        if job_id not in job_modifications:
            spec = get_job_spec(args.nomad_url, job_id)
            if spec:
                job_modifications[job_id] = {'spec': spec, 'mods': []}
            else:
                print(f"Skipping {job_id}: Could not fetch job spec.")
                continue

        job_data = job_modifications[job_id]
        spec = job_data['spec']

        # Find current reservation
        current_mb = None

        # Traverse spec to find the task
        # Note: Nomad job structure: Job -> TaskGroups -> Tasks
        found_task = False
        if 'TaskGroups' in spec:
            for tg in spec['TaskGroups']:
                if tg['Name'] == tg_name:
                    if 'Tasks' in tg:
                        for task in tg['Tasks']:
                            if task['Name'] == task_name:
                                current_mb = task.get('Resources', {}).get('MemoryMB', 0)
                                found_task = True
                                break
                if found_task: break

        if not found_task:
            print(f"Warning: Task {tg_name}.{task_name} not found in job {job_id} spec.")
            continue

        # Analyze
        status = "OK"
        # Logic: We want Reserved ~= Peak * 1.05
        # If Reserved is significantly different from Target

        # Thresholds:
        # If Under-provisioned (Reserved < Peak): Critical
        # If Over-provisioned (Reserved > Target): Optimization Opportunity

        # We use a 10% tolerance to avoid flapping
        diff = target_mb - current_mb

        if current_mb < peak_mb:
            status = "CRITICAL_UNDER_PROVISIONED"
        elif abs(diff) > (current_mb * 0.1) or abs(diff) > 50:
            # If changed by more than 10% OR more than 50MB
            if diff > 0:
                status = "NEEDS_INCREASE"
            else:
                status = "NEEDS_DECREASE"

        if status != "OK":
            job_data['mods'].append((tg_name, task_name, target_mb))

        audit_log.append({
            'job': job_id,
            'group': tg_name,
            'task': task_name,
            'peak_mb': round(peak_mb, 2),
            'current_mb': current_mb,
            'recommended_mb': target_mb,
            'status': status
        })

    # Output JSON Report
    print("=== AUDIT REPORT ===")
    print(json.dumps(audit_log, indent=2))
    print("====================")

    # Apply changes
    if args.apply:
        print("Applying optimizations...")
        for job_id, data in job_modifications.items():
            if data['mods']:
                update_job_memory(args.nomad_url, data['spec'], data['mods'])
    else:
        print("Dry-run complete. Use --apply to enforce changes.")

if __name__ == '__main__':
    main()
