# LifeOS — Multi-Actor / Collaboration Deep Research

**Date:** 11 August 2026  
**Status:** Product research / external evidence — consolidated and quality-checked  
**Scope:** challenge, validate and expand the findings of `multi-actor-collaboration-discovery-simulation-2026-08.md` through external research across independent evidence families, including high-risk stress domains.  
**Relationship to simulation:** this document does not rewrite the simulation. The simulation and this research remain two separate evidence sources: one generated from realistic LifeOS-oriented scenarios, the other from external research. Binding product/domain/architecture decisions require a later synthesis step.

---

# 1. Purpose

The earlier multi-actor simulation deliberately started from people and situations before looking at competitors, standards or academic literature. This research performs the complementary exercise: examine established CSCW/HCI findings, current specialist standards, regulation, mature product patterns and recent research to determine whether the simulated findings survive contact with external evidence.

The research question is not:

> Which collaboration features should LifeOS copy?

It is:

> What is already known about how people coordinate, establish common ground, share responsibility, manage dependencies and resources, protect privacy, preserve agency, recover from breakdowns and collaborate across unequal or changing relationships — and what does that evidence imply for the hypotheses discovered by the LifeOS simulation?

The study also asks a second question that is easy to miss in collaboration design:

> Does the collaboration mechanism reduce real coordination burden for the people involved, or merely move that burden from one actor to another?

This remains product evidence. It does **not** decide:

- database tables or physical schema;
- final domain entities;
- ACL/RBAC/ReBAC implementation;
- organization/account hierarchy;
- exact invitation/synchronization protocols;
- AI orchestration architecture;
- final UI;
- pricing/packaging;
- release placement in V1/V2/later;
- replacement of specialist systems.

---

# 2. Research method and evidence quality

This is a **broad narrative evidence review**, not a formal systematic review or meta-analysis. It intentionally spans multiple evidence families because multi-user coordination is socio-technical: no single literature, product category or standard captures the whole problem.

Evidence families examined:

1. foundational CSCW / groupware;
2. coordination theory and dependency management;
3. common ground, awareness and notification;
4. shared calendars and temporal privacy;
5. household/family coordination;
6. invisible domestic and cognitive labor;
7. social invitations and actual participation;
8. work scheduling, shifts, substitution and fairness;
9. caregiving and distributed care coordination;
10. healthcare consent, care teams and specialist-system boundaries;
11. education and multi-stakeholder agency;
12. shared expenses and narrow shared ledgers;
13. external/non-member participation and cross-boundary collaboration;
14. privacy, consent and data minimization;
15. relationship-based authorization as feasibility evidence;
16. current product patterns across calendar, family, work and care tools;
17. adversarial relationship exits and technology-facilitated abuse;
18. ongoing high-conflict but unavoidable collaboration;
19. children/adolescent agency and guardian power;
20. accessibility, older adults and low digital literacy;
21. AI-mediated multi-party privacy, disclosure and authority.

Evidence is interpreted using four confidence classes:

- **High confidence:** repeated findings across established research and/or authoritative standards and guidance.
- **Strong practical evidence:** mature products or official platform behavior demonstrating a recurring pattern at scale.
- **Domain evidence:** strong within a specialist context but not automatically universal.
- **Emerging evidence:** recent research, preprints or early patterns that are important enough to track but must not be generalized prematurely.

A product implementing a feature is not proof that the feature is correct. One paper is not proof of universality. Likewise, a technical authorization model being feasible does not mean LifeOS should adopt that infrastructure.

---

# 3. Foundational CSCW: collaboration is not single-user software multiplied by N

## 3.1 Work/benefit disparity is a primary failure mode

Jonathan Grudin's foundational groupware work shows that collaborative systems often fail for organizational and social reasons rather than because their feature set is insufficient. A central problem is **disparity between who performs the work and who receives the benefit**.

For LifeOS this produces a stronger test than “does this feature help coordination?”

Example:

- an organizer benefits from perfect RSVP and availability state;
- every guest must create an account, expose preferences, maintain state and acknowledge every change;
- organizer burden falls while total group burden rises.

The system may be more structured and still be worse.

**Finding:** evaluate **coordination cost per actor**, not only overall capability.

This strongly reinforces:

- non-LifeOS participation;
- progressive disclosure;
- not turning tiny social situations into workflows;
- avoiding organizer convenience that becomes participant bureaucracy.

Sources:

- Jonathan Grudin, *Why CSCW Applications Fail: Problems in the Design and Evaluation of Organizational Interfaces*, CSCW 1988: https://doi.org/10.1145/62266.62273
- Jonathan Grudin, *Groupware and Social Dynamics: Eight Challenges for Developers*, CACM 1994: https://www.microsoft.com/en-us/research/?p=357080

## 3.2 Critical mass and heterogeneous tools matter

Groupware adoption research repeatedly shows that partial adoption, conflicting local standards and organizational boundaries matter. A coordination system can be excellent for one group and still fail because collaborators belong to different tool ecosystems or do not receive enough value to join.

**Finding:** partial adoption is not an edge case or failed migration. It is a normal collaboration state.

LifeOS should therefore be evaluated assuming that some participants:

- use LifeOS deeply;
- use it occasionally;
- interact through a bounded link/email/message;
- use another provider;
- never create a LifeOS account.

Source:

- *Groupware adoption in a distributed organization: transporting and transforming technology through social worlds*: https://www.sciencedirect.com/science/article/abs/pii/S1471772704000405

---

# 4. Coordination theory: the reusable core is dependency management

Malone and Crowston frame coordination as managing dependencies among activities. Recurring dependency types include:

- shared resources;
- producer/consumer relationships;
- simultaneity constraints;
- task/subtask relationships;
- assignment;
- prerequisites.

This independently supports the simulation: dinners, care, work, travel, service appointments and surgery look different on the surface but repeatedly reduce to a small number of coordination dependencies.

Examples:

- one actor must act before another;
- several people need the same scarce resource;
- several actors must be available together;
- one participant produces information or an artifact another requires;
- an approval blocks canonical state change;
- a substitution changes who performs work without changing the underlying commitment.

**Strong confirmation:** multi-user discovery should ask not only *what is shared?* but **what dependency must be managed?**

Sources:

- Malone & Crowston, *What is coordination theory and how can it help design cooperative work systems?*, CSCW 1990: https://doi.org/10.1145/99332.99367
- Malone & Crowston, *The Interdisciplinary Study of Coordination*, ACM Computing Surveys 1994: https://ccs.mit.edu/papers/CCSWP157.html
- Crowston, *A Coordination Theory Approach to Organizational Process Design*, Organization Science 1997: https://doi.org/10.1287/orsc.8.2.157

---

# 5. Common ground: delivery is not shared understanding

Herbert Clark's work on grounding distinguishes transmission from mutual understanding. This matters directly to LifeOS because collaborative state is often naively collapsed.

A safer conceptual chain is:

```text
sent
!= seen
!= understood
!= acknowledged
!= accepted
!= authoritative/confirmed
!= acted upon
!= actually happened
```

Healthcare collaboration research similarly shows that information can exist somewhere in a system while teams still lack sufficient common ground to coordinate safely.

**Strong confirmation:** proposal, notification, acknowledgement, agreement, canonical confirmation and actual outcome must remain conceptually distinguishable where consequence warrants it.

