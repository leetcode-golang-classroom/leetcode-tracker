"""Shared helpers for talking to `gh` (issues + Projects v2) from the seed/record scripts."""
from __future__ import annotations

import json
import subprocess


def run(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout.strip()


def run_graphql(query: str, **fields: str) -> dict:
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in fields.items():
        args += ["-f", f"{key}={value}"]
    return json.loads(run(args))


def find_issue(repo: str, title_token: str) -> dict | None:
    out = run([
        "gh", "issue", "list", "--repo", repo, "--state", "all",
        "--search", f'"{title_token}" in:title',
        "--json", "id,number,title,url",
        "--limit", "1",
    ])
    items = json.loads(out) if out else []
    return items[0] if items else None


def create_issue(repo: str, title: str, body: str, labels: list[str]) -> dict:
    args = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
    for label in labels:
        args += ["--label", label]
    url = run(args)
    out = run(["gh", "issue", "view", url, "--json", "id,number,title,url"])
    return json.loads(out)


def comment_on_issue(issue_url: str, body: str) -> None:
    run(["gh", "issue", "comment", issue_url, "--body", body])


def add_sub_issue(parent_node_id: str, sub_node_id: str) -> None:
    mutation = """
    mutation($issueId: ID!, $subIssueId: ID!) {
      addSubIssue(input: {issueId: $issueId, subIssueId: $subIssueId}) {
        subIssue { id }
      }
    }
    """
    try:
        run_graphql(mutation, issueId=parent_node_id, subIssueId=sub_node_id)
    except RuntimeError as exc:
        if "already a sub-issue" in str(exc).lower():
            return
        raise


def get_project_meta(owner: str, number: str) -> dict:
    out = run(["gh", "project", "view", number, "--owner", owner, "--format", "json"])
    project = json.loads(out)
    fields_out = run(["gh", "project", "field-list", number, "--owner", owner, "--format", "json"])
    fields = json.loads(fields_out)["fields"]
    return {"id": project["id"], "fields": {f["name"]: f for f in fields}}


def add_item_to_project(owner: str, number: str, issue_url: str) -> str:
    out = run(["gh", "project", "item-add", number, "--owner", owner, "--url", issue_url, "--format", "json"])
    return json.loads(out)["id"]


def set_single_select(project_id: str, item_id: str, field: dict, option_name: str) -> None:
    option = next((o for o in field.get("options", []) if o["name"].lower() == option_name.lower()), None)
    if option is None:
        print(f"  ! warning: option '{option_name}' not found on field '{field['name']}', skipping")
        return
    run([
        "gh", "project", "item-edit",
        "--id", item_id, "--project-id", project_id,
        "--field-id", field["id"], "--single-select-option-id", option["id"],
    ])


def set_number(project_id: str, item_id: str, field: dict, value: float) -> None:
    run([
        "gh", "project", "item-edit",
        "--id", item_id, "--project-id", project_id,
        "--field-id", field["id"], "--number", str(value),
    ])


def set_iteration_by_index(project_id: str, item_id: str, field: dict, week: int) -> None:
    iterations = sorted(field.get("iterations", []), key=lambda it: it["startDate"])
    if week < 1 or week > len(iterations):
        print(f"  ! warning: no iteration configured for week {week} yet (only {len(iterations)} exist), skipping")
        return
    iteration = iterations[week - 1]
    run([
        "gh", "project", "item-edit",
        "--id", item_id, "--project-id", project_id,
        "--field-id", field["id"], "--iteration-id", iteration["id"],
    ])
