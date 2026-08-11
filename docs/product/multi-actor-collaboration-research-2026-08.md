# LifeOS — Multi-Actor / Collaboration Deep Research

**Date:** 11 August 2026  
**Status:** Product research / external evidence  
**Scope:** challenge, validate and expand the findings of `multi-actor-collaboration-discovery-simulation-2026-08.md` through external research across multiple independent evidence families.  
**Relationship to simulation:** this document does not rewrite the simulation. It is a second, independent evidence source used to identify confirmations, contradictions, missing needs, weak assumptions and product risks.

---

# 1. Purpose

The earlier simulation deliberately started from real-life actors and scenarios without looking at competitors or academic literature first. This research performs the opposite complementary exercise: examine decades of CSCW/HCI research, current standards, regulation, specialist-domain models and existing products to determine whether the simulated findings survive contact with external evidence.

The research question is not:

> Which collaboration features should LifeOS copy?

It is:

> What is already known about how people coordinate, share responsibility, establish common ground, protect privacy, manage shared resources and recover from collaboration breakdowns — and what does that evidence imply for the hypotheses discovered by the LifeOS simulation?

This remains product evidence. It does not define implementation architecture, database schema, exact authorization models, UI, release scope or pricing.

---

# 2. Research method

The research intentionally spans several evidence families because multi-user coordination is a socio-technical problem and no single literature or product category covers it adequately.

Evidence families examined:

1. foundational CSCW / groupware research;
2. coordination theory and dependency management;
3. common ground, awareness and notification research;
4. shared calendars and temporal privacy;
5. household and family coordination;
6. invisible domestic / cognitive labor;
7. social events, invitations and real attendance;
8. work scheduling, shifts, substitution and fairness;
9. caregiving and family care coordination;
10. healthcare consent, care teams and specialist-system boundaries;
11. education and multi-stakeholder agency;
12. shared expenses and group financial coordination;
13. external / non-member participation and cross-boundary collaboration;
14. privacy, consent and data minimization;
15. fine-grained and relationship-based authorization concepts;
16. current product patterns across calendar, family, work and care tools;
17. AI-mediated coordination and risks of automation.

Evidence hierarchy used in interpretation:

- **high confidence:** repeated findings across established research and/or authoritative standards;
- **strong practical evidence:** current mature products or official platform documentation showing recurring design patterns at scale;
- **domain evidence:** specialist standards and research demonstrating needs in a particular context;
- **emerging evidence:** recent studies or products that are promising but should not be generalized prematurely.

A product implementing a feature is not treated as proof that the feature is correct. Likewise, one study is not treated as proof of universality.

---

# 3. Foundational CSCW: collaboration is not an individual feature multiplied by N

## 3.1 Groupware has failure modes that single-user software does not

Jonathan Grudin's foundational CSCW work argued that groupware often fails for organizational and social reasons rather than technical ones. One central problem is **disparity between work and benefit**: the people required to enter data, maintain state or change behavior may not be the same people who receive the largest benefit.

This is highly relevant to LifeOS. A collaboration feature can be locally rational for the organizer while imposing administrative work on every participant.

Example:

- organizer benefits from perfect RSVP state;
- every guest is asked to create an account, expose availability, maintain preferences and acknowledge every change;
- the organizer's coordination burden decreases while the group's total burden increases.

That can still be a product failure.

**Implication for the simulation:** its `non-LifeOS participant` and `LifeOS should not add process to tiny situations` findings are strongly reinforced.

**Additional principle discovered from research:** evaluate **distribution of coordination cost**, not only total feature capability.

Sources:

- Jonathan Grudin, *Why CSCW Applications Fail: Problems in the Design and Evaluation of Organizational Interfaces*, CSCW 1988: https://doi.org/10.1145/62266.62273
- Jonathan Grudin, *Groupware and Social Dynamics: Eight Challenges for Developers*, Communications of the ACM 1994: https://www.microsoft.com/en-us/research/?p=357080

## 3.2 Critical mass matters

Groupware adoption literature repeatedly identifies critical-mass effects. A collaboration system can have excellent functionality but little value when only part of a group participates, or when different organizational homes use incompatible tools.

A study of groupware adoption in distributed organizations found that conflicting local standards, resource constraints and loyalties to home organizations shape adoption. Collaboration crosses boundaries that software ownership does not automatically erase.

**Implication:** LifeOS must treat partial adoption, provider boundaries and heterogeneous tools as the normal case, not as migration failures.

Source:

- *Groupware adoption in a distributed organization: transporting and transforming technology through social worlds*: https://www.sciencedirect.com/science/article/abs/pii/S1471772704000405

---

# 4. Coordination theory: the core problem is managing dependencies

Malone and Crowston's coordination theory defines coordination as managing dependencies among activities. Their work identifies recurring dependency families such as:

- shared resources;
- producer/consumer relationships;
- simultaneity constraints;
- task/subtask dependencies;
- assignment and prerequisite relationships.

This maps closely to the simulation, where apparently unrelated scenarios repeatedly produced:

- person A must act before person B;
- several people compete for one resource;
- one person's commitment changes another person's feasible plan;
- one person produces information or an artifact needed by another;
- several participants must be available simultaneously.

**Strong confirmation:** the simulation's cross-domain recurrence of responsibilities, prerequisites, shared resources and temporal coordination is consistent with established coordination theory rather than being an artifact of the invented scenarios.

**Important extension:** multi-user discovery should classify not only *what object is shared*, but **what dependency is being managed**.

Sources:

- Malone & Crowston, *What is coordination theory and how can it help design cooperative work systems?*, CSCW 1990: https://doi.org/10.1145/99332.99367
- Malone & Crowston, *The Interdisciplinary Study of Coordination*, ACM Computing Surveys 1994: https://ccs.mit.edu/papers/CCSWP157.html
- Crowston, *A Coordination Theory Approach to Organizational Process Design*, Organization Science 1997: https://doi.org/10.1287/orsc.8.2.157