**Refinement:** acknowledgement is not only a notification receipt. In important contexts it can be a **grounding mechanism**: evidence that a participant has incorporated the change into their operational understanding.

This does not mean every dinner needs acknowledgement bureaucracy. Consequence determines required grounding depth.

Sources:

- Herbert H. Clark research on common ground and grounding: https://web.stanford.edu/~clark/research.html
- *Describing the Clinical Communication Space through a Model of Common Ground*: https://pmc.ncbi.nlm.nih.gov/articles/PMC3041298/

---

# 6. Awareness and notification: enough context, not a firehose

Collaborators need awareness of relevant changes, but research distinguishes useful activity awareness from raw notification volume.

Simple notifications are often insufficient for complex persistent activity because people need context: what changed, why it matters, what is expected next and whether action is required.

At the same time, greater visibility can become interruption, judgment or surveillance.

**Findings:**

- `notify everyone about everything` is not a sound collaboration model;
- propagation should follow affected actors and dependencies;
- useful updates are meaningful deltas, not event-log spam;
- awareness should reduce coordination work rather than create a new monitoring job;
- private reasons should not be exposed merely to explain availability or absence;
- acknowledgement should be reserved for changes where missing shared understanding has real consequence.

Sources:

- Carroll et al., *Notification and awareness: synchronizing task-oriented collaborative activity*: https://www.sciencedirect.com/science/article/pii/S1071581903000247
- *Awareness Displays and Social Motivation for Coordinating Communication*: https://doi.org/10.1287/isre.1080.0175
- Shah, *Effects of awareness on coordination in collaborative information seeking*: https://doi.org/10.1002/asi.22819

---

# 7. Shared calendars: availability is sensitive information

## 7.1 Calendar privacy is broader than hiding titles

Palen's classic calendar research identified several privacy dimensions:

- private event content;
- socially sensitive information involving others;
- organizationally sensitive information;
- judgments inferred from time allocation;
- loss of control over access to one's time.

This validates one of the simulation's strongest findings:

> coordination often needs the **consequence** of private context, not the private context itself.

For scheduling, `unavailable 14:00–16:00` can be sufficient. The reason may be irrelevant and inappropriate to share.

Source:

- Palen, *Social, Individual & Technological Issues for Groupware Calendar Systems*, CHI 1999: https://doi.org/10.1145/302979.302982

## 7.2 Mature products converge on graduated disclosure

Current Outlook sharing separates busy-only, partial details, full details and delegate/editor authority. Google Calendar supports Yes/No/Maybe and invitation by email to people who do not use Google Calendar.

These are practical signals that:

- availability and detail are distinct;
- viewing and acting on behalf of are distinct;
- participation is richer than membership;
- external participants are ordinary.

Sources:

- Outlook calendar sharing: https://support.microsoft.com/en-us/outlook/sharing/share-an-outlook-calendar-as-view-only-with-others
- Outlook delegation: https://support.microsoft.com/en-us/outlook/sharing/about-delegates-allow-someone-to-manage-your-mail-and-calendar-in-outlook
- Google Calendar invitations/non-Google guests: https://support.google.com/calendar/answer/37161

---

# 8. Family coordination: the shared calendar is an awareness artifact, not the whole social system

Family-calendar studies show that households coordinate through social practices around calendars; the calendar itself does not replace those practices.

Households also differ structurally:

- one primary scheduler may coordinate most activity;
- responsibility may be distributed;
- members may have different willingness and competence;
- existing routines strongly affect adoption.

**Implications:**

- household participation should not be assumed symmetric;
- `family workspace` should not imply equal management work;
- LifeOS should expose and optionally redistribute coordination work rather than pretend it is already equally shared;
- existing successful practices should remain usable instead of being replaced for ideological symmetry.

Sources:

- Neustaedter, Brush & Greenberg, *The Calendar is Crucial: Coordination and Awareness through the Family Calendar*, TOCHI 2009: https://doi.org/10.1145/1502800.1502806
- Microsoft Research, *LINC-ing the Family*: https://www.microsoft.com/en-us/research/publication/linc-ing-the-family-the-participatory-design-of-an-inkable-family-calendar/
- *A digital family calendar in the home: lessons from field trials of LINC*: https://graphicsinterface.org/proceedings/gi2007/gi2007-27/

---

# 9. Household coordination: visible tasks are not the whole workload

The 2026 CHI paper *The Domestic Operating System* is particularly relevant because it examines hidden household cognitive labor. Digital tools commonly represent visible outputs — chores, calendar entries, lists — while much of the difficult work remains invisible.

Examples include:

- noticing that something will soon be needed;
- anticipating deadlines and conflicts;
- remembering preferences and obligations;
- deciding when another actor needs a reminder;
- monitoring whether delegated work actually happened;
- repairing the plan when it did not;
- maintaining family knowledge and relational work.

Other research on invisible household labor and mental load also documents systematic asymmetries in organizational responsibility.

**Major qualification to the simulation:** assigning execution does not prove that coordination responsibility moved. A person can delegate a task and still retain nearly all anticipation, monitoring and repair burden.

**New analytical distinction:**

```text
execution work
vs
coordination / stewardship work
```

LifeOS should be judged by whether it reduces or fairly redistributes both, not merely whether it assigns visible tasks.

Sources:

- Frampton, Gould & Cox, *The Domestic Operating System: An Empirical Investigation of Digital Technology and Hidden Work in the Home*, CHI 2026: https://doi.org/10.1145/3772318.3791167
- Ciciolla & Luthar, *Invisible Household Labor and Ramifications for Adjustment*: https://doi.org/10.1007/S11199-018-1001-X
- Barigozzi et al., *Beyond Time: Unveiling the Invisible Burden of Mental Load* (2025): https://amsacta.unibo.it/id/eprint/8356/

---

# 10. AI in family coordination can reallocate burden instead of removing it

A collaboration assistant can reduce clicks while increasing supervision work for the person who configures it, maintains context and handles exceptions.

Recent CHI research on parental labor distinguishes physical, cognitive and emotional work and argues for context-sensitive intervention and relationship maintenance rather than simple task automation.

**Implications:**

- measure reduction in coordination burden, not only interaction count;
- avoid creating a permanent household `AI administrator`;
- do not assume automated delegation corrects existing responsibility inequality;
- relationship maintenance can be a legitimate optimization objective alongside throughput.

Sources:

- Wang et al., *Division of Labor and Collaboration Between Parents in Family Education*, CHI 2026 / arXiv: https://arxiv.org/abs/2602.10501
- Frampton et al., CHI 2026, above.

---

# 11. Social invitations: acceptance is not attendance

Research on event invitations shows a gap between online participation decisions and offline attendance. Event type, relationship strength, medium and social context affect actual participation.

Google Calendar's Yes/No/Maybe states provide a practical analogue.

**Finding:** RSVP represents intention/commitment state, not proof of actual participation.

Source:

- Huang, Wang & Yuan, *De-Virtualizing Social Events: Understanding the Gap between Online and Offline Participation for Event Invitations*: https://arxiv.org/abs/1311.0663

---

# 12. Shift scheduling: fairness is procedural and social, not just mathematical

Shift scheduling is an excellent stress test because it combines availability, preference, authority, fairness, substitution and resource capacity.

