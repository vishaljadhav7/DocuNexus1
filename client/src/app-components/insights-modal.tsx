import { X } from "lucide-react";

interface InsightsModalProps {
  insights: Record<string, any>;
  onClose: () => void;
}

const severityColor = (s: string) => {
  if (s === "HIGH") return "text-red-600 bg-red-50 border-red-200";
  if (s === "MEDIUM") return "text-amber-600 bg-amber-50 border-amber-200";
  return "text-green-600 bg-green-50 border-green-200";
};

const impactColor = (i: string) => {
  if (i === "MEDIUM") return "text-blue-600 bg-blue-50 border-blue-200";
  return "text-slate-600 bg-slate-50 border-slate-200";
};

export function InsightsModal({ insights, onClose }: InsightsModalProps) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
    >
      <div
        className="bg-card border border-border rounded-2xl shadow-2xl w-full max-w-2xl max-h-[85vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between p-5 border-b border-border">
          <div>
            <h2 className="text-lg font-semibold text-foreground">Contract Insights</h2>
            <p className="text-sm text-muted-foreground mt-0.5">
              Overall Score:{" "}
              <span className="font-bold text-foreground">{insights.overall_score}/100</span>
              {" · "}
              {insights.contract_type} · {insights.contract_duration}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="overflow-y-auto p-5 space-y-6 flex-1">

          {/* Summary */}
          <section>
            <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Summary</h3>
            <p className="text-sm text-foreground leading-relaxed">{insights.summary}</p>
          </section>

          {/* Financial Terms */}
          {insights.financial_terms && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Financial Terms
              </h3>
              <p className="text-sm text-foreground mb-2">{insights.financial_terms.description}</p>
              <ul className="space-y-1">
                {insights.financial_terms.details?.map((d: string, i: number) => (
                  <li key={i} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-muted-foreground mt-0.5">·</span>
                    {d}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Risks */}
          {insights.risks?.length > 0 && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Risks</h3>
              <div className="space-y-2">
                {insights.risks.map((r: any, i: number) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-xl border border-border bg-muted/30">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full border mt-0.5 ${severityColor(r.severity)}`}>
                      {r.severity}
                    </span>
                    <div>
                      <p className="text-sm font-medium text-foreground">{r.risk}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{r.risk_details}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Opportunities */}
          {insights.opportunities?.length > 0 && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Opportunities
              </h3>
              <div className="space-y-2">
                {insights.opportunities.map((o: any, i: number) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-xl border border-border bg-muted/30">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full border mt-0.5 ${impactColor(o.impact)}`}>
                      {o.impact}
                    </span>
                    <div>
                      <p className="text-sm font-medium text-foreground">{o.opportunity}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{o.opportunity_details}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Key Clauses */}
          {insights.key_clauses?.length > 0 && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Key Clauses</h3>
              <ul className="space-y-1">
                {insights.key_clauses.map((c: string, i: number) => (
                  <li key={i} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-primary mt-0.5">·</span>
                    {c}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Recommendations */}
          {insights.recommendations?.length > 0 && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Recommendations
              </h3>
              <ul className="space-y-1">
                {insights.recommendations.map((r: string, i: number) => (
                  <li key={i} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-primary mt-0.5">·</span>
                    {r}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Negotiation Points */}
          {insights.negotiation_points?.length > 0 && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Negotiation Points
              </h3>
              <ul className="space-y-1">
                {insights.negotiation_points.map((n: string, i: number) => (
                  <li key={i} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-primary mt-0.5">·</span>
                    {n}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Legal Compliance */}
          {insights.legal_compliance && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Legal Compliance
              </h3>
              <p className="text-sm text-foreground">{insights.legal_compliance}</p>
            </section>
          )}

          {/* Termination Conditions */}
          {insights.termination_conditions && (
            <section>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Termination Conditions
              </h3>
              <p className="text-sm text-foreground">{insights.termination_conditions}</p>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}