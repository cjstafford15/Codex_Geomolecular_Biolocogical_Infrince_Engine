"""Captain Connectivity Agent.

This private-first captain report tracks whether the project is ready to
coordinate with GitHub, Sky Net, n8n, and local agents without accidentally
turning private research material into public output.
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "obsidian-vault"
REPORT_DIR = VAULT / "Agent Reports"
SCRIPTS_DIR = ROOT / "scripts"
N8N_DIR = ROOT / "n8n"
WORKFLOWS_DIR = N8N_DIR / "workflows"
GITHUB_REPO = "cjstafford15/Codex_Geomolecular_Biolocogical_Infrince_Engine"


def run_text(cmd: List[str]) -> tuple[int, str]:
    """Run a read-only local command and return its exit code and trimmed output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, str(exc)

    output = (result.stdout or result.stderr or "").strip()
    return result.returncode, output


def check_tiktoken_status() -> Dict[str, Any]:
    """Check if tiktoken is properly integrated for tokenization tasks."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        test_tokens = enc.encode("test geomolecular tokenization")
        status = "operational"
        score = 100
        notes = f"tiktoken ready with {len(test_tokens)} test tokens"
    except ImportError:
        status = "missing"
        score = 0
        notes = "tiktoken not installed - run pip install tiktoken"
    except Exception as e:
        status = "error"
        score = 25
        notes = f"tiktoken error: {str(e)}"
    
    return {
        "component": "tokenization",
        "library": "tiktoken",
        "status": status,
        "score": score,
        "notes": notes,
        "opportunities": ["AI text processing", "embedding preparation", "model input tokenization"]
    }


def check_privacy_posture() -> Dict[str, Any]:
    """Check that the GitHub coordination surface is private-first."""
    issues: List[str] = []
    notes: List[str] = []

    remote_code, remote_output = run_text(["git", "remote", "get-url", "origin"])
    remote_url = remote_output if remote_code == 0 else ""
    if not remote_url:
        issues.append("No origin remote found; GitHub coordination cannot be verified locally.")
    elif GITHUB_REPO not in remote_url:
        issues.append(f"Origin remote does not match expected private repo: {remote_url}")
    else:
        notes.append(f"Origin remote points at expected repo: {GITHUB_REPO}.")

    visibility = "unknown"
    gh_code, gh_output = run_text([
        "gh",
        "repo",
        "view",
        GITHUB_REPO,
        "--json",
        "visibility",
        "--jq",
        ".visibility",
    ])
    if gh_code == 0 and gh_output:
        visibility = gh_output.lower()
        if visibility != "private":
            issues.append(f"GitHub repo visibility is {visibility}; expected private.")
        else:
            notes.append("GitHub CLI confirms repository visibility is private.")
    else:
        notes.append("GitHub CLI visibility check unavailable; use the GitHub connector or repo settings to verify privacy.")

    workflow_files = list(WORKFLOWS_DIR.glob("*.json")) if WORKFLOWS_DIR.exists() else []
    for workflow_file in workflow_files:
        raw = workflow_file.read_text(encoding="utf-8")
        if re.search(r"(api[_-]?key|access[_-]?token|password|client[_-]?secret)", raw, re.IGNORECASE):
            issues.append(f"Possible secret-like field found in n8n workflow export: {workflow_file.name}")

    if issues:
        status = "attention_needed"
        score = 40 if visibility == "public" else 70
        notes.extend(issues)
    elif visibility == "private":
        status = "private_confirmed"
        score = 100
    else:
        status = "private_policy_local"
        score = 85

    return {
        "component": "privacy_posture",
        "status": status,
        "score": score,
        "notes": " ".join(notes),
        "repo": GITHUB_REPO,
        "origin_remote": remote_url,
        "visibility": visibility,
        "policy": "Keep project coordination private; do not publish webhook URLs, repo contents, reports, or external-drive knowledge dumps publicly.",
        "opportunities": [
            "Verify GitHub repo privacy after every remote migration",
            "Keep n8n webhook URLs private",
            "Use private issues or PRs for cross-project messages",
        ],
    }


def analyze_n8n_workflows() -> Dict[str, Any]:
    """Analyze n8n workflows for private local automation readiness."""
    if not WORKFLOWS_DIR.exists():
        return {
            "component": "n8n_workflows",
            "status": "missing",
            "score": 0,
            "notes": "No n8n workflows directory found",
            "workflows": [],
            "integrations": []
        }
    
    workflows: List[Dict[str, Any]] = []
    integrations = set()
    issues: List[str] = []
    
    for wf_file in WORKFLOWS_DIR.glob("*.json"):
        try:
            wf_data = json.loads(wf_file.read_text(encoding="utf-8"))
            
            wf_name = wf_data.get("name", wf_file.stem)
            nodes = wf_data.get("nodes", [])
            tags = wf_data.get("tags", [])
            version_id = wf_data.get("versionId", "")
            
            wf_integrations = []
            commands = []
            webhook_paths = []
            has_webhook = False
            has_execute_command = False
            has_response = False
            has_external_egress = False
            for node in nodes:
                node_type = node.get("type", "")
                node_type_lower = node_type.lower()
                parameters = node.get("parameters", {})

                if "webhook" in node_type_lower:
                    has_webhook = True
                    path = parameters.get("path")
                    if path:
                        webhook_paths.append(path)
                if "executecommand" in node_type_lower:
                    has_execute_command = True
                    command = parameters.get("command", "")
                    commands.append(command)
                    if command and "scripts/run_pipeline.py" not in command and "scripts\\run_pipeline.py" not in command:
                        issues.append(f"{wf_file.name} execute command does not run the project pipeline: {command}")
                if "respondtowebhook" in node_type_lower:
                    has_response = True
                if "httprequest" in node_type_lower or "email" in node_type_lower or "slack" in node_type_lower:
                    has_external_egress = True

                if "http" in node_type_lower or "webhook" in node_type_lower or "api" in node_type_lower:
                    wf_integrations.append(node_type)
                    integrations.add(node_type)

            if not has_webhook:
                issues.append(f"{wf_file.name} has no webhook trigger.")
            if not has_execute_command:
                issues.append(f"{wf_file.name} has no Execute Command pipeline node.")
            if not has_response:
                issues.append(f"{wf_file.name} has no webhook response node.")
            if has_external_egress:
                issues.append(f"{wf_file.name} contains an external egress node; review privacy before import.")
            
            workflows.append({
                "file": wf_file.name,
                "name": wf_name,
                "nodes": len(nodes),
                "api_nodes": len(wf_integrations),
                "integrations": wf_integrations,
                "webhook_paths": webhook_paths,
                "commands": commands,
                "tags": tags,
                "version_id": version_id,
                "private_ready": not has_external_egress and has_webhook and has_execute_command and has_response,
            })
            
        except Exception as e:
            workflows.append({
                "name": wf_file.stem,
                "error": str(e)
            })
            issues.append(f"{wf_file.name} could not be parsed: {e}")
    
    total_workflows = len(workflows)
    
    api_workflows = sum(1 for w in workflows if w.get("api_nodes", 0) > 0)
    private_ready = sum(1 for w in workflows if w.get("private_ready"))
    
    if total_workflows == 0:
        score = 0
        status = "empty"
        notes = "No workflows found"
    elif issues:
        score = max(40, int((private_ready / total_workflows) * 100))
        status = "attention_needed"
        notes = "; ".join(issues)
    else:
        score = min(100, int((private_ready / total_workflows) * 100))
        status = "private_local_ready" if score == 100 else "limited"
        notes = f"{private_ready}/{total_workflows} workflows run the local project pipeline without external egress nodes"
    
    return {
        "component": "n8n_workflows",
        "status": status,
        "score": score,
        "notes": notes,
        "workflows": workflows,
        "unique_integrations": list(integrations),
        "opportunities": [
            "Keep webhook URLs private",
            "Import updated workflow JSON after pipeline changes",
            "Use Execute Command only for local project scripts unless reviewed",
        ],
    }


def analyze_agent_scripts() -> Dict[str, Any]:
    """Analyze agent scripts for private local readiness."""
    agents = []
    
    for script_file in SCRIPTS_DIR.glob("*.py"):
        if script_file.name == "captain_connectivity_.py":
            continue  # Don't analyze ourselves
        
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Private-first agents should prefer local files and shared loaders.
            has_external_egress = bool(re.search(
                r"\b(import\s+requests|from\s+urllib|import\s+urllib|import\s+socket|import\s+httpx|import\s+aiohttp)\b",
                content,
                re.IGNORECASE,
            ))
            has_secret_like_text = bool(re.search(
                r"(api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*=",
                content,
                re.IGNORECASE,
            ))
            has_main_guard = 'if __name__ == "__main__"' in content
            uses_shared_loader = "geomolecular_data" in content or script_file.name in {
                "geomolecular_data.py",
                "run_pipeline.py",
                "create_excel_template.py",
            }
            
            readiness_features = []
            if not has_external_egress:
                readiness_features.append("local-only")
            if not has_secret_like_text:
                readiness_features.append("secret-free")
            if has_main_guard:
                readiness_features.append("standalone-runnable")
            if uses_shared_loader:
                readiness_features.append("shared-data-path")
            
            agent_score = 0
            if not has_external_egress:
                agent_score += 35
            if not has_secret_like_text:
                agent_score += 30
            if has_main_guard:
                agent_score += 20
            if uses_shared_loader:
                agent_score += 15
            
            agents.append({
                "name": script_file.stem,
                "features": readiness_features,
                "score": agent_score,
                "has_external_egress": has_external_egress,
                "has_secret_like_text": has_secret_like_text,
                "has_main_guard": has_main_guard,
                "uses_shared_loader": uses_shared_loader,
            })
            
        except Exception as e:
            agents.append({
                "name": script_file.stem,
                "error": str(e),
                "score": 0
            })
    
    if not agents:
        return {
            "component": "agent_scripts",
            "status": "no_agents",
            "score": 0,
            "notes": "No agent scripts found",
            "agents": []
        }
    
    avg_score = sum(a.get('score', 0) for a in agents) / len(agents)
    if avg_score >= 90:
        status = "private_local_ready"
    elif avg_score >= 75:
        status = "mostly_ready"
    else:
        status = "review_needed"
    
    return {
        "component": "agent_scripts",
        "status": status,
        "score": int(avg_score),
        "notes": f"Average private-local readiness: {avg_score:.1f}%",
        "agents": agents,
        "opportunities": [
            "Keep agents local-only unless external egress is explicitly reviewed",
            "Use shared workbook loaders for every agent that reads project data",
            "Add tests around generated reports before expanding automation",
        ],
    }


def recommend_networks() -> Dict[str, Any]:
    """Recommend networks for task diversification."""
    recommendations = {
        "local_networks": [
            {"name": "Local File System", "purpose": "Data persistence and sharing between agents", "score": 95},
            {"name": "Local APIs", "purpose": "Inter-agent communication", "score": 80},
            {"name": "SQLite/PostgreSQL", "purpose": "Structured data storage", "score": 90}
        ],
        "cloud_networks": [
            {"name": "Private GitHub", "purpose": "Version control, private issue packets, and controlled PRs", "score": 100},
            {"name": "Private n8n", "purpose": "Workflow automation with private webhook URLs and local commands", "score": 90},
            {"name": "OpenAI API", "purpose": "AI processing with tiktoken", "score": 90},
            {"name": "Private Cloud Compute", "purpose": "Scalable processing only after data-egress review", "score": 70}
        ],
        "diversification_strategy": {
            "primary": "Local-first for data sovereignty",
            "secondary": "Private GitHub for durable cross-project coordination",
            "backup": "n8n automation only when workflow exports remain secret-free"
        }
    }
    
    return {
        "component": "network_recommendations",
        "status": "analyzed",
        "score": 100,  # Recommendations are always available
        "recommendations": recommendations
    }


def calculate_overall_score(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate the overall connectivity opportunity score."""
    if not components:
        return {"overall_score": 0, "status": "no_data"}
    
    scores = [c.get('score', 0) for c in components if 'score' in c]
    if not scores:
        return {"overall_score": 0, "status": "no_scores"}
    
    overall_score = sum(scores) / len(scores)
    
    if overall_score >= 90:
        status = "excellent_connectivity"
        message = "Private coordination is in strong condition."
    elif overall_score >= 70:
        status = "good_connectivity"
        message = "Core coordination is working; review the lower-scoring surfaces."
    elif overall_score >= 50:
        status = "moderate_connectivity"
        message = "Connectivity exists, but privacy or automation gaps need attention."
    else:
        status = "poor_connectivity"
        message = "Coordination is not ready for reliable private automation."
    
    return {
        "overall_score": round(overall_score, 1),
        "status": status,
        "message": message,
        "components_analyzed": len(components),
        "average_component_score": round(sum(scores) / len(scores), 1)
    }


