def generate(title, translation=None, analysis=None, links=None):
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Overview")
    lines.append("This document summarizes translation output and analysis insights.")
    if translation:
        lines.append("## Translated Code")
        lines.append("```")
        lines.append(translation)
        lines.append("```")
    if analysis:
        lines.append("## Dependencies")
        for d in analysis.get("dependencies", []):
            lines.append(f"- {d}")
        lines.append("## Complexity")
        lines.append(f"- {analysis.get('complexity')}")
        lines.append("## Potential Vulnerabilities")
        for v in analysis.get("vulnerabilities", []):
            lines.append(f"- {v}")
    if links:
        lines.append("## References")
        lines.append(f"- URLs: {links.get('urls')}")
        lines.append(f"- API Paths: {links.get('api_paths')}")
        lines.append(f"- IPs: {links.get('ips')}")
        lines.append(f"- Emails: {links.get('emails')}")
    lines.append("")
    lines.append("## Usage Example")
    lines.append("Refer to the translated code block above and adapt to your project structure.")
    return "\n".join(lines)