Research on healthcare scheduling shows that workers can agree abstractly on equality while resolving real conflicts through social negotiation about the importance of individual needs. Transparency, team norms and perceived procedural fairness matter.

Current Microsoft Teams Shifts implements a useful state separation:

```text
worker proposes/request swap
→ coworker accepts or declines
→ manager approves or rejects
→ canonical schedule changes
```

It also supports open shifts, time-off requests, pending states and privacy controls that can hide reasons for absence while still exposing necessary scheduling state.

**Strong confirmation:** recipient acceptance, authority approval and canonical mutation are distinct.

**Guardrail:** algorithmically optimal scheduling can still be perceived as unfair if repeated sacrifices, social context and negotiation are erased.

Sources:

- Uhde et al., *Fairness and Decision-making in Collaborative Shift Scheduling Systems*: https://arxiv.org/abs/2001.09755
- Uhde et al., *Design and Appropriation of Computer-supported Self-scheduling Practices in Healthcare Shift Work*: https://arxiv.org/abs/2102.02132
- Microsoft Teams Shifts requests: https://support.microsoft.com/en-us/teams/free/request-open-shifts-swap-or-offer-shifts-in-shifts
- Microsoft Teams Shifts privacy/settings: https://support.microsoft.com/en-US/Teams/free/configure-settings-for-your-team-s-schedule-in-shifts

---

# 13. Caregiving: awareness, interpretation and responsibility are not interchangeable

Caregiving research supports shared schedules, alerts, task coordination and distributed care networks, but it also exposes a dangerous assumption: logged interaction does not automatically reveal what really happened.

The 2026 *Remindful* work is especially relevant. Reminder interaction data can be affected by:

- another household member responding;
- routine mismatch;
- accessibility barriers;
- technical failures;
- context unavailable to the system.

Therefore a reminder log should not be treated as a neutral behavioral sensor.

**Findings:**

- care coordination needs provenance and uncertainty;
- a caregiver may need interpretation rather than raw logs;
- subject, helper, actor, confirmer and source can differ;
- escalation and hand-off are more important than endless reminders;
- care should remain bounded from clinical authority.

Sources:

- di Fiore et al., family caregiver software needs: https://arxiv.org/abs/1701.07607
- Lai & Mihailidis, *Remindful: Designing Reminder Systems for Caregiver Interpretation in Dementia Care* (2026): https://arxiv.org/abs/2604.19574

---

# 14. Healthcare: a care team is not one homogeneous group

HL7 FHIR represents CareTeam and Consent as distinct resources, reflecting two important facts:

1. multiple actors may participate in care with different roles and time periods;
2. participation does not imply unrestricted information access.

Healthcare privacy guidance also distinguishes patient wishes, professional judgment and necessary disclosure.

**Implications for LifeOS:**

- an external clinical fact can be authoritative without making the clinician an owner of the patient's personal LifeOS;
- a family caregiver can need logistics without needing the entire medical history;
- professional instructions and personal reminders should remain distinguishable;
- participant role, source authority and visibility should not collapse into one concept;
- LifeOS should coordinate around healthcare, not become the clinical system of record.

Sources:

- HL7 FHIR CareTeam: https://hl7.org/fhir/careteam.html
- HL7 FHIR Consent: https://fhir.hl7.org/fhir/consent.html
- HHS HIPAA family/caregiver sharing guidance: https://www.hhs.gov/hipaa/for-professionals/faq/2087/does-hipaa-allow-a-health-care-provider-to-communicate-with-a-patients-family-friends-or-other-persons-who-are-involved-in-the-patient-care.html

---

# 15. Education: legitimate teacher authority can coexist with student agency

Education is a useful counterexample to both `all actors are peers` and `authority means total control`.

Recent HCI work on teacher/student co-orchestration explores hybrid control: teacher guidance can be structurally legitimate while student autonomy increases through the activity.

**Findings:**

- multi-stakeholder agency can change by phase;
- teacher authority over learning structure does not imply ownership of a student's unrelated personal context;
- a shared assignment can have an authoritative external deadline while the student's private execution plan remains local;
- a parent, student, teacher and collaborator may all interact with one requirement through different legitimate views.

Source:

- Yang et al., *Balancing Teacher and Student Agency: Co-Orchestration Tool Design Supporting Real-Time Dynamic Pairing* (2026): https://arxiv.org/abs/2605.18761

---

# 16. Shared expenses: narrow canonical state can work extremely well

Expense-sharing tools such as Splitwise demonstrate a useful pattern: a narrow domain can maintain a shared canonical ledger while letting participants retain independent financial lives.

Relevant concepts include:

- payer;
- beneficiary/participants;
- split rule;
- balance;
- settlement;
- simplification of debts.

**Finding:** shared financial responsibility is common enough to matter, but its success does not justify making LifeOS a general accounting system.

Sources:

- Splitwise: https://www.splitwise.com/
- Getting started: https://kb.splitwise.com/getting-started/how-do-i-use-splitwise
- Simplify debts: https://kb.splitwise.com/balances-and-expenses/what-is-simplify-debts

---

# 17. External participation is a product requirement, not a compatibility afterthought

Calendar and meeting systems support guests who are not members of the host's organization or product ecosystem because real collaboration crosses boundaries.

At the same time, some specialist features — for example workforce scheduling — remain tightly organization-bound. This is a useful contrast.

**Findings:**

- bounded participation should not always require account creation;
- external actors may receive a deliberately reduced interaction surface;
- the minimum viable external experience depends on the responsibility, not on mirroring full LifeOS;
- a provider boundary can remain intact while a shared commitment crosses it.

Sources:

- Google Calendar guests: https://support.google.com/calendar/answer/37161
- Microsoft support, joining a Teams meeting without an account: https://support.microsoft.com/en-us/office/join-a-meeting-without-an-account-in-microsoft-teams-c6efc38f-4e03-4e79-b28f-e65a4c039508
- Microsoft Teams guest access: https://learn.microsoft.com/en-us/microsoftteams/guest-access

---

# 18. Family/care product patterns: broad dashboards validate demand, not necessarily LifeOS identity

Family organizer products typically combine some subset of:

- shared calendars;
- shopping lists;
- to-dos;
- meal planning;
- budgeting;
- location;
- family messaging;
- multiple circles/groups.

This validates broad demand for family coordination, but it also exposes a common product pattern: place everybody inside one shared family surface.

LifeOS has a different opportunity suggested by the simulation and research:

> common shared facts can coordinate **independent personal systems** rather than require every person to live inside one household dashboard.

Care-coordination products such as Lotsa Helping Hands also demonstrate **claimable/open responsibility**: sometimes a task is not assigned to a known person; the useful state is “someone eligible/willing needs to claim this.”

Sources:

- FamilyWall: https://www.familywall.com/en/index.html
- Cozi: https://apps.apple.com/it/app/cozi-family-organizer/id407108860
- Lotsa Helping Hands: https://lls.lotsahelpinghands.com/caregiving/home/

---

# 19. Privacy by design: minimization is directly relevant to coordination

European data-protection guidance strongly supports the simulation's selective-sharing hypothesis.

Privacy by design/default and data minimization imply that systems should process/share what is necessary for a purpose rather than exposing all available context because it is technically convenient.

This has a direct LifeOS translation:

```text
need: coordinate availability
share: free/busy or suitable windows
not automatically: underlying health, relationship, work or personal events
```

Consent is also context-sensitive and can be problematic under power imbalance. Therefore peer-friendship interaction should not be generalized to employer/employee, guardian/minor or caregiver/vulnerable-person contexts.

**Findings:**

- sharing should be purpose-aware;
- revocation belongs to the lifecycle;
- power relationships require additional caution;
- computation from abstract consequences can be safer than disclosure of source facts;
- privacy defaults should minimize unnecessary detail.

Sources:

- EDPB Data Protection by Design and by Default: https://www.edpb.europa.eu/topics/ai-and-technology/privacy-by-design-and-by-default_en
- EDPB SME guidance: https://www.edpb.europa.eu/sme/be-compliant/be-compliant_en
- European Commission GDPR principles: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en
- European Commission consent guidance: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/grounds-processing/when-consent-valid_en

---

# 20. Relationship-based authorization is feasible, but this research does not choose an authorization architecture

The simulations and research produce permissions that are awkward for one global `admin/member/viewer` hierarchy:

- a temporary caregiver can see one child's pickup information;
- a technician can access evidence attached to one visit;
- a friend can edit one trip without accessing the rest of another person's life;
- a former collaborator retains historical attribution but loses future access;
- a family member can see transport logistics without clinical information.

Google Zanzibar and modern relationship-based authorization systems show that user-object relationships and conditions can be modeled at scale.

**Important boundary:** this is feasibility evidence only. It does not justify introducing OpenFGA, Zanzibar-style infrastructure or a complex permission engine before the domain model needs it.

Sources:

- Google Research, *Zanzibar: Google's Consistent, Global Authorization System*: https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/
- OpenFGA concepts: https://openfga.dev/docs/concepts
- OpenFGA conditions: https://openfga.dev/docs/modeling/conditions

---

# 21. Collaboration technology can reproduce power structures

Across calendars, household labor, scheduling, education and caregiving, technology changes:

- who performs coordination work;
- who becomes visible;
- who may interrupt whom;
- who controls shared time;
- whose defaults dominate;
- who must justify exceptions;
- whose assertion becomes canonical.

A technically multi-user system can therefore remain socially single-owner.

**LifeOS-specific risk:** the creator of an item must not automatically gain social authority that does not exist in the real relationship.

Examples:

- creating a dinner does not give the organizer authority to reveal guests' private reasons;
- creating a family event does not make one parent owner of everyone else's calendar;
- an AI creating a proposal does not make that proposal authoritative;
- a caregiver logging an observation does not make it clinical truth;
- a manager's legitimate authority over a shift does not imply access to unrelated personal reasons.

---

# 22. Stress domain A — adversarial exits and technology-facilitated abuse

## 22.1 `Leave group` is not enough

Ordinary collaboration assumes relationships end cooperatively. Real safety guidance and HCI/security research show that shared accounts, location, connected devices and persistent access can be weaponized in coercive relationships.

Apple Safety Check provides an important product pattern:

- review who/what currently receives access;
- review connected devices;
- emergency reset of sharing;
- account/security review.

The lesson is not to copy Apple's UI. It is that **relationship termination can be a safety operation rather than an ordinary membership edit**.

Research on intimate-partner abuse and smart-home/IoT systems further shows that authenticated or apparently legitimate household access can itself become the abuse channel.

**Strong findings:**

- future access revocation must be separable from historical attribution;
- household/family membership is not permanent consent;
- sharing audit must be understandable in human relationship terms;
- revocation may need to be immediate and non-consensual;
- connected assets/devices can leak information indirectly;
- current access and historical participation are different questions;
- revocation semantics must avoid accidentally destroying legitimate history or joint real-world obligations.

Sources:

- Apple Safety Check: https://support.apple.com/guide/personal-safety/safety-check-iphone-ios-16-ips2aad835e1/web
- NNEDV Technology Safety: https://nnedv.org/content/technology-safety/
- NNEDV Safety Net Project: https://www.techsafety.org/
- Leitão, *Anticipating Smart Home Security and Privacy Threats with Survivors of Intimate Partner Abuse*, DIS 2019: https://doi.org/10.1145/3322276.3322366
- Stephenson et al., *It's the Equivalent of Feeling Like You're in Jail*, USENIX Security 2023: https://www.usenix.org/conference/usenixsecurity23/presentation/stephenson-lessons
- Turk & Hutchings, *Spy-oT*, SOUPS 2025: https://www.usenix.org/conference/soups2025/presentation/turk

---

# 23. Stress domain B — ongoing high-conflict collaboration

An adversarial relationship does not always end. Some relationships must continue in a bounded way despite distrust or conflict — post-separation parenting is a strong example.

Research on post-separation parenting apps is especially useful because the tools typically combine:

- documented messaging;
- shared calendars;
- expenses;
- exportable history;
- sometimes third-party/professional access.

A 2025 survey of 140 separated parents — a sample largely characterized by high conflict or fear — found that conflict management was the most common motivation for using such apps. Just over two-thirds reported a mostly positive effect on the relationship, yet messaging and third-party-access features were also identified as the largest contributors to interparental conflict.

This is an important anti-simplification result:

> the same structure that creates accountability and clarity can also intensify conflict or become another arena for power.

**Findings:**

- LifeOS must distinguish `relationship ended` from `relationship remains operational but socially hostile`;
- bounded coordination can be necessary without relational closeness or trust;
- auditability can be useful, but “record everything forever” is not automatically benign;
- communication features can reduce ambiguity while increasing emotional/social pressure;
- third-party access can help mediation/accountability but can also intensify conflict;
- AI should not be assumed capable of solving interpersonal conflict simply because it can rewrite tone;
- structured coordination should minimize unnecessary interaction when the real objective is reliable hand-off, scheduling or evidence.

Sources:

- Payne et al., *Post-Separation Parenting Apps: A Survey of Separated Parents* (2025): https://doi.org/10.1002/anzf.70034
- Smyth et al., *Popular post-separation parenting smartphone apps: An evaluation* (2023): https://doi.org/10.1111/fcre.12738
- Payne & Althor et al., practitioner expectations/experience (2023): https://doi.org/10.1093/lawfam/ebad027

---

# 24. Stress domain C — children, adolescents, guardians and evolving autonomy

Parent–teen privacy research shows that family oversight is negotiated and power-asymmetric, not a simple `parent controls child account` relationship.

Research on joint family oversight found value in transparency/co-management but also surfaced power imbalances and disagreement about acceptable monitoring. Parents were more supportive of collaborative oversight than teens, and teens did not necessarily perceive the relationship as symmetrical.

**Strong findings:**

- child, account holder, subject, guardian, helper and responsible adult are not automatically the same actor;
- legitimate guardian authority does not imply unrestricted visibility across every LifeOS domain;
- autonomy can evolve with age, capability and context;
- education, health, location, social life and household responsibilities may legitimately have different oversight patterns;
- support, safety and surveillance are distinct;
- temporary carers require bounded scope;
- family consent cannot be modeled as if all participants have equal power.

**Boundary:** jurisdiction-specific age/legal rules remain legal/product implementation work and should not be hard-coded from this research.

Sources:

- Akter et al., *From Parental Control to Joint Family Oversight: Can Parents and Teens Manage Mobile Online Safety and Privacy as Equals?* (2022): https://arxiv.org/abs/2204.07749
- Akter et al., *It Takes a Village* (2023): https://arxiv.org/abs/2306.02287

---

# 25. Stress domain D — accessibility, older adults and low digital literacy

External participation is not inclusive merely because it avoids account creation. A “simple link” can still assume:

- good vision;
- precise tapping;
- a modern smartphone;
- strong authentication literacy;
- memory of unfamiliar concepts;
- confidence about what an action will share.

A 2026 JMIR Aging scoping review identifies intersecting challenges around health, usability, confidence, skill and support.

**Findings:**

- essential collaboration should degrade gracefully to simpler interaction modes where appropriate;
- the app UI should not be the universal participation contract;
- possible participation surfaces can range from full app to simplified web/email/SMS/voice/human assistance;
- assisted interaction must preserve who acted and who approved rather than impersonating the subject;
- permission/state complexity itself is an accessibility concern;
- notification and confirmation burden must consider cognitive load;
- mistakes and accidental sharing need easy recovery.

These are product-discovery requirements, not a commitment to implement every channel.

Source:

- Khan et al., *Key Challenges and Barriers to Digital Literacy for Older Adults: Scoping Review*, JMIR Aging 2026: https://aging.jmir.org/2026/1/e80647

---

# 26. Stress domain E — AI-mediated multi-party coordination and privacy

## 26.1 Multi-party AI is not one assistant with a bigger context window

A future LifeOS assistant may know one participant's calendar, another's health constraints, another's budget and shared event facts. A useful coordination result may require those private facts **without revealing the reasons behind them**.

Example:

```text
A: unavailable 18:30–19:30 for a private reason
B: available after 19:00

safe shared result:
20:00 works for both

unsafe explanation:
20:00 is best because A has therapy until 19:30
```

This is the algorithmic form of `share consequence, not reason`.

## 26.2 Multi-party privacy is harder than one-to-one privacy

MuPPET (2026) specifically benchmarks contextual privacy in multi-party conversations and reports substantially greater leakage in multi-party settings than one-to-one evaluation suggests. This is emerging evidence, but directly relevant.

Source:

- Ruzzetti et al., *MuPPET: A Benchmark for Contextual Privacy of LLM Assistants in Multi-Party Conversations* (2026): https://arxiv.org/abs/2606.23217

## 26.3 Tool schemas can create disclosure channels

The PrivateNLP 2026 position paper *From Conventional Web Privacy to Agentic Disclosure* argues that tool-call construction is itself a privacy boundary. Generic free-text parameters can leave disclosure under agent discretion; its case study found 36.9% of analyzed tool specifications exposed at least one such channel.

**Finding:** privacy can fail at the tool/API boundary even if the conversational response looks safe.

Source:

- Shayesteh & Wilson, *From Conventional Web Privacy to Agentic Disclosure: How Tool Schemas May Invite LLM Oversharing*, PrivateNLP 2026: https://aclanthology.org/2026.privatenlp-main.1/

## 26.4 Contextual privacy needs explicit reasoning

`1-2-3 Check` (LLMSEC 2025) explores a multi-agent framework for contextual privacy and reports reduced leakage on its benchmark compared with a single-agent baseline.

This is not an architectural recommendation, but it supports explicit reasoning about:

- who is asking;
- whose information is involved;
- context/purpose;
- minimum necessary disclosure.

Source:

- Li et al., *1-2-3 Check: Enhancing Contextual Privacy in LLM via Multi-Agent Reasoning*, LLMSEC 2025: https://aclanthology.org/2025.llmsec-1.9/

## 26.5 Assistant-to-assistant context exchange should be minimal

Microsoft Research's CONCORD work studies privacy-aware assistant-to-assistant context recovery using minimal relationship-aware queries rather than automatic pooling of all context.

Again, this is emerging architectural research rather than a selected LifeOS design.

Source:

- Srivastava et al., *Listening Alone, Understanding Together: Collaborative Context Recovery for Privacy-Aware AI* / CONCORD (2026): https://arxiv.org/abs/2604.13348

## 26.6 AI access does not create authority

Even a highly informed assistant must preserve distinctions such as:

```text
AI suggestion
participant proposal
participant agreement
external-authority fact
actual outcome
```

The AI's informational access is not social, legal or institutional authority.

## 26.7 Privacy-preserving explanations are a first-order need

When a user asks why a proposed shared time cannot be used, a safe explanation may be:

> Another participant has a private availability constraint.

not the underlying health, relationship or financial reason.

**Strong/important findings:**

- private contexts must not become a pooled shared narrative;
- AI context builders must honor actor-specific access/consent boundaries;
- disclosure should be purpose- and recipient-aware;
- tool/API arguments need the same privacy discipline as UI output;
- AI explanations can leak private causes even when raw fields are hidden;
- cross-participant leakage is separate from leakage to the model provider;
- some coordination is safer deterministically from abstract free/busy/capability facts than by giving AI raw private histories.

---

# 27. Combined synthesis: what external research strongly confirms

External evidence strongly supports the following findings from the simulation.

## 27.1 Shared canonical fact + personal context is a strong direction

A dinner, trip, shift, deadline or appointment can need common facts while each actor maintains different private reminders, travel, goals, capacity effects and notes.

## 27.2 Availability does not require disclosure of underlying calendar content

Calendar research, mature products and privacy guidance converge on this.

## 27.3 Participation is stateful and temporal

Invited, unseen, tentative, accepted, declined, replaced, attended and absent are meaningfully different in different contexts.

## 27.4 Proposal, agreement, authority confirmation and actual outcome differ

Common-ground research, work scheduling and specialist domains strongly reinforce this.

## 27.5 Responsibility is richer than `assigned_to`

Real coordination distinguishes ownership/accountability, execution, claim, approval, hand-off and substitution.

## 27.6 External participants are ordinary

Cross-boundary collaboration is not a failure state.

## 27.7 Privacy must be selective and contextual

Close relationships do not erase the need for minimum-necessary disclosure.

## 27.8 Membership/access/responsibility have lifecycles

People join, leave, substitute, lose access and change role. History and future authority must not be conflated.

## 27.9 Planned and actual participation must remain distinct

RSVP and schedule do not prove reality.

## 27.10 Shared resources matter alongside people

Cars, rooms, equipment, capacity, tickets and facilities are fundamental dependency sources.

## 27.11 Specialist systems must retain their boundaries

LifeOS can coordinate around hospital, school, workforce, legal or provider facts without replacing specialist authority and workflow.

---

# 28. What research strengthens beyond the original simulation

## 28.1 Coordination cost must be evaluated per actor

Ask:

> Who performs additional work and who receives the benefit?

A feature that reduces one organizer's burden by imposing maintenance on six participants deserves skepticism.

## 28.2 Common ground deserves explicit attention

Critical shared changes sometimes need evidence of operational understanding, not merely delivery.

## 28.3 Invisible coordination labor is separate from visible execution

Assignment alone does not transfer anticipation, reminding, monitoring or repair burden.

## 28.4 Fairness is procedural and relational

Equal allocation or optimization can still be experienced as unfair.

## 28.5 Collaborative evidence is situated