def render_report(analysis: Dict[str, Any]) -> str:
    """Render the connectivity report in Markdown."""
    lines = [
        "# Captain Connectivity Report",
        "",
        "Type: `agent-report`",
        "Agent: `captain-connectivity-agent`",
        "",
        "## Executive Summary",
        "",
        f"**Overall Connectivity Score: {analysis['overall']['overall_score']}%**",
        "",
        f"*{analysis['overall']['message']}*",
        "",
        f"- Components analyzed: {analysis['overall']['components_analyzed']}",
        f"- Average component score: {analysis['overall']['average_component_score']}%",
        f"- Privacy policy: {analysis['privacy_policy']}",
        "",
        "## Component Analysis",
        "",
    ]
    
    for component in analysis['components']:
        lines.append(f"### {component['component'].replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"- **Status:** {component.get('status', 'unknown')}")
        lines.append(f"- **Score:** {component.get('score', 0)}%")
        lines.append(f"- **Notes:** {component.get('notes', 'No notes')}")
        lines.append("")
        
        if 'workflows' in component and component['workflows']:
            lines.append("**Workflows:**")
            for wf in component['workflows'][:5]:  # Limit to 5
                wf_name = wf.get('name', 'Unknown')
                wf_score = wf.get('api_nodes', 0)
                private_ready = "private-ready" if wf.get("private_ready") else "review-needed"
                version_id = wf.get("version_id", "unknown-version")
                lines.append(f"- {wf_name}: {wf_score} API connections, {private_ready}, `{version_id}`")
            if len(component['workflows']) > 5:
                lines.append(f"- ... and {len(component['workflows']) - 5} more")
            lines.append("")
        
        if 'agents' in component and component['agents']:
            lines.append("**Agents:**")
            for agent in component['agents']:
                agent_name = agent.get('name', 'Unknown')
                agent_score = agent.get('score', 0)
                features = ', '.join(agent.get('features', []))
                lines.append(f"- {agent_name}: {agent_score}% ({features or 'no features'})")
            lines.append("")
        
        if 'opportunities' in component and component['opportunities']:
            lines.append("**Next Checks:**")
            for opp in component['opportunities']:
                lines.append(f"- {opp}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Network Recommendations
    if 'network_recommendations' in analysis:
        rec = analysis['network_recommendations']
        lines.append("## Network Recommendations")
        lines.append("")
        lines.append("### Local Networks")
        for net in rec['recommendations']['local_networks']:
            lines.append(f"- **{net['name']}**: {net['purpose']} (Score: {net['score']}%)")
        lines.append("")
        
        lines.append("### Cloud Networks")
        for net in rec['recommendations']['cloud_networks']:
            lines.append(f"- **{net['name']}**: {net['purpose']} (Score: {net['score']}%)")
        lines.append("")
        
        lines.append("### Diversification Strategy")
        strat = rec['recommendations']['diversification_strategy']
        lines.append(f"- **Primary:** {strat['primary']}")
        lines.append(f"- **Secondary:** {strat['secondary']}")
        lines.append(f"- **Backup:** {strat['backup']}")
        lines.append("")
    
    lines.append("## Captain's Log")
    lines.append("")
    lines.append("Private-first rule: local files, private GitHub coordination, private n8n webhooks, and no public knowledge export without explicit approval.")
    lines.append("Run `python scripts/run_pipeline.py` after workbook, workflow, or agent changes so this report stays current.")
    lines.append("")
    
    return "\n".join(lines)


def main() -> None:
    """Main function to run the Captain Connectivity analysis."""
    print("Captain Connectivity: analyzing privacy, n8n, and agent readiness...")
    
    # Analyze all components
    components = [
        check_privacy_posture(),
        check_tiktoken_status(),
        analyze_n8n_workflows(),
        analyze_agent_scripts(),
        recommend_networks()
    ]
    
    # Calculate overall score
    overall = calculate_overall_score(components)
    
    analysis = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "privacy_policy": "private-first; no public publication of repo, webhook URLs, reports, or external-drive knowledge without explicit approval",
        "overall": overall,
        "components": components,
        "privacy_posture": components[0],
        "network_recommendations": components[-1]  # Last component is recommendations
    }
    
    # Ensure report directory exists
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write JSON report
    json_path = REPORT_DIR / "captain-connectivity-report.json"
    json_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    
    # Write Markdown report
    md_path = REPORT_DIR / "captain-connectivity-report.md"
    md_path.write_text(render_report(analysis), encoding="utf-8")
    
    print(f"Report written to {md_path}")
    print(f"Overall Connectivity Score: {overall['overall_score']}% - {overall['message']}")


if __name__ == "__main__":
    main()