---

# 5. Common ground: sharing a fact is not the same as sharing understanding

Herbert Clark's work on common ground and grounding distinguishes information transmission from establishing that information has become mutually understood.

This difference matters throughout LifeOS:

```text
message sent != message seen
message seen != understood
understood != accepted
accepted != acted upon
planned != actually happened
```

Healthcare collaboration studies similarly show that weak common ground can create coordination failures even when information exists somewhere in the system.

**Strong confirmation:** the simulation's separation of proposal, acknowledgement, confirmation and actual outcome is well founded.

**New refinement:** LifeOS should not treat acknowledgement purely as a notification mechanic. In some contexts it is a **grounding mechanism**: evidence that a relevant participant has incorporated a change into shared understanding.

Sources:

- Herbert H. Clark research on common ground and grounding: https://web.stanford.edu/~clark/research.html
- *Describing the Clinical Communication Space through a Model of Common Ground*: https://pmc.ncbi.nlm.nih.gov/articles/PMC3041298/

---

# 6. Awareness and notification: enough context to coordinate, not a firehose

Collaborators need awareness of intentions, actions and results, but research distinguishes useful activity awareness from raw notification volume.

Carroll et al. found that simple notifications do not adequately support persistent complex collaborative activity; users need enough activity context to interpret what changed and what it means.

Other research on awareness displays shows that more visibility is not automatically better. Awareness can reduce disruptive coordination attempts, but its effectiveness depends on social incentives and relevance.

**Implications:**

- `notify everybody about every change` is not a sound collaboration model;
- change propagation should be scoped by relevance;
- users need meaningful deltas and implications, not just event logs;
- awareness should reduce coordination work rather than create a new review workload.

This strengthens the simulation's concept of affected-participant propagation, but adds a guardrail against notification-driven overengineering.

Sources:

- Carroll et al., *Notification and awareness: synchronizing task-oriented collaborative activity*: https://www.sciencedirect.com/science/article/pii/S1071581903000247
- *Awareness Displays and Social Motivation for Coordinating Communication*: https://doi.org/10.1287/isre.1080.0175
- Shah, *Effects of awareness on coordination in collaborative information seeking*: https://doi.org/10.1002/asi.22819

---

# 7. Shared calendars: availability is socially sensitive information

## 7.1 Calendar privacy is not only event-content privacy

Leysia Palen's study of groupware calendar systems identified several distinct privacy concerns:

- private event information;
- socially sensitive information involving other people;
- organizationally sensitive information;
- judgments about how a person allocates time;
- loss of control over access to one's time.

The research also documents practical privacy strategies such as full detail, free/busy only, nothing, or deliberately context-limited entries.

This directly validates one of the strongest simulation findings:

> coordination often needs the consequence of private context, not the private context itself.

For example `unavailable 14:00–16:00` can be sufficient; `oncology appointment` is not required to schedule dinner or project work.

Source:

- Palen, *Social, Individual & Technological Issues for Groupware Calendar Systems*, CHI 1999: https://doi.org/10.1145/302979.302982

## 7.2 Current calendar products converge on graduated disclosure

Outlook supports multiple visibility levels including busy-only, title/location and full details, with additional editor/delegate authority. Private calendar items can remain hidden even from delegates unless explicitly permitted.

Google Calendar allows invitations to people without Google Calendar and supports Yes/No/Maybe RSVP states.

These are practical signals that:

- availability and detail are different permissions;
- viewing and acting-on-behalf-of are different authorities;
- participant state is richer than membership;
- non-platform participants are common enough to support explicitly.

Sources:

- Microsoft Outlook calendar sharing: https://support.microsoft.com/en-us/outlook/sharing/share-an-outlook-calendar-as-view-only-with-others
- Microsoft Outlook delegation: https://support.microsoft.com/en-us/outlook/sharing/about-delegates-allow-someone-to-manage-your-mail-and-calendar-in-outlook
- Google Calendar guest invitations: https://support.google.com/calendar/answer/37161

---

# 8. Family calendars: awareness often matters more than direct coordination

Research on family calendars is especially relevant because family life mixes high trust, recurring coordination, unequal responsibilities and personal privacy.

Neustaedter, Brush and Greenberg studied family coordination and found that calendars often act primarily as **awareness artifacts**. Families coordinate through social practices around the calendar; the calendar itself does not replace those practices.

Studies also identified different calendaring topologies: some households revolve around one primary scheduler, others distribute responsibility more broadly.

A field trial of the LINC digital family calendar found that successful adoption depended on fitting existing routines rather than forcing a new workflow.

**Implications:**

- LifeOS should not assume every household wants symmetric participation;
- a `family workspace` should not imply everybody performs the same management work;
- tools should expose and optionally redistribute coordination, not pretend social structure is already equal;
- adoption should support existing working practices first, then offer improvements.

Sources:

- Neustaedter, Brush & Greenberg, *The Calendar is Crucial: Coordination and Awareness through the Family Calendar*, TOCHI 2009: https://doi.org/10.1145/1502800.1502806
- Microsoft Research, *LINC-ing the Family*: https://www.microsoft.com/en-us/research/publication/linc-ing-the-family-the-participatory-design-of-an-inkable-family-calendar/
- *A digital family calendar in the home: lessons from field trials of LINC*: https://graphicsinterface.org/proceedings/gi2007/gi2007-27/

---

# 9. Household coordination has hidden work that task lists do not capture

A major expansion beyond the original simulation comes from recent research on domestic mental load.

The 2026 CHI paper *The Domestic Operating System* reports that digital tools support household cognitive work but often focus on visible outputs such as chores and plans while leaving hidden coordination labor poorly represented.

Invisible household work includes things like:

- noticing that something will soon be needed;
- remembering deadlines and preferences;
- anticipating conflicts;
- deciding when another person must be reminded;
- monitoring whether delegated work actually happened;
- maintaining family knowledge and social relationships.