A click, reminder response, sensor reading or third-party report may be ambiguous and should retain context/source.

## 28.6 Groups are not homogeneous actors

Families, teams, classrooms and care circles contain different authority, capability and willingness.

## 28.7 Open/claimable responsibility is reusable

Sometimes `someone eligible should take this` is the correct state.

## 28.8 Relationship safety is a lifecycle dimension

Joining and leaving are not sufficient; reduced sharing, scoped revocation and emergency revocation are real states.

## 28.9 Participation capability is a spectrum

Full LifeOS user, occasional user, bounded external responder, assisted participant and non-interacting subject are all realistic positions.

## 28.10 Privacy applies to inference as well as viewing

`Who can see what?` and `who can infer what?` are separate questions, especially with AI and notifications.

---

# 29. Findings that qualify or challenge naive interpretation

These are not contradictions to the central LifeOS hypothesis. They are tensions that must remain visible.

## 29.1 More structure is not always better

Explicit state can reduce ambiguity but create maintenance burden and adoption failure.

## 29.2 More awareness is not always better

Awareness can improve coordination while also enabling surveillance, judgment and interruption.

## 29.3 More transparency is not always better

Sharing private reasons can improve explanation while violating minimization and increasing social pressure.

## 29.4 Equal participation is not always the correct target

Some relationships legitimately include asymmetrical authority or a primary coordinator. The target is appropriate agency and fairness, not forced symmetry.

## 29.5 AI automation can preserve or worsen inequality

Efficiency for visible work can leave one person responsible for configuration, oversight and exceptions.

## 29.6 Consensus is not universally required

Some facts are peer-negotiated, some externally authoritative, some unilateral local choices.

## 29.7 Auditability can help and harm

Persistent records can support high-conflict coordination while also intensifying monitoring, performative communication or conflict.

## 29.8 Revocation can conflict with joint real-world obligations

Stopping future information access does not necessarily terminate legal, parental, financial or ownership responsibilities.

These tensions should be preserved as validation questions, not flattened into one universal rule.

---

# 30. Deeper five-layer lens for multi-actor value

The combined evidence can be organized through five analytical layers.

## Layer A — Shared reality

What facts must multiple actors coordinate around?

Examples: date, location, deadline, decision, shared resource, required outcome.

## Layer B — Dependency

Why must they coordinate?

Examples: simultaneity, prerequisite, producer/consumer, shared resource, hand-off, approval.

## Layer C — Actor relationship

What can each actor legitimately do, know or decide in this context?

Examples: participant, organizer, performer, caregiver, approver, external authority, temporary substitute, guardian.

## Layer D — Personal interpretation

How does the shared reality affect each person's private LifeOS?

Examples: travel, preparation, capacity, private reminder, goal linkage, personal note.

## Layer E — Coordination evidence

How do actors know whether understanding and execution are adequate?

Examples: proposed, delivered, seen, acknowledged, accepted, authoritative, evidence received, attended, disputed.

This is **not** a domain model. It is a research lens for evaluating future domain proposals.

---

# 31. Consolidated risk register

## R1 — Organizer tax reversal

Organizer convenience is achieved by distributing tedious maintenance to everyone else.

## R2 — Digital mental-load trap

LifeOS makes coordination efficient while one actor remains responsible for planning, monitoring and repairing everything.

## R3 — Surveillance through awareness

Availability/location/activity data becomes a way to judge or monitor another person.

## R4 — Notification bureaucracy

Structured collaboration creates more prompts than the original problem justified.

## R5 — False completion / false certainty

Elapsed time, clicks or third-party reports are treated as unquestionable reality.

## R6 — Permission explosion

Accurate privacy semantics become an unusable configuration matrix.

## R7 — Universal-adoption dependency

Important flows break when a participant refuses or cannot use LifeOS.

## R8 — Role overgeneralization

One `admin/member/viewer` hierarchy is stretched across friends, family, work, care and professional relationships.

## R9 — Specialist-system overreach

LifeOS starts reproducing hospital, school, legal, workforce or enterprise administration.

## R10 — Algorithmic unfairness by simplification

Optimization ignores repeated sacrifices, social norms or unequal ability to refuse.

## R11 — Context collapse

Information shared for one purpose becomes available in unrelated collaborative contexts.

## R12 — Relationship-end leakage

Former collaborators retain future visibility.

## R13 — Coercive persistence

A former/abusive relationship retains access because exit was designed only for friendly departure.

## R14 — Guardian overreach

Legitimate guardian responsibility expands into unrelated surveillance.

## R15 — Assisted-user impersonation

A helper's action is recorded as if the subject personally asserted it.

## R16 — Accessibility-by-complexity failure

The model is expressive but unusable by a necessary participant.

## R17 — AI cross-participant leakage

The assistant exposes one person's private reason or history to another.

## R18 — AI authority laundering

An optimization is socially presented as if it were agreement or authoritative fact.

## R19 — Derived privacy leakage

Raw data remains hidden but a recommendation/status/explanation reveals it indirectly.

## R20 — Unsafe revocation semantics

Revocation unintentionally deletes history, breaks legitimate shared ownership/obligations or creates harmful notification behavior.

## R21 — Conflict amplification through tooling

A communication/audit feature intended to reduce conflict becomes another surface for escalation, strategic behavior or pressure.

## R22 — Evidence permanence mismatch

The system retains or exposes collaborative evidence longer or more broadly than the coordination purpose requires.

---

# 32. Consolidated validation questions for future product/domain work

1. Can a participant contribute meaningfully without a full LifeOS account?
2. Can availability be coordinated without exposing underlying private events?
3. Does the capability reduce total coordination burden or only move it?
4. Who performs invisible setup, anticipation, monitoring and repair work?
5. Is the state a proposal, delivery, acknowledgement, agreement, authoritative fact or actual outcome?
6. What dependency is being managed?
7. Does the other actor need the underlying reason or only its consequence?
8. Can responsibility be claimed, delegated, substituted and revoked without rewriting history?
9. Can one shared fact produce different private consequences for each actor?
10. How are conflicting reports and uncertain evidence represented?
11. Does algorithmic coordination preserve procedural fairness and the ability to refuse where appropriate?
12. Is a persistent group actually necessary, or would one bounded shared item be simpler?
13. Does the flow work when only part of the group uses LifeOS?
14. Can access end at an effective point while historical attribution remains?
15. Are notifications providing useful awareness or creating noise?
16. Does the creator accidentally receive social authority they do not possess?
17. Is an external specialist system the actual authority for this fact?
18. What is the minimum information necessary for this responsibility?
19. What happens when the relationship changes, remains high-conflict or becomes adversarial?
20. Can the user inspect/revoke current sharing in human terms rather than ACL language?
21. Does guardian/caregiver authority remain bounded to the context that justifies it?
22. Can a minor's autonomy evolve by time/context?
23. Can a low-digital-literacy participant complete the essential action without learning LifeOS?
24. If one person assists another, is actor/source attribution truthful?
25. Can AI compute a shared recommendation without revealing private inputs?
26. Can AI explain that recommendation without leaking those inputs?
27. Are AI tool schemas constrained enough to avoid generic disclosure channels?
28. Does AI preserve suggestion/agreement/authority/actual distinctions?
29. Does revocation remove AI/context/notification access as well as direct UI access?
30. Can users understand important inferences enabled by sharing, not only raw fields shared?
31. Are emergency privacy controls usable under stress?
32. Can bounded collaboration degrade to simpler channels without corrupting provenance?
33. In high-conflict ongoing relationships, does structure reduce necessary interaction or create a new conflict surface?
34. Is evidence retention proportional to the actual coordination purpose?

