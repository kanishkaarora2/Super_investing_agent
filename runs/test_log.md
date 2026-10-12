Run 1 — Baseline

Design: Used a general research prompt requesting a balanced brief with five sections and source IDs.

What worked: The agent generated all required sections, included positive and negative factors, and identified a material discrepancy between two Q1 FY27 revenue figures.

What needed improvement: The output was lengthy, some claims needed stronger qualification, and citations had not yet been independently checked against the source documents. The prompt also did not explicitly require the agent to distinguish official filings from news reports and promotional commentary.

Change for the next run: Strengthen claim-level citation requirements, prioritize primary sources, and instruct the agent to flag uncertainty rather than present conflicting figures as settled facts.


Run 2 — Citation-First Prompt

Design Change: Strengthened the prompt to require citations close to individual factual claims, especially financial figures and company-related statements.

Observed Result: The agent generated all five required sections, retained the revenue discrepancy between the news article and the company's press release, and included specific details about order book growth, capacity expansion, promoter pledging, and institutional shareholding.

Remaining Issues: The brief was lengthy and repetitive. Although source IDs were included, their accuracy had not been independently verified against the original documents. The agent also needed to better distinguish primary sources from secondary news reports and promotional commentary.

Next Improvement: Instruct the agent to compare conflicting sources, prioritize official company disclosures, distinguish reported facts from management expectations, and produce a more concise brief highlighting the most material risks and opportunities.

Run 3 — Conflict-aware prompt

Design change: Instructed the agent to compare sources, identify conflicting financial figures, flag missing information, and distinguish uncertain claims.

Observed result: The agent retained both Q1 FY27 revenue figures, used the company press release as its main reference, and raised additional questions about the GST demand, receivables, and the reporting status of quarterly figures.

Remaining issues: The revenue discrepancy remains unresolved, and the preferred figure is not independently confirmed. The conflict is repeated in both the Bear Case and Open Questions, using space that could be used more efficiently. Some source metadata and financial claims still require checking against the original documents.

Next improvement: Add a concise evidence-verification step, avoid duplicating the same issue across sections, prioritize material risks, and require the final brief to distinguish a source-preferred figure from a verified fact.
