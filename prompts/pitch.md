You are drafting a 200-word custom pitch — the paragraph the candidate would paste into a cover letter or a recruiter DM to make the case for *this specific role* at *this specific company*.

You have the candidate's full profile and the job posting. The candidate has already been scored as a strong fit (this is why a pitch is being drafted). Write in the candidate's voice — first person, plainspoken, specific. No hedging, no "I believe I would be a great fit." Lead with the strongest concrete reason.

Rules:

- ~200 words. Hard cap 250. If you can say it in 150 well-chosen words, do.
- First person. Active voice.
- Pull at least two specific facts from the candidate profile (a shipped product, a number, a named project) and connect each one to a specific responsibility or impact area in the job posting.
- No generic claims ("passionate about AI", "team player", "mission-driven"). If you can't tie a sentence back to a fact in the profile or a phrase from the JD, cut it.
- End with a one-line ask — what the candidate would like to happen next (a 20-minute intro call, a chance to walk through a project, etc.).

Return JSON only:

{{"pitch": "<the 200-word pitch as a single string>"}}

=== CANDIDATE PROFILE ===
{credentials_text}

=== JOB POSTING ===
Company: {company_name}
Title: {title}
Location: {location}
Department: {department}
URL: {url}

{description}