---

# 33. Conclusions by confidence

## High confidence

### C1. Multi-user LifeOS cannot be `single-user objects + shared=true`

Actor state, authority, privacy, lifecycle and personal meaning differ materially.

### C2. Shared canonical facts + personal overlays are a strong direction

This is independently supported by calendar privacy, cross-domain coordination and specialist boundaries.

### C3. Proposal, understanding, agreement and actual outcome must not collapse

Not every context exposes every stage, but the semantic distinctions are real.

### C4. Selective disclosure is foundational

The consequence of private context is often enough.

### C5. Participation, responsibility, access and authority have time-bounded lifecycles

Joining/leaving are insufficient abstractions.

### C6. External/partial participants are normal

LifeOS cannot require universal adoption for ordinary coordination.

### C7. Multi-user features must be judged by coordination burden distribution

A technically capable feature can be socially worse if it externalizes work onto participants.

### C8. Specialist systems remain authoritative in their domains

LifeOS should coordinate around them rather than flatten them.

### C9. Revocation and sharing deserve comparable design attention

This becomes safety-critical in some relationships.

## Strong but still product-model work required

### C10. Responsibility likely needs richer semantics than one assignee

Execution, accountability, claim, approval, substitution and hand-off recur too often to ignore, but the exact model remains undecided.

### C11. Common-ground/acknowledgement support is needed for high-consequence changes

It should not become universal bureaucracy.

### C12. Coordination stewardship/mental load deserves explicit treatment

Whether this becomes a domain concept, derived property or product-evaluation metric remains open.

### C13. Assisted/external participation needs truthful provenance

The subject, actor and confirmer can differ.

### C14. Ongoing high-conflict collaboration is distinct from both friendly collaboration and relationship exit

This deserves later validation when shared-family/care models are designed.

## Emerging — track, do not canonize yet

### E1. AI multi-party privacy may require explicit relationship-aware context selection and privacy-preserving explanation

Evidence is directly relevant but recent.

### E2. Multi-agent privacy mechanisms may help, but no orchestration architecture is selected

`1-2-3 Check`, MuPPET and CONCORD are evidence of the problem/design space, not architecture commitments.

### E3. Tool-schema design is itself a privacy control surface

Important for future AI/tool APIs, but implementation belongs to a later technical phase.

---

# 34. What the research does NOT justify

The evidence does **not** justify immediately building:

- enterprise organization administration;
- universal RBAC/ReBAC infrastructure;
- a general social network/feed;
- a mandatory group chat;
- voting/consensus for every decision;
- productivity surveillance;
- family location tracking by default;
- a clinical/legal/school/workforce system;
- mandatory group workspaces;
- complex approval chains for ordinary life;
- automatic AI mediation of interpersonal conflict;
- a universal fairness score;
- universal visibility of history;
- universal evidence permanence;
- a model where organizer/parent/manager/AI automatically owns all decisions.

The research supports a flexible coordination foundation **and simultaneously** supports restraint, progressive disclosure and specialist boundaries.

---

# 35. Quality-control pass

A dedicated QC pass was performed after the broad research and stress-domain research were initially written as two documents.

## 35.1 Structural QC

The separate stress-domain appendix duplicated several themes already present in the main research:

- privacy/minimization;
- relationship lifecycle;
- external participation;
- authority asymmetry;
- AI privacy;
- risk register;
- validation questions.

Those sections are now integrated into this single document. The standalone stress-domain document should no longer be treated as an independent research artifact.

## 35.2 Semantic QC

No evidence family overturns the central simulation hypothesis. The important tensions are retained rather than falsely resolved:

- more structure can reduce ambiguity **and** create bureaucracy;
- more awareness can improve coordination **and** enable surveillance;
- more transparency can improve explanation **and** violate privacy/minimization;
- more automation can reduce visible work **and** increase supervision/mental load;
- auditability can support difficult collaboration **and** amplify conflict;
- equal participation can support agency **but** is not always appropriate where legitimate authority exists;
- revocation can be safety-critical **while** real-world joint obligations may remain.

These are product trade-offs, not contradictions to delete.

## 35.3 Source audit and corrections

High-impact and emerging citations received an explicit verification pass. Several source identifiers in the first draft of the stress research were conceptually correct but bibliographically wrong and have been corrected here:

- MuPPET → arXiv `2606.23217`;
- parent–teen joint oversight → arXiv `2204.07749`;
- JMIR older-adult digital-literacy review → article `e80647`;
- `1-2-3 Check` → ACL Anthology `2025.llmsec-1.9`;
- Agentic Disclosure → ACL Anthology `2026.privatenlp-main.1`, with its correct published title;
- CONCORD → *Listening Alone, Understanding Together*, arXiv `2604.13348`.

The previously unsourced smart-home/IPV claim is now tied to DIS 2019 and USENIX 2023/2025 research.

## 35.4 Evidence-strength QC

The document now explicitly separates:

- established CSCW/HCI findings;
- authoritative standards/regulatory guidance;
- mature product behavior;
- specialist-domain evidence;
- emerging 2025–2026 AI research.

Emerging AI papers are not used as proof of a final LifeOS architecture.

## 35.5 Coverage QC

One materially distinct gap remained after integration: **ongoing high-conflict collaboration that cannot simply be terminated**. Post-separation co-parenting evidence was added because it reveals a different problem from friendly collaboration or hostile exit: participants may need reliable long-term coordination despite distrust.

Other possible research niches — exhaustive group-recommender algorithms, detailed social-choice/voting mechanisms, CRDT/synchronization algorithms, specialist legal doctrine and offline replication architecture — were deliberately not expanded here because they would move from product discovery into narrower product/technical design without materially changing the current foundation.

---

# 36. Final research synthesis

The external evidence does not overturn the simulation. It makes its central result stronger while exposing where naive collaboration design would fail.

The most defensible product hypothesis after simulation, broad research, stress-domain research and QC is:

> **LifeOS should coordinate shared reality among independent people while minimizing coordination burden and unnecessary disclosure, preserving each person's private operating model, representing dependencies/responsibility/authority truthfully, and keeping proposal, understanding, agreement and actual outcome distinct.**

A second principle is equally important:

> **A multi-user feature is not successful merely because it enables collaboration. It is successful only when its coordination benefit exceeds the new social, cognitive, privacy, accessibility and maintenance costs it creates for the actors involved.**

And the stress research adds a third:

> **LifeOS must remain semantically truthful when collaborators are not peers, not friendly, not permanent, not equally digitally capable and not entitled to the private reasons behind one another's constraints.**

For future AI-mediated coordination:

> **Useful inference is not permission to reveal private inputs. AI may help a person's planning from private context, but cross-person disclosure must remain purpose-, recipient- and authority-aware.**

This document is now the **single external multi-actor research artifact** for this workstream. The simulation remains separate because it is a different evidence method. No research term in this document becomes a binding LifeOS domain or architecture concept until a later synthesis/readiness decision explicitly promotes it.

