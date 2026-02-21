def markdown_summary(title, translation=None, analysis=None, links=None):
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    if translation is not None:
        lines.append("## Translation")
        lines.append("```")
        lines.append(translation)
        lines.append("```")
    if analysis is not None:
        lines.append("## Analysis")
        lines.append(f"- Dependencies: {analysis.get('dependencies')}")
        lines.append(f"- Complexity: {analysis.get('complexity')}")
        lines.append(f"- Vulnerabilities: {analysis.get('vulnerabilities')}")
    if links is not None:
        lines.append("## Links")
        lines.append(f"- URLs: {links.get('urls')}")
        lines.append(f"- API Paths: {links.get('api_paths')}")
        lines.append(f"- IPs: {links.get('ips')}")
        lines.append(f"- Emails: {links.get('emails')}")
    return "\n".join(lines)