Related research finds persistent asymmetries in mental labor, including planning and emotional monitoring. Italian research published in 2025–2026 similarly identifies cognitive and emotional mental-load gaps inside couples.

**This qualifies the simulation.** A shared task or explicit assignee does not automatically redistribute responsibility. The person who creates, decomposes, monitors and repairs the task may still carry most of the cognitive burden.

**New cross-case need:** distinguish **execution work** from **coordination / stewardship work** when evaluating whether LifeOS actually reduces burden.

Sources:

- Frampton, Gould & Cox, *The Domestic Operating System: An Empirical Investigation of Digital Technology and Hidden Work in the Home*, CHI 2026: https://doi.org/10.1145/3772318.3791167
- Ciciolla & Luthar, *Invisible Household Labor and Ramifications for Adjustment*: https://doi.org/10.1007/S11199-018-1001-X
- Barigozzi et al., *Beyond Time: Unveiling the Invisible Burden of Mental Load*: https://amsacta.unibo.it/id/eprint/8356/

---

# 10. AI in family coordination can reallocate burden rather than remove it

Recent research and commentary around AI family assistants raise a useful warning: automation can create new data-entry, oversight and exception-management work. A system may make household output more efficient while increasing the responsibility of the person who configures and supervises it.

A 2026 study of parent collaboration in family education distinguishes physical, cognitive and emotional labor and argues for relationship-sensitive intervention rather than treating automation as universal burden reduction.

**Implications for LifeOS AI:**

- measure whether AI reduces *coordination burden*, not only clicks;
- avoid making one household member the permanent `AI administrator`;
- proposed delegation should not silently reinforce existing unequal responsibility;
- relationship maintenance can be a legitimate optimization target alongside task throughput.

Sources:

- Wang et al., *Division of Labor and Collaboration Between Parents in Family Education* (2026): https://arxiv.org/abs/2602.10501
- Frampton et al., CHI 2026, above.

---

# 11. Social invitations: online acceptance is not actual participation

Research on online event invitations found that online participation decisions and offline attendance differ. Attendance depends on event type, relationship strength, communication medium and social context.

This directly reinforces the simulation's `planned participation != actual participation` distinction.

Current Google Calendar also exposes `Yes / No / Maybe`, demonstrating the practical importance of non-binary commitment.

**Implication:** RSVP is an intention state, not evidence of attendance.

Source:

- Huang, Wang & Yuan, *De-Virtualizing Social Events: Understanding the Gap between Online and Offline Participation for Event Invitations*: https://arxiv.org/abs/1311.0663

---

# 12. Shift scheduling: fairness is not reducible to optimization

Shift scheduling is a strong stress test because it combines availability, preferences, authority, fairness, substitution and resource capacity.

Research on collaborative healthcare shift scheduling found that workers may agree abstractly on equality but resolve concrete conflicts by negotiating the importance of individual needs. Transparency, team spirit and perceived procedural fairness matter.

A nine-month study of worker-centered self-scheduling found that social standing and conflict-avoidance practices affect how people use collaborative scheduling tools. Purely competitive allocation can damage social practices.

Microsoft Teams Shifts currently implements a multi-stage distinction:

```text
worker requests swap
→ coworker accepts/declines
→ manager approves/denies
→ schedule changes
```

It also distinguishes open shifts, offers, time-off requests, pending requests and approved state. Its current documentation additionally provides privacy controls for why colleagues are absent and how much shift detail others can see.

**Strong confirmation:** proposal, recipient acceptance, authority approval and canonical schedule mutation should remain distinct concepts.

**New guardrail:** algorithmically `optimal` coordination can be experienced as unfair if social negotiation and procedural transparency are lost.

Sources:

- Uhde et al., *Fairness and Decision-making in Collaborative Shift Scheduling Systems*: https://arxiv.org/abs/2001.09755
- Uhde et al., *Design and Appropriation of Computer-supported Self-scheduling Practices in Healthcare Shift Work*: https://arxiv.org/abs/2102.02132
- Microsoft Teams Shifts swap/offer workflow: https://support.microsoft.com/en-us/teams/free/request-open-shifts-swap-or-offer-shifts-in-shifts
- Microsoft Teams Shifts privacy controls: https://support.microsoft.com/en-US/Teams/free/configure-settings-for-your-team-s-schedule-in-shifts

---

# 13. Caregiving: the cared-for person must not disappear behind the care network

Caregiving research consistently shows that coordination is not simply family project management. It combines:

- information transfer;
- high emotional load;
- unequal expertise;
- changing capacity;
- clinical/professional authority;
- family participation;
- privacy and consent;
- uncertainty about what actually happened.

Research on family caregivers in severe conditions specifically identifies information, coordination and social challenges when relatives mediate between patient and health services.

Recent dementia-care HCI research warns that reminder logs are context-dependent. A missed or acknowledged prompt cannot automatically be interpreted as a reliable behavioral truth because household participation, accessibility issues and technical failures change what the data means.

**Strong confirmation:** the simulation's preservation of uncertainty and source provenance in caregiving is essential.

**Additional insight:** evidence produced by coordination tools should be interpreted as **situated evidence**, not neutral sensing.

Sources:

- di Fiore et al., *Understanding how Software Can Support the Needs of Family Caregivers for Patients with Severe Conditions*: https://arxiv.org/abs/1701.07607
- Lai & Mihailidis, *Remindful: Designing Reminder Systems for Caregiver Interpretation in Dementia Care* (2026): https://arxiv.org/abs/2604.19574

---

# 14. Healthcare standards validate dynamic teams, roles, consent and provenance

## 14.1 Care teams are dynamic and role-specific

HL7 FHIR defines a CareTeam as people and organizations who plan to participate in coordination and delivery of care. The standard explicitly allows patients, practitioners, family members, guardians and other caregivers, and notes that team composition can change over time.