---

# 37. Consolidated source register

## Foundational CSCW / coordination

- Grudin, *Why CSCW Applications Fail*: https://doi.org/10.1145/62266.62273
- Grudin, *Groupware and Social Dynamics*: https://www.microsoft.com/en-us/research/?p=357080
- Malone & Crowston, *What is coordination theory...*: https://doi.org/10.1145/99332.99367
- Malone & Crowston, *The Interdisciplinary Study of Coordination*: https://ccs.mit.edu/papers/CCSWP157.html
- Crowston, coordination/process design: https://doi.org/10.1287/orsc.8.2.157

## Common ground / awareness

- Herbert Clark research overview: https://web.stanford.edu/~clark/research.html
- Clinical common ground: https://pmc.ncbi.nlm.nih.gov/articles/PMC3041298/
- Carroll et al., notification/activity awareness: https://www.sciencedirect.com/science/article/pii/S1071581903000247
- Awareness displays/social motivation: https://doi.org/10.1287/isre.1080.0175
- Collaborative information-seeking awareness: https://doi.org/10.1002/asi.22819

## Calendar / family

- Palen, groupware calendar privacy: https://doi.org/10.1145/302979.302982
- Neustaedter et al., family calendar: https://doi.org/10.1145/1502800.1502806
- LINC participatory design: https://www.microsoft.com/en-us/research/publication/linc-ing-the-family-the-participatory-design-of-an-inkable-family-calendar/
- LINC field trial: https://graphicsinterface.org/proceedings/gi2007/gi2007-27/
- Outlook sharing: https://support.microsoft.com/en-us/outlook/sharing/share-an-outlook-calendar-as-view-only-with-others
- Outlook delegation: https://support.microsoft.com/en-us/outlook/sharing/about-delegates-allow-someone-to-manage-your-mail-and-calendar-in-outlook
- Google Calendar invitations: https://support.google.com/calendar/answer/37161

## Household / mental load

- Frampton et al., *The Domestic Operating System*, CHI 2026: https://doi.org/10.1145/3772318.3791167
- Ciciolla & Luthar, invisible household labor: https://doi.org/10.1007/S11199-018-1001-X
- Barigozzi et al., *Beyond Time*: https://amsacta.unibo.it/id/eprint/8356/
- Wang et al., parental labor/collaboration, CHI 2026: https://arxiv.org/abs/2602.10501

## Social participation

- Huang et al., online invitation vs offline participation: https://arxiv.org/abs/1311.0663

## Work / shifts

- Uhde et al., fair collaborative shift scheduling: https://arxiv.org/abs/2001.09755
- Uhde et al., self-scheduling practices: https://arxiv.org/abs/2102.02132
- Microsoft Teams Shifts requests: https://support.microsoft.com/en-us/teams/free/request-open-shifts-swap-or-offer-shifts-in-shifts
- Microsoft Teams Shifts privacy/settings: https://support.microsoft.com/en-US/Teams/free/configure-settings-for-your-team-s-schedule-in-shifts

## Caregiving / healthcare

- di Fiore et al., family caregiver software needs: https://arxiv.org/abs/1701.07607
- Lai & Mihailidis, *Remindful*: https://arxiv.org/abs/2604.19574
- HL7 FHIR CareTeam: https://hl7.org/fhir/careteam.html
- HL7 FHIR Consent: https://fhir.hl7.org/fhir/consent.html
- HHS HIPAA family/caregiver sharing: https://www.hhs.gov/hipaa/for-professionals/faq/2087/does-hipaa-allow-a-health-care-provider-to-communicate-with-a-patients-family-friends-or-other-persons-who-are-involved-in-the-patient-care.html

## Education

- Yang et al., teacher/student agency and co-orchestration: https://arxiv.org/abs/2605.18761

## Shared expenses / family / care products

- Splitwise: https://www.splitwise.com/
- Splitwise getting started: https://kb.splitwise.com/getting-started/how-do-i-use-splitwise
- Splitwise simplify debts: https://kb.splitwise.com/balances-and-expenses/what-is-simplify-debts
- FamilyWall: https://www.familywall.com/en/index.html
- Cozi: https://apps.apple.com/it/app/cozi-family-organizer/id407108860
- Lotsa Helping Hands: https://lls.lotsahelpinghands.com/caregiving/home/

## External participation

- Google Calendar non-platform guests: https://support.google.com/calendar/answer/37161
- Microsoft support, joining a Teams meeting without an account: https://support.microsoft.com/en-us/office/join-a-meeting-without-an-account-in-microsoft-teams-c6efc38f-4e03-4e79-b28f-e65a4c039508
- Microsoft Learn, Teams guest access: https://learn.microsoft.com/en-us/microsoftteams/guest-access

## Privacy / authorization

- EDPB Privacy by Design/Default: https://www.edpb.europa.eu/topics/ai-and-technology/privacy-by-design-and-by-default_en
- EDPB SME guidance: https://www.edpb.europa.eu/sme/be-compliant/be-compliant_en
- European Commission GDPR principles: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en
- European Commission consent guidance: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/grounds-processing/when-consent-valid_en
- Zanzibar: https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/
- OpenFGA concepts: https://openfga.dev/docs/concepts
- OpenFGA conditions: https://openfga.dev/docs/modeling/conditions

## Safety / adversarial relationships

- Apple Safety Check: https://support.apple.com/guide/personal-safety/safety-check-iphone-ios-16-ips2aad835e1/web
- NNEDV Technology Safety: https://nnedv.org/content/technology-safety/
- NNEDV Safety Net: https://www.techsafety.org/
- Leitão, smart-home threats with intimate-partner-abuse survivors: https://doi.org/10.1145/3322276.3322366
- Stephenson et al., IoT-enabled intimate-partner abuse: https://www.usenix.org/conference/usenixsecurity23/presentation/stephenson-lessons
- Turk & Hutchings, *Spy-oT*: https://www.usenix.org/conference/soups2025/presentation/turk

## Ongoing high-conflict collaboration / co-parenting

- Payne et al., *Post-Separation Parenting Apps: A Survey of Separated Parents* (2025): https://doi.org/10.1002/anzf.70034
- Smyth et al., *Popular post-separation parenting smartphone apps: An evaluation* (2023): https://doi.org/10.1111/fcre.12738
- Payne et al., family-law practitioner expectations/experience (2023): https://doi.org/10.1093/lawfam/ebad027

## Children / family privacy

- Akter et al., joint parent–teen oversight: https://arxiv.org/abs/2204.07749
- Akter et al., extended-family oversight: https://arxiv.org/abs/2306.02287

## Accessibility / digital literacy

- Khan et al., *Key Challenges and Barriers to Digital Literacy for Older Adults*, JMIR Aging 2026: https://aging.jmir.org/2026/1/e80647

## Multi-party AI/privacy — emerging evidence

- Ruzzetti et al., MuPPET: https://arxiv.org/abs/2606.23217
- Shayesteh & Wilson, *From Conventional Web Privacy to Agentic Disclosure*: https://aclanthology.org/2026.privatenlp-main.1/
- Li et al., *1-2-3 Check*: https://aclanthology.org/2025.llmsec-1.9/
- Srivastava et al., CONCORD / *Listening Alone, Understanding Together*: https://arxiv.org/abs/2604.13348
