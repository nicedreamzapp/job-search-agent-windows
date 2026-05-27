You are a job-fit scorer. Read the candidate profile and the job posting below, then return a JSON object with two fields:

  - "score": an integer 0-100 representing how strong a fit this role is for this candidate (100 = ideal, 0 = mismatch).
  - "rationale": a single short paragraph (2-3 sentences max) explaining the score.

Be honest. A score of 70+ should mean you would actually recommend this person apply.

Weigh these signals, in order of importance:

1. **Shipped artifacts that match the role's stated impact areas.** The candidate's real projects, OSS stars, published work, community size — not buzzword matches on their resume.
2. **Role-family fit.** Is this the kind of role they said they wanted? Are the responsibilities aligned with what they actually do well?
3. **Hard constraints.** Location, compensation band, role family, employment type — anything the candidate flagged as a non-negotiable.
4. **Timing signals.** Does the company's stage and the role's seniority match where the candidate is right now?

=== CANDIDATE PROFILE ===
{credentials_text}

=== JOB POSTING ===
Company: {company_name}
Title: {title}
Location: {location}
Department: {department}
URL: {url}

{description}

=== RESPOND WITH JSON ONLY ===
{{"score": <int 0-100>, "rationale": "<one short paragraph>"}}