FHIR also distinguishes CareTeam from a generic Group: the former carries participant and role meaning around care.

This supports the simulation's separation between `group membership` and `participation in a particular shared context`.

Source:

- HL7 FHIR CareTeam: https://hl7.org/fhir/careteam.html

## 14.2 Consent is scoped by recipient, role, purpose and period

FHIR Consent models permission or denial for identified recipients or recipient roles to perform actions within a policy context, for specific purposes and periods.

This is important evidence that `shared with caregiver` is too coarse for sensitive coordination.

Source:

- HL7 FHIR Consent: https://fhir.hl7.org/fhir/consent.html

## 14.3 Relevant-only disclosure is a real specialist requirement

U.S. HHS guidance under HIPAA repeatedly states that providers may share with family/friends involved in care, but disclosures should be limited to information directly relevant to that person's involvement.

Although LifeOS is not defined by U.S. healthcare law, the pattern is valuable product evidence because it matches the simulation's `minimum necessary context` principle.

Sources:

- HHS family/friend disclosure FAQ: https://www.hhs.gov/hipaa/for-professionals/faq/2087/does-hipaa-allow-a-health-care-provider-to-communicate-with-a-patients-family-friends-or-other-persons-who-are-involved-in-the-patient-care.html
- HHS family/friends guidance: https://www.hhs.gov/hipaa/for-individuals/family-members-friends/index.html

---

# 15. Specialist systems reinforce the boundary: coordinate around them, do not casually replace them

Healthcare standards and workplace systems repeatedly show specialist concepts whose semantics matter: clinical consent, care roles, qualification, manager approval, workforce scheduling, etc.

The simulation's negative evidence is therefore strengthened:

> LifeOS can coordinate personal and shared consequences around specialist systems without pretending their domain semantics are generic calendar fields.

This is particularly strong for healthcare, workforce management, education administration and legal workflows.

---

# 16. Education: agency is distributed, not simply hierarchical

Recent HCI work on classroom orchestration studies how control can shift between teachers and students before, during and after collaborative activity. The design problem is not only `teacher has authority`; it is how to preserve appropriate teacher guidance while allowing student agency to increase where suitable.

A 2026 paper on teacher/student dynamic pairing recommends hybrid control rather than fixed unilateral control.

**Implication:** LifeOS should not assume one static authority model for all relationships. Authority may be contextual, phase-specific and object-specific.

Source:

- Yang et al., *Balancing Teacher and Student Agency: Co-Orchestration Tool Design Supporting Real-Time Dynamic Pairing* (2026): https://arxiv.org/abs/2605.18761

---

# 17. Shared expenses: a successful narrow domain shows the value of canonical shared state

Splitwise provides a useful narrow example of structured coordination that does not try to become a general social platform.

Its model revolves around:

- group or one-off context;
- payer;
- beneficiaries;
- split method;
- balances;
- settlement;
- recurring expenses;
- simplification of payment paths.

The product's `Simplify Debts` feature can alter who pays whom while preserving every participant's total balance. This demonstrates a useful distinction between **economic truth** and **chosen coordination path**.

**Implication:** shared financial state may justify native LifeOS support at a lightweight level, but payment execution and accounting need not become core LifeOS responsibilities.

Sources:

- Splitwise overview: https://www.splitwise.com/
- Splitwise getting started: https://kb.splitwise.com/getting-started/how-do-i-use-splitwise
- Splitwise Simplify Debts: https://kb.splitwise.com/balances-and-expenses/what-is-simplify-debts

---

# 18. External participants are not edge cases

Google Calendar allows inviting any email address, including people without Google Calendar, who can RSVP by email.

Microsoft Teams supports several different cross-boundary models — anonymous meeting join, external access and guest membership — with different capabilities. Importantly, some Microsoft features do **not** support guests: Teams Shifts currently excludes guests entirely.

This is valuable negative product evidence. Even mature ecosystems struggle when collaboration crosses organization/product boundaries.

**Strong confirmation:** LifeOS should distinguish levels of external participation rather than force `full account member` as the only state.

Potential participation tiers suggested by evidence, without yet defining final product concepts:

- receive information only;
- RSVP / acknowledge;
- contribute one bounded response or artifact;
- temporarily participate in one shared item;
- persistent registered collaborator.

Sources:

- Google Calendar non-user invitations: https://support.google.com/calendar/answer/37161
- Microsoft Teams external/guest meeting participation: https://support.microsoft.com/en-us/teams/meetings/join-a-microsoft-teams-meeting-or-event-outside-your-org
- Microsoft Teams guest access: https://support.microsoft.com/en-US/teams/teams-channels/add-guests-to-a-team-in-microsoft-teams
- Microsoft Shifts guest limitation: https://learn.microsoft.com/en-us/microsoftteams/expand-teams-across-your-org/shifts/manage-the-shifts-app-for-your-organization-in-teams

---

# 19. Family coordination products show breadth — and the danger of the mega-dashboard

Current family products such as FamilyWall and Cozi converge around combinations of:

- shared calendar;
- reminders;
- shopping lists;
- to-dos;
- meal planning;
- budgeting;
- location;
- family messaging;
- multiple groups/circles.

This validates demand for cross-domain family coordination, but it also demonstrates a common product pattern: collect many household utilities into one shared dashboard.

That is not necessarily the right identity for LifeOS.

The LifeOS simulation suggests a more general differentiator: a shared fact can affect each person's independent planning model differently, rather than forcing every participant to live inside one family dashboard.

Sources:

- FamilyWall official feature overview: https://www.familywall.com/en/index.html
- FamilyWall support: https://support.familywall.com/en/support/solutions/articles/47001013681-about-familywall
- Cozi App Store description: https://apps.apple.com/it/app/cozi-family-organizer/id407108860

---

# 20. Care coordination products support explicit communities and claimable help

Lotsa Helping Hands provides a private care community where meals, rides, shopping, childcare, visits and coverage are represented as calendar activities/tasks that volunteers can take.

