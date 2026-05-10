from typing import Literal, Optional
from pydantic import BaseModel


class RiskItem(BaseModel):
    risk: str
    risk_details: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]


class OpportunityItem(BaseModel):
    opportunity: str
    opportunity_details: str
    impact: Literal["LOW", "MEDIUM", "HIGH"]


class FinancialTerms(BaseModel):
    description: str
    details: list[str]


class CompensationStructure(BaseModel):
    base_salary: Optional[str] = None
    bonuses: Optional[str] = None
    equity: Optional[str] = None
    other_benefits: Optional[str] = None


class ContractInsights(BaseModel):
    contract_type: str
    overall_score: int
    summary: str
    risks: list[RiskItem]
    opportunities: list[OpportunityItem]
    recommendations: list[str]
    key_clauses: list[str]
    legal_compliance: str
    negotiation_points: list[str]
    contract_duration: Optional[str] = None
    termination_conditions: Optional[str] = None
    financial_terms: Optional[FinancialTerms] = None
    compensation_structure: Optional[CompensationStructure] = None
    performance_metrics: list[str] = []


class ContractAnalysisResponse(BaseModel):
    document_id: str
    insights: ContractInsights