def get_contract_analysis_prompt(text: str) -> str:
    return f"""Analyze the following document section summaries extracted from a contract.

First, determine the contract type, then provide a comprehensive analysis.

Respond ONLY with a valid JSON object using this exact structure — no extra text or markdown:
{{
  "contract_type": "<type of contract e.g. Employment, NDA, Sales, Lease>",
  "overall_score": <integer 1-100, representing overall favorability>,
  "summary": "<comprehensive summary of the contract including key terms and conditions>",
  "risks": [
    {{"risk": "<risk title>", "risk_details": "<brief explanation>", "severity": "LOW|MEDIUM|HIGH"}}
  ],
  "opportunities": [
    {{"opportunity": "<opportunity title>", "opportunity_details": "<brief explanation>", "impact": "LOW|MEDIUM|HIGH"}}
  ],
  "recommendations": ["<recommendation>"],
  "key_clauses": ["<clause>"],
  "legal_compliance": "<assessment of legal compliance>",
  "negotiation_points": ["<point>"],
  "contract_duration": "<duration or null>",
  "termination_conditions": "<summary of termination conditions or null>",
  "financial_terms": {{
    "description": "<overview of general financial terms>",
    "details": ["<detail>"]
  }},
  "compensation_structure": {{
    "base_salary": "<value or null>",
    "bonuses": "<value or null>",
    "equity": "<value or null>",
    "other_benefits": "<value or null>"
  }},
  "performance_metrics": ["<metric>"]
}}

Requirements:
- Provide at least 10 risks and 10 opportunities
- overall_score must be an integer between 1 and 100
- Use null (not "null") for missing optional fields
- financial_terms and compensation_structure are null if not applicable

Document section summaries:
{text}"""