This validates:

- open/claimable responsibility;
- care circles larger than immediate family;
- recurring help needs;
- bounded information sharing;
- social support coexisting with structured tasks.

It also highlights a distinction underrepresented in the simulation: sometimes the owner does not know *who* should do a task. The useful state is:

> this responsibility needs a qualified/willing person from an eligible set.

This is analogous to open shifts but applies beyond employment.

Sources:

- Lotsa Helping Hands coordination service: https://lls.lotsahelpinghands.com/caregiving/home/
- Activities & Tasks model: https://www.lotsahelpinghands.com/help/pe_activities.html

---

# 21. Privacy by design supports minimization as an architectural product principle

European data-protection guidance provides strong external support for the simulation's selective-sharing hypothesis.

The EDPB describes privacy by design/default as building protection into systems from the start and using defaults that protect individuals. Its SME guidance explicitly states that, by default, only data necessary for each specific purpose should be processed, including amount, extent, storage and accessibility.

European Commission GDPR guidance similarly emphasizes purpose limitation and data minimization.

Consent, where relied upon, must be specific, informed and withdrawable; consent is not freely given when there is a significant power imbalance or unnecessary processing is made a condition of service.

**Product implications:**

- `share full context because it is easier` is a poor default;
- sharing should be purpose/scenario-aware;
- revocation is part of the lifecycle, not an administrative afterthought;
- employer/employee and similar power relationships require more caution than peer friendships;
- LifeOS should often compute coordination from abstractions such as availability rather than disclose source data.

Sources:

- EDPB Data Protection by Design and by Default: https://www.edpb.europa.eu/topics/ai-and-technology/privacy-by-design-and-by-default_en
- EDPB SME guidance: https://www.edpb.europa.eu/sme/be-compliant/be-compliant_en
- European Commission GDPR principles: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en
- European Commission consent guidance: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/grounds-processing/when-consent-valid_en

---

# 22. Relationship-based authorization is technically plausible, but this research does not choose it

The simulation produced needs that are awkward for simplistic global roles:

- Anna can see one child's pickup details because she is caregiver for this period;
- Luca can edit one trip but not the rest of a friend's calendar;
- a technician can see evidence attached to one service visit;
- a family member can receive transport details but not clinical information;
- a former collaborator retains historical attribution but loses future access.

Google's Zanzibar paper demonstrates that large-scale authorization can be modeled around relationships between users and objects. Modern OpenFGA documentation additionally illustrates relationship-based, userset and conditional/time-based authorization patterns.

This is **technical feasibility evidence only**. It does not mean LifeOS should adopt OpenFGA or Zanzibar-style infrastructure now.

It does, however, weaken the assumption that all future permissions must fit static account roles such as `admin/member/viewer`.

Sources:

- Google Research, *Zanzibar: Google's Consistent, Global Authorization System*: https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/
- OpenFGA concepts: https://openfga.dev/docs/concepts
- OpenFGA conditions / time-based authorization: https://openfga.dev/docs/modeling/conditions

---

# 23. One of the largest research warnings: collaboration tools can reproduce power structures

Across calendars, household labor, shift scheduling, education and caregiving, the evidence repeatedly shows that collaboration technology does not merely transmit neutral information. It changes:

- who performs coordination work;
- who becomes visible;
- who can interrupt whom;
- who controls shared time;
- whose preferences become defaults;
- who must justify exceptions;
- which actions are considered authoritative.

Therefore a product that technically supports multiple users can still be socially single-owner.

**LifeOS-specific risk:** if the creator of an item automatically controls all fields, visibility, notification policy and participant state, the system may encode `organizer dominance` into every relationship.

The simulation already suspected this. External evidence makes it a first-order design risk.

---

# 24. Research comparison against the simulation

## 24.1 Strongly confirmed findings

External evidence strongly supports the following simulated findings:

### Shared fact and personal context should remain separable

Calendar research, privacy evidence, cross-organization tools and healthcare coordination all support different local/private views around a common commitment.

### Availability should be shareable without calendar disclosure

Both classic calendar research and current Outlook products support free/busy abstractions.

### Participation is stateful

Yes/No/Maybe invitations, shift requests and social-event research all show that binary membership is insufficient.

### Proposal, agreement, authority confirmation and actual outcome differ

Work scheduling and common-ground research strongly reinforce this separation.

### Responsibility is not one field

Delegation, open shifts, volunteer care and authority approval show distinctions among doing, accepting, owning, approving and substituting.

### External participants are normal

Current calendar/meeting products and adoption research confirm partial-membership reality.

### Privacy must be selective and contextual

Calendar research, GDPR guidance, healthcare law/standards and current products converge here.

### Roles and membership change over time

FHIR CareTeam, work substitution and authorization patterns all support temporal lifecycle.

### Planned and actual participation must remain separate

Social-event research and care evidence strongly validate this.

### Shared resources matter alongside people

Coordination theory and scheduling domains both identify shared-resource dependency as fundamental.

### Specialist systems should not be flattened into generic collaboration

Healthcare/workforce evidence strongly reinforces the boundary.

---

# 25. Findings strengthened beyond what the simulation originally expressed

## 25.1 Coordination cost must be measured per actor

The simulation compared `without LifeOS` and `with LifeOS`, but research suggests a sharper test:

> who does additional work, and who receives the benefit?

A feature should be treated skeptically if it centralizes benefit while distributing tedious maintenance to others.

## 25.2 Common ground deserves explicit attention

The simulation included acknowledgement, but research shows the deeper issue is whether participants possess sufficiently aligned understanding to coordinate safely.

## 25.3 Invisible coordination labor is a separate burden

Assignment does not equal responsibility transfer. Someone may still carry planning, anticipation, reminding and verification.

## 25.4 Fairness is procedural and social, not only numerical

Optimization, equal allocation or perfect availability matching can still feel unfair. Negotiation, explanation and social context matter.

## 25.5 Evidence from collaborative systems is situated

A click, sensor reading or reminder acknowledgment may not mean what a naive system assumes. Context and source matter.

## 25.6 Groups should not be treated as homogeneous actors

Families, teams and care circles contain asymmetric roles, expertise, authority and willingness to participate.

## 25.7 Open responsibility is a reusable pattern

Several domains need `someone eligible should claim this`, not immediate assignment to a named individual.

---

# 26. Findings that qualify or challenge the simulation

## 26.1 More structure is not always better

The simulation correctly included negative evidence, but CSCW research makes this stronger: adding explicit state can itself create maintenance work and adoption failure.

LifeOS should not require every social event to become a mini-workflow.

## 26.2 Full transparency can harm collaboration

More awareness can enable coordination but can also create judgment, surveillance and interruption. `Everyone can see everything` is not a neutral convenience.

## 26.3 Equal participation is not always the desired end state

Some families intentionally use one primary scheduler; some work settings require formal authority; some care situations require representative action. The objective is appropriate agency and fairness, not symmetry for its own sake.

## 26.4 AI automation can preserve or worsen inequality

Reducing clicks for the household coordinator does not necessarily redistribute cognitive ownership. AI can become another system one person must curate.

## 26.5 Consensus is not universally required

Some decisions are peer-negotiated; others are externally authoritative; others permit unilateral local choice. A generic `vote until agreement` model would be wrong.

---

# 27. Important needs missing or underweighted in the simulation

## 27.1 Coordination stewardship / mental load

Who notices, anticipates, creates, reminds, verifies and repairs coordination should be visible in the product analysis even when not exposed as a user-facing metric.

## 27.2 Cost-benefit asymmetry

Every collaborative capability should be evaluated for per-participant burden.

## 27.3 Grounding / shared understanding

Critical changes may require more than delivery receipt; participants sometimes need acknowledgement with meaning.

## 27.4 Procedural fairness

Systems involving scarce slots, workload or repeated concessions should consider whether decision processes are perceived as fair and explainable.

## 27.5 Claimable / open responsibilities

The responsible person may be selected later from a group or eligible pool.

## 27.6 Escalation policy as coordination repair

When nobody accepts, somebody fails to acknowledge or prerequisites remain unresolved, real groups need a repair path rather than infinite reminders.

## 27.7 Social cost of refusing

A user may technically be able to decline but feel socially unable to do so. Privacy/consent UI cannot assume all relationships have equal power.

## 27.8 Trust level of evidence

Self-report, another person's report, external authoritative data, sensor data and inferred AI conclusions can disagree and should not collapse automatically.

## 27.9 Coordination fatigue

Repeated approvals, updates and notifications create their own workload. The product needs a notion of when *not* to ask.

---

# 28. Product landscape patterns

Across current products, several recurring patterns appear.

## Calendar platforms

Strengths:

- canonical event;
- RSVP;
- free/busy;
- basic delegation;
- external invitations.

Weakness:

- relatively weak modeling of personal meaning around the same event;
- limited cross-domain responsibility/dependency handling.

## Family organizers

Strengths:

- broad household dashboard;
- shared calendar, lists, meals, chores, location, messaging.

Weakness:

- often assumes one shared family surface rather than independent personal systems coordinating selectively.

## Work collaboration / scheduling

Strengths:

- formal roles, approvals, shift requests, assignment and workflow.

Weakness:

- often too process-heavy for informal life and cross-boundary participants.

## Expense-sharing tools

Strengths:

- narrow, clear shared canonical financial state;
- excellent fit for one recurring dependency family.

Weakness:

- little broader personal planning context.

## Care coordination tools

Strengths:

- shared help calendar;
- volunteer/claimable responsibilities;
- sensitive information and care circles.

Weakness:

- often focused on one care recipient and one domain rather than a complete personal operating model.

**LifeOS opportunity suggested by comparison:** do not beat every specialist product at its own specialist workflow. Provide a reusable coordination grammar that can connect shared realities to each participant's private operating model.

---

# 29. A deeper model of multi-actor value discovered by research

The combined simulation + research suggests that multi-actor value can be understood through five layers.

## Layer A — Shared reality

What facts must several actors coordinate around?

Examples: date, location, deadline, current decision, shared resource, required outcome.

## Layer B — Dependency

Why must they coordinate?

Examples: simultaneity, prerequisite, producer/consumer, shared resource, hand-off, approval.

## Layer C — Actor relationship

What can each actor legitimately do, know or decide in this context?

Examples: participant, organizer, caregiver, approver, performer, external authority, temporary substitute.

## Layer D — Personal interpretation

How does the shared fact affect each person's own LifeOS?

Examples: travel buffer, private preparation, goal linkage, capacity impact, personal reminder, private notes.

## Layer E — Coordination evidence

How do participants know whether shared understanding and execution are adequate?

Examples: proposed, seen, acknowledged, accepted, confirmed, evidence received, actually attended, disputed.

This five-layer framing is not yet a domain model. It is a research synthesis that can later be used to test domain-model proposals.

---

# 30. Risk register derived from external evidence

## R1 — Organizer tax reversal

LifeOS reduces organizer burden by imposing maintenance burden on everyone else.

## R2 — Digital mental-load trap

LifeOS makes household coordination more efficient but leaves one person responsible for configuring and supervising the system.

## R3 — Surveillance through awareness

Useful coordination data becomes an unintended mechanism for judging time use, location or responsiveness.

## R4 — Notification bureaucracy

Structured collaboration generates more prompts than the social problem justified.

## R5 — False completion / false certainty

A click, elapsed time or third-party report is treated as unquestionable evidence of reality.

## R6 — Permission explosion

Trying to expose every possible privacy distinction directly to the user creates unusable configuration.

## R7 — Universal-adoption dependency

Important flows break when one participant is external or refuses an account.

## R8 — Role overgeneralization

One global `member/admin` hierarchy is stretched across friendships, families, work, care and professional contexts.

## R9 — Specialist-system overreach

LifeOS begins replicating clinical, workforce, education or enterprise administration instead of coordinating with it.

## R10 — Algorithmic unfairness by simplification

Scheduling/assignment optimization ignores social norms, repeated sacrifices or unequal ability to refuse.

## R11 — Context collapse

Information shared for one purpose becomes visible or reusable in unrelated shared contexts.

## R12 — Relationship-end leakage

Former partners, caregivers, colleagues or collaborators retain future visibility after the social relationship ends.

---

# 31. Research-derived validation questions for future work

These questions should challenge future multi-actor product/domain proposals without yet fixing their answers.

1. Can a participant contribute meaningfully without creating a full LifeOS account?
2. Can LifeOS coordinate availability without exposing underlying private events?
3. Does a proposed capability reduce total coordination burden or merely transfer it?
4. Who performs invisible setup, monitoring and repair work?
5. Is a state a proposal, acknowledgement, agreement, authoritative fact or actual outcome?
6. What dependency is being managed?
7. Does the participant need the underlying reason or only its consequence?
8. Can responsibility be claimed, delegated, substituted and later revoked without rewriting history?
9. Can one shared fact have different private consequences for each participant?
10. How does the system behave when reports conflict or evidence is uncertain?
11. Does an algorithmic recommendation preserve perceived procedural fairness?
12. Is the group necessary, or would a single bounded shared item be simpler?
13. Does the collaboration still work if only half the people use LifeOS?
14. Can access end at a specific point while historical attribution remains?
15. Are notifications providing activity awareness or merely producing noise?
16. Does the design accidentally give the item creator social authority they do not actually possess?
17. Is a specialist external system the real authority for this fact?
18. What is the least information required to coordinate this actor's responsibility?
19. What happens when the relationship itself changes or becomes adversarial?
20. Can the user inspect and revoke active sharing without understanding an ACL system?

---

# 32. Research conclusions by confidence

## High-confidence conclusions

### C1. Multi-user LifeOS cannot be modeled as `single-user objects + shared=true`

The evidence across CSCW, calendars, care, work and privacy is too strong. Actor state, authority, privacy and local meaning differ materially.

### C2. Shared canonical facts and personal overlays are a strong product direction

This idea is independently supported by calendar privacy, cross-domain coordination and specialist-system boundaries.

### C3. Multi-user state must preserve uncertainty and lifecycle

Invitation, acceptance, authority confirmation, actual participation and later evidence are distinct.

### C4. Selective disclosure is not an optional privacy enhancement

It is fundamental to real coordination.

### C5. External participation must be designed intentionally

Critical-mass and cross-boundary evidence makes this necessary for broad applicability.

### C6. Coordination burden itself is a product metric

A collaboration flow is not successful merely because shared state is correct.

### C7. Responsibility and authority require richer semantics than assignment

This appears across care, work, family and specialist scenarios.

### C8. Context-specific authority must coexist with personal autonomy

Neither complete peer symmetry nor universal organizer control is defensible.

## Strong but still design-dependent conclusions

### C9. Groups should be lightweight containers rather than automatic privacy domains

Evidence favors contextual participation over blanket group exposure.

### C10. Open/claimable responsibilities are likely reusable beyond work scheduling

Caregiving and volunteer coordination reinforce this.

### C11. Meaningful acknowledgement should be available for high-consequence changes

But it should not become mandatory bureaucracy for casual activity.

### C12. LifeOS may need explicit support for coordination stewardship

Whether this becomes a visible domain concept or remains an analytical property is intentionally undecided.

---

# 33. What the research does NOT justify

External research does not justify immediately building:

- enterprise organization administration;
- universal RBAC/ReBAC infrastructure before domain needs are modeled;
- a general chat platform;
- voting/consensus for all shared decisions;
- detailed productivity surveillance;
- full family location tracking by default;
- clinical or legal records systems;
- workforce management;
- mandatory group workspaces;
- automatic AI mediation of interpersonal conflict;
- a universal `fairness score`;
- universal visibility of activity history;
- complex approval chains for ordinary social life.

The research strengthens the need for a flexible coordination foundation, but also strengthens the case for progressive disclosure and domain restraint.

---

# 34. Relationship to the original simulation

The simulation's strongest hypothesis survives external research:

> independent personal systems should be able to coordinate around shared facts, responsibilities and resources without being merged into one shared operating system.

External evidence adds four major requirements around that hypothesis:

1. **coordination-cost fairness** — collaboration must not disproportionately burden the wrong participant;
2. **common-ground support** — important shared changes require enough acknowledgement/context to become operationally understood;
3. **invisible-work awareness** — task assignment alone does not prove coordination burden was transferred;
4. **social/authority realism** — fairness, power, consent and legitimate authority differ by relationship and context.

These are the most important additions produced by the research pass.

---

# 35. Recommended next evidence work

Before promoting concepts into binding domain decisions, additional targeted research would still be useful in four areas:

1. **relationship breakdown and hostile/adversarial exits** — separation, terminated employment, abusive/coercive relationships and revocation UX;
2. **children and adolescent agency** — guardian authority versus age-appropriate privacy and autonomy, particularly in Europe;
3. **accessibility and low-digital-literacy collaboration** — SMS/email/voice/print and assisted interaction models;
4. **AI multi-party mediation** — how AI should reason when participants have different private contexts, permissions, interests and authority without leaking one person's data to another.

These should be treated as focused follow-up research families, not reasons to reopen or rewrite the completed simulation.

---

# 36. Source register

## Foundational CSCW / coordination

- Grudin, *Why CSCW Applications Fail*: https://doi.org/10.1145/62266.62273
- Grudin, *Groupware and Social Dynamics*: https://www.microsoft.com/en-us/research/?p=357080
- Malone & Crowston, *What is coordination theory...*: https://doi.org/10.1145/99332.99367
- Malone & Crowston, *The Interdisciplinary Study of Coordination*: https://ccs.mit.edu/papers/CCSWP157.html
- Crowston, *A Coordination Theory Approach to Organizational Process Design*: https://doi.org/10.1287/orsc.8.2.157

## Common ground / awareness

- Clark research overview: https://web.stanford.edu/~clark/research.html
- Clinical common ground: https://pmc.ncbi.nlm.nih.gov/articles/PMC3041298/
- Carroll et al., notification/activity awareness: https://www.sciencedirect.com/science/article/pii/S1071581903000247
- Awareness displays/social motivation: https://doi.org/10.1287/isre.1080.0175
- Collaborative information seeking awareness: https://doi.org/10.1002/asi.22819

## Calendar / family

- Palen, groupware calendar privacy: https://doi.org/10.1145/302979.302982
- Neustaedter et al., family calendar: https://doi.org/10.1145/1502800.1502806
- LINC participatory design: https://www.microsoft.com/en-us/research/publication/linc-ing-the-family-the-participatory-design-of-an-inkable-family-calendar/
- LINC field trial: https://graphicsinterface.org/proceedings/gi2007/gi2007-27/
- Outlook sharing: https://support.microsoft.com/en-us/outlook/sharing/share-an-outlook-calendar-as-view-only-with-others
- Outlook delegation: https://support.microsoft.com/en-us/outlook/sharing/about-delegates-allow-someone-to-manage-your-mail-and-calendar-in-outlook
- Google Calendar invitations: https://support.google.com/calendar/answer/37161

## Household / mental load

- Frampton et al., *The Domestic Operating System*: https://doi.org/10.1145/3772318.3791167
- Ciciolla & Luthar, invisible household labor: https://doi.org/10.1007/S11199-018-1001-X
- Barigozzi et al., mental load: https://amsacta.unibo.it/id/eprint/8356/
- Wang et al., family education labor: https://arxiv.org/abs/2602.10501

## Social participation

- Huang et al., online invitation vs offline participation: https://arxiv.org/abs/1311.0663

## Work / shifts

- Uhde et al., fair collaborative shift scheduling: https://arxiv.org/abs/2001.09755
- Uhde et al., self-scheduling practices: https://arxiv.org/abs/2102.02132
- Microsoft Teams Shifts requests: https://support.microsoft.com/en-us/teams/free/request-open-shifts-swap-or-offer-shifts-in-shifts
- Microsoft Teams Shifts privacy/settings: https://support.microsoft.com/en-US/Teams/free/configure-settings-for-your-team-s-schedule-in-shifts

## Caregiving / healthcare

- di Fiore et al., family caregiver software needs: https://arxiv.org/abs/1701.07607
- Lai & Mihailidis, Remindful: https://arxiv.org/abs/2604.19574
- HL7 FHIR CareTeam: https://hl7.org/fhir/careteam.html
- HL7 FHIR Consent: https://fhir.hl7.org/fhir/consent.html
- HHS HIPAA family/caregiver sharing: https://www.hhs.gov/hipaa/for-professionals/faq/2087/does-hipaa-allow-a-health-care-provider-to-communicate-with-a-patients-family-friends-or-other-persons-who-are-involved-in-the-patient-care.html

## Education

- Yang et al., teacher/student agency: https://arxiv.org/abs/2605.18761

## Shared expenses / household products / care products

- Splitwise: https://www.splitwise.com/
- Splitwise getting started: https://kb.splitwise.com/getting-started/how-do-i-use-splitwise
- Splitwise simplify debts: https://kb.splitwise.com/balances-and-expenses/what-is-simplify-debts
- FamilyWall: https://www.familywall.com/en/index.html
- Cozi: https://apps.apple.com/it/app/cozi-family-organizer/id407108860
- Lotsa Helping Hands: https://lls.lotsahelpinghands.com/caregiving/home/

## External participation

- Google Calendar guests: https://support.google.com/calendar/answer/37161
- Teams outside-org meeting participation: https://support.microsoft.com/en-us/teams/meetings/join-a-microsoft-teams-meeting-or-event-outside-your-org
- Teams guest access: https://support.microsoft.com/en-US/teams/teams-channels/add-guests-to-a-team-in-microsoft-teams
- Teams Shifts guest limitation: https://learn.microsoft.com/en-us/microsoftteams/expand-teams-across-your-org/shifts/manage-the-shifts-app-for-your-organization-in-teams

## Privacy / authorization

- EDPB Privacy by Design/Default: https://www.edpb.europa.eu/topics/ai-and-technology/privacy-by-design-and-by-default_en
- EDPB SME compliance guidance: https://www.edpb.europa.eu/sme/be-compliant/be-compliant_en
- European Commission GDPR principles: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en
- European Commission consent guidance: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/grounds-processing/when-consent-valid_en
- Zanzibar: https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/
- OpenFGA concepts: https://openfga.dev/docs/concepts

---

# Conclusion

The external evidence does not overturn the simulation. It makes its central result considerably stronger while exposing several areas where a naive implementation would fail.

The research supports a model in which collaboration is not a shared account or a group calendar layered on top of a personal planner. It is the controlled coordination of dependencies among independent actors who may possess different information, authority, responsibilities, tools and personal interpretations of the same shared reality.

The most defensible product hypothesis after both simulation and research is therefore:

> **LifeOS should coordinate shared reality while minimizing coordination burden and disclosure, preserving each person's private operating model, representing responsibility and authority truthfully, and keeping proposal, understanding, agreement and actual outcome distinct.**

The evidence also establishes a critical warning:

> **A multi-user feature is not successful merely because it enables collaboration. It is successful only when the coordination benefit exceeds the new social, cognitive, privacy and maintenance costs it creates for the people involved.**

This document remains research evidence. Specific domain concepts should be promoted only through a separate synthesis/readiness step after this research and the simulation are reviewed together.