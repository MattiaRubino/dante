# LifeOS — Multi-Actor / Collaboration Discovery Simulation

**Date:** 11 August 2026  
**Status:** Product study / discovery evidence  
**Scope:** discover reusable multi-user, multi-actor and collaboration needs through realistic people and situations, without turning the study into an implementation specification.  
**Relationship to previous study:** complements `feature-discovery-simulation-2026-08.md`. The previous study explored broad single-user and cross-domain needs; this study keeps the same discovery logic but focuses exclusively on situations involving multiple people, responsibilities, shared facts, shared resources or coordinated action.

## Purpose

The goal is not to list collaboration features that LifeOS could copy from existing products.

The goal is to simulate what different people actually need when their plans, responsibilities, information, resources or outcomes depend on other people, and then identify which needs recur across unrelated domains.

The study deliberately uses two complementary lenses:

1. **persona-driven discovery** — for each kind of person, identify the multi-user situations they may face, what they would want LifeOS to help with, and which reusable capabilities emerge;
2. **scenario-driven discovery** — simulate realistic situations first without LifeOS and then with LifeOS, actor by actor, including failures, changes, non-users and privacy boundaries.

Neither lens replaces the other. A persona can participate in many scenarios, and the same scenario can produce very different needs for different actors.

## Study boundaries

This document is discovery evidence, not a binding architecture or V2 specification.

It therefore does **not** decide:

- database tables or physical schema;
- ACL or authorization implementation;
- organization/account hierarchy;
- exact invitation protocols;
- exact synchronization mechanics;
- chat or messaging architecture;
- final UI;
- pricing or packaging;
- whether a capability belongs to V1, V2 or a later release.

Those decisions may use this study as evidence later.

The study also intentionally does not perform external product or academic research. That should be a separate follow-up so that existing products do not bias the initial discovery.

## Discovery principles

- Start from the real situation, not from a desired feature.
- Treat every actor as a person with their own goals, context and boundaries, not as a subordinate of the scenario creator.
- Do not assume every participant uses LifeOS.
- Do not assume every participant wants the same amount of information or control.
- Do not assume collaboration means exposing a full calendar, profile, goal, history or personal context.
- Do not assume sharing is always desirable; a useful system must also support non-sharing and partial participation.
- Distinguish a fact that is genuinely shared from the personal meaning, reminders, notes and planning surrounding that fact.
- Test normal flow and disruption: refusal, silence, cancellation, late entry, early exit, conflicting changes, temporary delegation and unavailable resources.
- Follow relationships over time when useful: groups form, roles change, people leave, responsibility transfers and relationships may end.
- A result that shows little or no LifeOS advantage is valid evidence.
- The product should reduce coordination friction without pretending to solve human disagreement, trust or responsibility automatically.

## Standard simulation frame

For detailed scenarios the study uses the following frame:

1. **Real context and actors** — who is involved and why.
2. **Without LifeOS** — how the situation can realistically unfold today.
3. **Actor-by-actor needs** — what each person wants to know, decide, do, avoid or keep private.
4. **With LifeOS** — replay the same situation and observe where LifeOS could reduce friction.
5. **Stress variation** — introduce realistic change, failure or disagreement.
6. **What improves / what does not** — identify actual value rather than assuming it.
7. **Capabilities that emerge** — record reusable needs only after the simulation.

---

# Part I — Persona-driven multi-user discovery

This section mirrors the logic of the earlier feature-discovery study: **type of person → what they must coordinate with others → what they would want to do with LifeOS → reusable capabilities that emerge**.

The categories are discovery prompts, not profiles that LifeOS must impose on users.

## Study and knowledge

### Student

**Multi-user reality:** lessons, group assignments, study groups, project partners, tutors, professors, exam information, shared material, classmates travelling to the same campus, roommates and family commitments that compete with study.

**What the student may want from LifeOS:** coordinate a study session without exposing their full calendar; share only the agreed session while keeping a personal preparation plan private; divide group-project work; know who owns each deliverable; see when another person's delay blocks their own task; receive changes to lessons or deadlines; keep personal notes around a shared class or event; propose alternative times; coordinate shared files, travel or expenses; keep commitments involving classmates visible alongside personal goals.

**Emerges:** selective availability, participant state, shared facts plus personal overlays, responsibility, dependency across people, proposal/acceptance, shared milestones, external participants, shared material and personal follow-up.

### Teacher / lecturer / researcher

**Multi-user reality:** classes, office hours, students, co-authors, reviewers, research groups, shared experiments, conferences, corrections, teaching assistants and institutional deadlines.

**What they may want from LifeOS:** publish or share canonical times and deadlines without sharing private workload; coordinate office-hour requests; manage co-authored milestones; distinguish a group deadline from each person's private preparation; see expected contributions and actual hand-offs; request review; acknowledge receipt; coordinate resources such as rooms or equipment; preserve who changed a shared decision and why.

**Emerges:** audience-scoped information, role-dependent views, request/review/approval, hand-off, shared resources, decision history, contribution state and canonical-vs-personal context.

### Language learner / peer-learning participant

**Multi-user reality:** conversation partners, tutors, teachers, study groups, language exchanges and certification preparation.

**What they may want from LifeOS:** find mutually suitable practice slots, maintain a personal learning program while sharing only the joint session, exchange preparation material, alternate responsibility for topics, record whether the session actually happened, keep private performance notes, repeat sessions with the same group and invite occasional external participants.

**Emerges:** recurring shared activity with personal progress, limited disclosure, actual participation, optional shared evidence, group continuity and private reflection.

## Work and operations

### Software developer / knowledge worker

**Multi-user reality:** meetings, pair work, incidents, reviews, dependencies, hand-offs, shared deadlines, stakeholders and interruptions caused by other people's work.

**What they may want from LifeOS:** know which personal tasks depend on another person's delivery; request or accept review; coordinate a meeting around free/busy rather than raw calendar detail; hand work to someone else; track commitments made in meetings; keep personal deep-work scheduling private while exposing only necessary availability; receive a change that affects them without copying an entire team plan into their personal system.

**Emerges:** cross-person dependency, review request, hand-off, commitment extraction, selective synchronization, acknowledgement and personal scheduling around shared commitments.

### Manager / team lead

**Multi-user reality:** team outcomes, assignments, approvals, one-to-ones, capacity differences, vacations, blocked work and changing priorities.

**What they may want from LifeOS:** coordinate responsibilities without owning each person's private calendar; know whether a shared commitment is accepted, blocked or at risk; propose work rather than silently inserting it into another person's day; distinguish team progress from individual private goals; delegate responsibility; transfer ownership when roles change; understand which decisions are waiting for approval.

**Emerges:** proposal rather than unilateral assignment, responsibility transfer, shared outcome with personal execution, scoped capacity signals, approval, escalation and status visibility without full personal exposure.

### Shift worker / healthcare worker / operations worker

**Multi-user reality:** fixed shifts, rotating teams, coverage requirements, absences, swap requests, on-call periods and minimum staffing.

**What they may want from LifeOS:** request a swap; see whether coverage is still satisfied without exposing colleagues' full lives; accept or refuse a replacement; keep a personal recovery plan private; receive authoritative shift changes; know when a swap is provisional versus confirmed; preserve who was actually present.

**Emerges:** coverage requirement, role/capability matching, swap workflow, provisional/confirmed state, actual participation, authority and change acknowledgement.

### Field technician

**Multi-user reality:** customer, dispatcher, colleague, site contact, equipment, access windows, parts and follow-up.

**What they may want from LifeOS:** share appointment facts with the customer while keeping internal work notes private; coordinate arrival windows; hand a job to another technician; request access or confirmation; attach evidence; identify which materials are provided by whom; notify affected people when timing changes; preserve actual attendance and completion evidence.

**Emerges:** multi-party appointment, public/shared vs internal information, resource responsibility, external participant, evidence exchange, transfer and actual work record.

### Freelancer / consultant

**Multi-user reality:** several clients, subcontractors, review cycles, deliverables, meetings, invoices and dependencies.

**What they may want from LifeOS:** expose client-facing milestones without exposing the rest of their workload; request client review; keep internal preparation private; coordinate subcontractors; record approval and revision history; distinguish the client's due date from their own earlier internal deadline; terminate access cleanly when a project finishes.

**Emerges:** boundary between internal and external project state, review/approval, temporary collaboration, scoped visibility, client-facing canonical milestones and access lifecycle.

### Small business owner / shop operator

**Multi-user reality:** employees, suppliers, customers, deliveries, stock, shifts, accountant, maintenance providers and family help.

**What they may want from LifeOS:** coordinate recurring responsibilities, temporary substitutions, supplier deliveries and maintenance; know which shared resource or stock issue affects planned work; let an external professional see only the relevant record; keep financial/private data separate from staff-facing operations.

**Emerges:** resource-aware coordination, recurring responsibility, external professional access, operational role, limited view and responsibility continuity.

## Household, family and personal life

### Partner / cohabiting adult

**Multi-user reality:** groceries, household tasks, bills, appointments, visits, trips, shared purchases, maintenance and personal commitments.

**What they may want from LifeOS:** maintain their own personal LifeOS while coordinating household facts; know whether a task is mine, yours, either person's or genuinely joint; claim an unassigned chore; share a grocery list without sharing unrelated goals; coordinate bills and maintenance; keep surprise plans or private notes private; avoid duplicate purchases; transfer responsibility when one person is unavailable.

**Emerges:** shared household context without merged identities, joint/individual responsibility, claimable work, shared list/resource, privacy inside close relationships and duplicate prevention.

### Parent / guardian

**Multi-user reality:** partner or co-parent, children, school, grandparents, babysitters, doctors, sports coaches and family logistics.

**What they may want from LifeOS:** coordinate pickups and appointments; know who is responsible today; hand off a child-related task; share selected facts with a grandparent or babysitter; keep adult private information hidden; record consent or required documents; handle a co-parent who may not use LifeOS; change responsibility when plans fail.

**Emerges:** subject distinct from actor, guardianship/authority context, delegated temporary responsibility, minimum-necessary sharing, external participant and hand-off confirmation.

### Caregiver

**Multi-user reality:** cared-for person, family, doctors, pharmacy, paid carers, appointments, medications, supplies and observations.

**What they may want from LifeOS:** coordinate who does what; know whether a medication-related action was actually confirmed; separate the cared-for person's data from each caregiver's private notes; share only clinically or practically relevant information; hand over a shift; flag uncertainty instead of assuming completion; handle conflicting reports.

**Emerges:** subject-centric collaboration, sensitive-data boundaries, actual confirmation, hand-over, conflicting evidence, role-limited access and escalation.

### Older or low-digital participant

**Multi-user reality:** family help, appointments, deliveries, community activities and occasional professional support.

**What they may want from LifeOS:** participate without mastering a complex collaboration system; accept or decline simply; receive clear reminders; allow a trusted person to help with selected things without giving unrestricted control; continue through SMS/email/link/printed information when they do not use LifeOS directly.

**Emerges:** assisted participation, delegated help with limits, external-channel participation, simple confirmation and accessibility asymmetry.

### Traveller / trip organizer

**Multi-user reality:** friends or family, bookings, transport, rooms, tickets, expenses, documents and changing schedules.

**What they may want from LifeOS:** coordinate dates without exposing full calendars; keep shared itinerary facts synchronized; let each participant add personal travel to/from the shared trip; track who booked or paid; manage people joining only part of the trip; preserve private documents; handle cancellations and replacement bookings.

**Emerges:** bounded shared container, partial participation windows, shared itinerary plus personal travel, responsibility/payment state, selective document sharing and change propagation.

### Athlete / hobby participant / club member

**Multi-user reality:** coach, training partners, teammates, club events, equipment, facilities and competitions.

**What they may want from LifeOS:** share attendance or planned joint sessions while keeping personal health data private; coordinate facility or equipment availability; let a coach propose sessions without automatically controlling the athlete's entire calendar; record actual attendance; manage temporary team membership.

**Emerges:** coaching proposal, private performance context, shared resource booking, attendance, temporary membership and consent boundaries.

## Creative work and events

### Musician / creator

**Multi-user reality:** bandmates, producer, designer, distributor, venue, collaborators and audience-facing deadlines.

**What they may want from LifeOS:** coordinate a release or rehearsal while preserving each collaborator's private planning; assign or claim deliverables; request review; freeze approved versions; distinguish internal and public dates; invite one-off collaborators; preserve who approved what.

**Emerges:** collaborative milestone, approval/version checkpoint, temporary collaborator, shared asset state and internal/public timeline distinction.

### Photographer / videographer

**Multi-user reality:** client, subject/model, assistant, venue, makeup artist, second shooter, editor and delivery contacts.

**What they may want from LifeOS:** coordinate date/location and call time; share only relevant preparation; confirm model releases or required documents; track equipment responsibility; hand off editing; keep client-facing delivery status separate from private creative notes; handle weather-triggered changes across all affected people.

**Emerges:** multi-role event, prerequisite acknowledgement, resource responsibility, external-condition change propagation, client/internal boundary and hand-off.

### Writer / researcher / editor

**Multi-user reality:** co-authors, editors, reviewers, sources and publishers.

**What they may want from LifeOS:** share milestones and review requests; keep private notes private; know which version is under review; record accepted/rejected changes; coordinate interviews with external people; close access after publication.

**Emerges:** review state, version-under-discussion, external interview participant, decision history and collaboration lifecycle.

### Event organizer

**Multi-user reality:** attendees, venue, performers, suppliers, volunteers, security, transport and payments.

**What they may want from LifeOS:** maintain one set of canonical event facts while giving each actor only the details relevant to them; coordinate arrival and responsibilities; know who acknowledged changes; handle replacements; manage shared resources and prerequisites; preserve private attendee or supplier data.

**Emerges:** canonical shared event, role-scoped views, acknowledgement, replacement, dependency/resource coordination and selective disclosure.

## Production, property and shared resources

### Farmer / small producer

**Multi-user reality:** family workers, employees, contractors, suppliers, buyers, shared machinery and weather-dependent work.

**What they may want from LifeOS:** coordinate work windows and machine availability; assign or claim responsibility; know whether inputs arrived; hand work to another person; share only the relevant field/task details with a contractor; respond to weather changes without exposing unrelated business data.

**Emerges:** shared asset capacity, contractor-limited view, dependency on external delivery, reassignment and condition-triggered coordination.

### Artisan / workshop operator

**Multi-user reality:** customer, workers, suppliers, outsourced specialists and delivery partners.

**What they may want from LifeOS:** expose order milestones to a customer without exposing internal costs; coordinate production stages across people; record who performed or approved a stage; manage material shortages; transfer a job when someone is absent.

**Emerges:** customer-facing status, internal workflow privacy, actual contributor, quality approval, resource dependency and continuity of responsibility.

### Shared vehicle / property owner or user

**Multi-user reality:** partners, family, roommates, renters, mechanics, cleaners and service providers.

**What they may want from LifeOS:** know who is using the resource and when; coordinate maintenance; record fuel/charge/condition or damage; distinguish private trip purpose from shared availability; allocate costs; grant temporary access to a mechanic without exposing household information.

**Emerges:** resource reservation, shared condition history, private purpose vs shared occupancy, temporary service-provider access and cost responsibility.

## Professional and sensitive relationships

### Patient

**Multi-user reality:** clinicians, caregiver, family, pharmacy, diagnostic services and appointments.

**What they may want from LifeOS:** coordinate relevant appointments and preparation while retaining authority over who sees personal data; let a caregiver help with selected tasks; receive clinician-provided instructions without confusing them with personal notes; record whether preparation or medication actions actually occurred; revoke access later.

**Emerges:** sensitive selective sharing, source/authority distinction, delegated assistance, actual confirmation and revocable participation.

### Doctor / clinician

**Multi-user reality:** patient, colleagues, nurses, assistants, facilities and other services.

**What they may want from LifeOS:** coordinate personal work commitments and patient-facing logistics without turning LifeOS into a clinical record system; distinguish authoritative professional instructions from patient-generated notes; manage team participation and resource availability; preserve confidentiality and minimum disclosure.

**Emerges:** professional authority/source, specialist-system boundary, role-specific coordination, resource capacity and privacy constraints.

### Teacher / school-side coordinator

**Multi-user reality:** students, parents, other teachers, school administration, rooms, activities and trips.

**What they may want from LifeOS:** distribute canonical dates and required actions; collect acknowledgements; coordinate parent/student responsibilities; handle a child whose parents use different systems; avoid exposing one family's data to another; support temporary group activities.

**Emerges:** audience segmentation, guardian/subject distinction, acknowledgement, temporary group, institutional source and family privacy.

### Technician / professional service provider

**Multi-user reality:** customer, site contact, dispatcher, colleague, supplier and follow-up professional.

**What they may want from LifeOS:** coordinate access and appointment windows; request preparation from the customer; show only customer-relevant status; preserve internal technical notes; record actual service and evidence; transfer follow-up responsibly.

**Emerges:** prerequisite request, external confirmation, customer/internal boundary, evidence and hand-over.

### Lawyer / client or other confidential adviser relationship

**Multi-user reality:** client, advisers, counterparties, courts/institutions, assistants and deadlines.

**What they may want from LifeOS:** coordinate dates, document requests and client actions without exposing confidential internal reasoning; distinguish authoritative deadlines from reminders; track acknowledgement and document delivery; tightly limit who sees what; close or archive collaboration when the matter ends.

**Emerges:** high-sensitivity scope, authoritative source, document request/receipt, constrained sharing, matter lifecycle and auditable acknowledgement.

---

# Part II — Scenario-driven real-life simulations

## Level 1 — Social coordination

### Scenario 1 — Dinner with friends

**Context and actors**  
Six friends want dinner on Saturday. One person starts the idea. Two have children and uncertain timing. One works shifts. One dislikes planning apps. One will join only if the restaurant is near public transport.

**Without LifeOS**  
The proposal starts in a group chat. Three people answer quickly, two answer hours later and one does not answer. Several dates are mentioned in different messages. Someone starts a poll. A restaurant link is posted, then another. One person says “I should be free” but later discovers another commitment. The organizer eventually books for six, then changes it to five. The final time is buried between unrelated messages. Two people separately add slightly different times to their calendars. One assumes the booking is at 20:30, another at 21:00. The organizer has to remind everyone manually.

**Actor-by-actor needs**

- The organizer wants a clear decision and final headcount without repeatedly asking everyone.
- The shift worker wants to expose only whether proposed windows work, not their work calendar.
- The parents want to answer provisionally until childcare is confirmed.
- The transport-sensitive participant wants location to be part of the decision, not an afterthought.
- The low-digital participant wants one simple final message rather than another system to maintain.
- Everyone wants the final agreed facts to be clear once a choice is made.

**With LifeOS**  
The organizer creates a social plan with several possible windows and two restaurant options. LifeOS asks each participant only for the information needed to answer those options. Participants can mark yes, no or provisional without exposing why. One person receives a simple external link instead of needing an account. When a combination reaches agreement, the organizer confirms the canonical dinner facts. Each LifeOS user then decides how the dinner appears locally, what personal reminder they want and whether travel time should be added. The provisional parent becomes confirmed later. Only the headcount update is propagated to the organizer; the reason remains private.

**Stress variation**  
At 17:00 on Saturday the restaurant changes the booking to 21:00. Some participants can still attend, one cannot. The changed shared fact requires acknowledgement rather than silently overwriting six private calendars. A participant proposes an alternative restaurant; it remains a proposal until accepted instead of becoming the new truth by whoever edited last.

**What improves / what does not**  
LifeOS can reduce message archaeology, duplicated calendar entry, repeated availability questions and ambiguity about the final decision. It cannot decide whether friends prefer one restaurant, force people to answer or eliminate social negotiation.

**Capabilities that emerge**  
Availability without full-calendar disclosure; invitation and response state; provisional participation; proposal vs confirmed shared fact; acknowledgement of material change; external participant; personal reminder/travel overlay; headcount derived from participation.

### Scenario 2 — Weekend trip with mixed participation

**Context and actors**  
Seven friends plan a three-night trip. Five travel from the same city, one arrives one day later and one leaves early. Two people use LifeOS heavily, three only lightly and two do not use it. One person pays the accommodation deposit. Different people book transport.

**Without LifeOS**  
Planning spreads across chat, booking emails, screenshots, a notes app and individual calendars. The accommodation address is copied several times. Flight and train changes are communicated manually. People ask repeatedly who has paid, who arrives when and whether airport transfer should wait for the late participant. Some travel documents are shared too broadly in the group chat. One participant thinks a shared excursion is mandatory although it was only an idea. The organizer becomes the human source of truth.

**Actor-by-actor needs**

- The main organizer wants one reliable trip overview without owning everyone's personal travel plan.
- The late-arriving participant wants only the shared facts that apply after arrival plus their own private route.
- The person who paid wants a clear reimbursement state.
- Other participants want to know what is confirmed, optional or still proposed.
- Non-LifeOS participants need access to essential itinerary facts without joining the platform.
- Everyone needs personal documents to remain private unless explicitly shared.

**With LifeOS**  
The trip has shared canonical facts: accommodation, agreed shared activities, check-in constraints and group transport decisions. Each participant attaches their own arrival/departure facts at the level they choose to share. LifeOS can answer “who is physically present for this activity?” without exposing unrelated calendar details. Shared costs record payer, expected contributors and settlement state. Booking documents can be private, selectively shared or represented only by safe derived facts such as confirmation time and address. Optional activities remain proposals until a person joins them.

**Stress variation**  
A flight cancellation means two people arrive six hours late. Their personal travel changes affect one shared airport-transfer decision but not the rest of the trip. LifeOS should propagate only the relevant consequence. Later one participant cancels the final night; cost sharing and room assumptions need review rather than silent recalculation that nobody understands.

**What improves / what does not**  
LifeOS can reduce duplicate itinerary data, over-sharing, repeated “who arrives when?” questions and unclear cost responsibility. It does not replace booking providers or guarantee fair expense decisions.

**Capabilities that emerge**  
Bounded shared plan; partial participation periods; shared canonical facts plus personal travel; selective document disclosure; shared cost obligation; consequence propagation; optional sub-activities; external access; change review.

### Scenario 3 — Concert with scarce tickets

**Context and actors**  
Four friends want tickets for a popular concert. One person has presale access and agrees to buy. Ticket availability changes quickly. One friend is uncertain because of work.

**Without LifeOS**  
The buyer asks who is definitely in. Messages arrive at different times. Tickets appear for sale. The uncertain friend says “buy if you can,” but the acceptable price limit is unclear. The buyer purchases four seats and later discovers one person cannot attend. Resale and repayment become separate conversations. Everyone stores ticket information differently.

**Actor-by-actor needs**

- The buyer wants explicit authority to purchase within an agreed limit.
- The uncertain participant wants to express conditional commitment.
- Everyone wants clarity on money owed and ticket ownership.
- Each attendee wants the final event in their own calendar without exposing unrelated plans.

**With LifeOS**  
Participants can express confirmed, conditional or declined participation and, if appropriate, a maximum approved spend. The designated buyer receives a clear delegated action, not an ambiguous chat promise. After purchase, each ticket or entitlement has a current holder. Payment obligations are visible only to relevant people. A later transfer changes ticket responsibility while preserving what happened historically.

**Stress variation**  
The uncertain friend drops out. Another friend joins. The ticket transfers without rewriting the original purchase history or pretending the new person was part of the original commitment.

**Capabilities that emerge**  
Delegated action with explicit limits; conditional commitment; shared financial obligation; transferable entitlement; historical ownership; participant replacement.

---

# Level 2 — Household and family

### Scenario 4 — Shared household week

**Context and actors**  
Two adults live together. Both work. They share groceries, cleaning, bills, maintenance and some social plans but keep independent goals, work calendars, finances and personal notes.

**Without LifeOS**  
Tasks live in memory, chat messages, a fridge note and separate apps. Both occasionally buy the same item. A utility bill is assumed to be the other person's responsibility. A plumber appointment is booked but the person who must be home does not know the access window changed. One partner becomes the default household coordinator because they remember more things.

**Actor-by-actor needs**

- Both want a common household picture without merging their personal LifeOS data.
- Either person should be able to claim an unowned chore.
- Some responsibilities are fixed, some alternate and some are genuinely joint.
- Surprise gifts, private health items and personal finances must remain private.
- A service provider may need the address and access time but nothing else.

**With LifeOS**  
Household items exist as shared facts only where sharing creates value. Groceries, selected bills, maintenance and chores can be joint. Each person's personal schedule remains their own. A chore can be unassigned, assigned, jointly responsible or claimable. The plumber sees only the appointment/access information sent externally. When one partner is travelling, responsibilities can temporarily transfer or be renegotiated instead of silently failing.

**Stress variation**  
Both partners edit the maintenance appointment near the same time, based on different phone calls. LifeOS should surface the conflict or source difference rather than accept the last write as unquestioned truth. Later they decide to stop sharing one financial category; historical shared facts remain understandable while future sharing changes.

**What improves / what does not**  
LifeOS can reduce invisible mental load, duplication and responsibility ambiguity. It cannot make household labour fair by itself or infer agreement where none exists.

**Capabilities that emerge**  
Shared context without merged identity; claimable responsibility; recurring/alternating responsibility; external service participant; privacy within close relationships; conflict detection; future-effective sharing change.

### Scenario 5 — Family logistics around a child

**Context and actors**  
Two parents coordinate school, sports, medical appointments and pickups for a child. A grandparent helps on Thursdays. The school and sports coach do not use LifeOS.

**Without LifeOS**  
Information arrives by school email, messaging groups, paper notices and coach messages. One parent forwards some items to the other. Pickup changes are agreed in chat. The grandparent sees only some updates. A permission slip is forgotten because each parent assumes the other handled it. The child's calendar exists as fragments in several adult calendars.

**Actor-by-actor needs**

- The child-related plan needs continuity regardless of which adult performs each action.
- Each parent needs to know current responsibility without sharing unrelated personal details.
- The grandparent needs only Thursday-relevant logistics.
- School-originated facts should remain distinguishable from parent interpretation.
- Sensitive child information should not leak into general family sharing.

**With LifeOS**  
The child is the subject of relevant commitments, but each adult remains a separate actor. A school event can be imported or recorded with source provenance. Pickup responsibility is explicit and can be handed over. The grandparent receives a limited view or external notification for their relevant period. A permission form is a required action with an owner and receipt state rather than a vague message. Each parent can keep private notes around the same shared event.

**Stress variation**  
The responsible parent becomes unavailable two hours before pickup. A hand-off request goes to the other parent and grandparent. Until someone accepts, LifeOS treats pickup coverage as unresolved rather than assuming the message was seen.

**Capabilities that emerge**  
Subject distinct from participant; guardianship context; source provenance; delegated responsibility; limited helper access; required acknowledgement; unresolved coverage; private overlays.

### Scenario 6 — Shared car and pet

**Context and actors**  
A couple shares one car and a dog. A sibling sometimes borrows the car. A dog walker helps twice a week. A mechanic and vet are occasional external actors.

**Without LifeOS**  
Car availability is discussed ad hoc. Fuel level and minor damage are remembered inconsistently. Maintenance reminders are on one person's phone. Dog medication and walks are confirmed by chat. The sibling borrows the car and returns it nearly empty. The dog walker does not need household information but receives it through the same chat thread.

**Actor-by-actor needs**

- Household members need resource availability and condition, not necessarily trip purpose.
- The borrower needs a temporary usage window and relevant rules.
- The dog walker needs only pet-related instructions and confirmation.
- The mechanic and vet need specific records, not household context.
- Responsibility for refill, medication or appointments must be clear.

**With LifeOS**  
The shared car exposes availability and relevant condition while personal destination can remain private. Temporary borrowers receive only the needed reservation and instructions. Pet care actions can be confirmed by whoever performs them. Service appointments can selectively expose maintenance or health facts. A returned-low-fuel condition can create a responsibility or observation without turning into a punitive score.

**Stress variation**  
Two people need the car at overlapping times. LifeOS can expose the resource conflict and alternatives but cannot decide whose trip is morally more important unless participants have already defined a rule.

**Capabilities that emerge**  
Shared resource availability; private purpose vs shared occupancy; temporary user; condition history; subject-centric care; service-provider scoped sharing; actual confirmation; conflict requiring human decision.

---

# Level 3 — Work and coordinated execution

### Scenario 7 — Team deliverable with dependencies and review

**Context and actors**  
A five-person software/product team must deliver a release. Design, backend, frontend, QA and product approval depend on one another. Each person also has unrelated private or company work.

**Without LifeOS**  
The shared tracker shows tasks but not each person's realistic personal plan. Status meetings discover blockers late. A developer says a task is “done,” meaning code is written, while QA assumes it means ready to test. Review requests are spread across tools. The manager asks for updates manually. Each person's calendar separately contains the meetings and self-created focus blocks.

**Actor-by-actor needs**

- Contributors need dependencies that affect them without exposing their full daily plan.
- The manager needs reliable shared status, not surveillance of private time.
- Reviewers need clear requests and acceptance criteria.
- Shared completion language must not erase the difference between delivered, reviewed, approved and actually deployed.
- Each person should be able to schedule personal execution around the same team commitment.

**With LifeOS**  
Shared deliverable facts and dependencies are visible to participants. A contributor can commit to an expected hand-off without sharing personal focus blocks. Review is an explicit requested state. Team status derives from agreed shared milestones while personal execution remains local. If a dependency slips, LifeOS can show affected commitments and propose coordination without automatically rewriting everyone's calendar.

**Stress variation**  
Backend slips one day. Frontend can still do some work but not all. LifeOS should propagate the actual dependency consequence rather than naïvely shift every downstream task. A reviewer becomes unavailable and review responsibility transfers explicitly.

**Capabilities that emerge**  
Shared outcome vs personal execution; cross-person dependency; explicit hand-off; review/approval state; selective capacity; change impact; responsibility transfer; semantic clarity of status.

### Scenario 8 — Shift swap

**Context and actors**  
A nurse cannot work an assigned evening shift. Three colleagues could potentially cover. Minimum staffing and role qualifications must still be satisfied. A supervisor must approve the final change.

**Without LifeOS**  
The nurse messages colleagues individually or in a group. People answer asynchronously. Someone says yes, then realizes they would violate a rest constraint. The roster remains unchanged until a supervisor updates it. Different people temporarily believe different versions of the schedule.

**Actor-by-actor needs**

- The nurse needs to request replacement without exposing personal reasons.
- Colleagues need enough information to judge feasibility.
- The supervisor needs to know the proposed swap still satisfies operational requirements.
- Everyone needs to distinguish requested, tentatively accepted and officially confirmed states.

**With LifeOS**  
The shift owner requests a swap. Eligible colleagues can accept or decline based on information they choose to expose or local rules that determine feasibility. A candidate acceptance remains provisional until required approval. Once confirmed, the canonical shift responsibility changes and affected personal schedules update according to each user's preferences.

**Stress variation**  
The approved replacement becomes sick shortly before the shift. The system reopens coverage as unresolved; it does not pretend that the earlier approved record means the shift is currently covered.

**Capabilities that emerge**  
Swap request; capability/eligibility; privacy of reason; provisional vs authoritative confirmation; required approval; actual coverage; re-opened responsibility after new evidence.

### Scenario 9 — Freelancer, client and subcontractor

**Context and actors**  
A freelance designer delivers a website to a client and hires a copywriter for part of the work. The client has an internal approver who is not a LifeOS user.

**Without LifeOS**  
The freelancer keeps a private project plan. The client sees email deadlines. The copywriter has a separate task list. A draft is emailed, feedback arrives in multiple messages, and approval is ambiguous. A client delay compresses the freelancer's remaining schedule but the client cannot see the internal consequence.

**Actor-by-actor needs**

- The freelancer needs internal planning to remain private.
- The client needs reliable deliverable status and decisions required from them.
- The copywriter needs only their scope and dependencies.
- The external approver needs a lightweight way to approve or request changes.
- Project access should end cleanly after delivery.

**With LifeOS**  
Client-facing milestones and requests are shared while internal preparation remains local. The copywriter participates only in the relevant slice. A review request records who must respond and by when. External approval can happen through a limited interaction without full membership. A client delay becomes explicit evidence that may cause the freelancer to revise their private plan; that revision is not automatically exposed.

**Stress variation**  
The client asks the copywriter directly for an out-of-scope change. LifeOS should not silently convert that message into authorized work; responsibility and approval boundaries remain visible.

**Capabilities that emerge**  
Scoped collaboration; external approver; client-facing vs internal state; request/response; access lifecycle; authority boundary; personal replanning from shared change.

---

# Level 4 — Caregiving

### Scenario 10 — Coordinating care for an older parent

**Context and actors**  
An older parent lives alone. Two adult children share support. A paid caregiver visits three mornings a week. The parent has a GP, specialist appointments and regular medication. One child lives in another city.

**Without LifeOS**  
Appointments are stored in several calendars. Medication refill reminders live on one child's phone. The caregiver sends messages after visits. The parent sometimes reports having taken medication but is unsure. One child assumes the other booked transport. Medical documents are forwarded broadly because there is no better coordination channel. When something changes, nobody knows whether everyone affected has seen it.

**Actor-by-actor needs**

- The older parent remains a person with autonomy, not merely an object being managed.
- Each child needs enough information to perform agreed responsibilities, not unrestricted access to everything.
- The caregiver needs visit instructions and a way to confirm actions/observations.
- Clinicians remain authoritative for clinical instructions; family notes are not equivalent.
- Uncertainty about medication or attendance must remain uncertainty until confirmed.

**With LifeOS**  
Responsibilities are explicit: transport, refill, accompanying an appointment, grocery delivery. The cared-for person can approve which facts are shared where possible. The caregiver has a limited view for scheduled visits and can record agreed confirmations or observations. Clinical instructions retain their source. Family members can attach private notes without turning them into shared medical truth. A missed or uncertain action enters review/escalation rather than being automatically marked complete because time passed.

**Stress variation**  
One child becomes temporarily unavailable for two weeks. Responsibilities transfer for that period and then require restoration or review. Later the paid caregiver changes; the old caregiver's access ends while historical participation remains attributable.

**What improves / what does not**  
LifeOS can reduce coordination gaps, excessive forwarding, uncertainty about responsibility and loss of hand-over information. It must not become a medical record system, diagnose, or let family coordination erase the older person's rights.

**Capabilities that emerge**  
Subject-centric coordination; consent/authority boundaries; sensitive selective sharing; temporary responsibility transfer; source distinction; uncertain actual state; caregiver lifecycle; escalation.

### Scenario 11 — Temporary childcare hand-off

**Context and actors**  
Parents leave a child with grandparents for a weekend. The child has a sports activity, allergy information and one scheduled medication. A neighbor may provide emergency backup.

**Without LifeOS**  
Instructions are sent by chat and repeated verbally. The grandparents save screenshots. A last-minute sports time change is sent to one parent, who must remember to forward it. Allergy and medication information sit beside irrelevant conversation. Nobody has a clear way to know whether the medication action was acknowledged.

**With LifeOS**  
A temporary care period defines what the grandparents need to know and do. Relevant schedule, medication instruction and emergency contact facts are available for that period. Parents retain private context. Material changes propagate only to affected carers. Required actions can be confirmed without sharing the child's whole health history. Backup participation can be added only if needed.

**Stress variation**  
A grandparent becomes ill Saturday morning. The hand-off to the other grandparent or backup neighbor is explicit and incomplete until accepted.

**Capabilities that emerge**  
Time-bounded delegated care; minimum-necessary sensitive information; temporary role; required acknowledgement; emergency substitution; access expiry.

---

# Level 5 — Specialist relationships

### Scenario 12 — Teacher, student and parent around an assignment

**Context and actors**  
A secondary-school student has a large project. The teacher sets milestones. A parent wants to support without controlling the student's entire schedule. Some classmates collaborate on one section.

**Without LifeOS**  
Deadlines are in the school portal. The student copies them into a personal planner. The parent asks repeatedly about progress. Group members coordinate in chat. A teacher deadline changes, but one student's local copy remains stale. The parent sees either too little or too much depending on what the student forwards.

**Actor-by-actor needs**

- The teacher needs canonical assignment facts and submitted/required states.
- The student needs a private execution plan and notes.
- The parent may need limited high-level support visibility, depending on consent/age/authority.
- Classmates need only the shared section and joint milestone.

**With LifeOS**  
Authoritative assignment dates can remain linked to their source. The student builds a private plan around them. A parent may receive only agreed high-level reminders or required actions. The collaborative section has its own participants and responsibilities without exposing each student's full study program.

**Stress variation**  
The teacher extends the deadline. The canonical external fact changes, but LifeOS does not automatically assume the student should delay their personal plan; it can preserve the earlier target or propose a change.

**Capabilities that emerge**  
Authoritative external fact; personal plan around shared requirement; consent/guardian visibility; subgroup collaboration; source-linked change without forced personal replanning.

### Scenario 13 — Technician and customer service visit

**Context and actors**  
A homeowner needs a heating-system repair. A service company dispatches a technician. A replacement part may be delivered by a supplier. Another household member can provide access if needed.

**Without LifeOS**  
The company gives a broad arrival window. The homeowner sends photos by message. The technician arrives but the correct part is not available. A second appointment is required. Internal technical notes, customer-facing updates and supplier timing exist in separate systems. The household member who can open the door is updated manually.

**Actor-by-actor needs**

- The customer needs appointment, preparation and meaningful status.
- The technician needs technical information and evidence not necessarily appropriate for the customer view.
- The dispatcher needs assignment and resource status.
- The supplier needs only part/delivery facts.
- The backup household member needs access timing, not repair history.

**With LifeOS**  
LifeOS can coordinate the user's side of the service relationship while preserving provider-system boundaries. Customer-facing appointment facts, required preparation and evidence can be shared. The provider may expose status updates through an integration or limited interaction. The backup person receives only the access commitment. A missing part creates a visible dependency before the return visit.

**Stress variation**  
The technician is replaced. The appointment remains the same shared commitment, while actual participant and internal provider assignment change.

**Capabilities that emerge**  
Shared commitment across organizational boundary; scoped evidence; prerequisite; resource dependency; participant replacement; role-specific information; provider-system interoperability without ownership confusion.

### Scenario 14 — Doctor, patient and caregiver around a procedure

**Context and actors**  
A patient has a planned outpatient procedure. A clinician provides preparation instructions. A family caregiver will drive the patient home. The facility has an appointment time that can change.

**Without LifeOS**  
The patient receives instructions through a portal or paper. They manually add the appointment to a calendar and message the caregiver. The caregiver knows the time but not necessarily when pickup will actually be needed. A schedule change may require several separate communications. Personal notes become mixed with clinical instructions.

**Actor-by-actor needs**

- The patient needs one understandable personal plan while preserving the distinction between professional instructions and personal reminders.
- The caregiver needs the minimum logistics necessary to help.
- The clinician/facility needs preparation or arrival requirements communicated accurately.
- Sensitive information must not automatically follow every scheduling fact.

**With LifeOS**  
The procedure commitment can reference its authoritative source while the patient builds personal preparation actions around it. The caregiver receives transport timing and agreed instructions only. A facility change updates the shared appointment fact and highlights affected personal actions. Clinical data remains bounded; LifeOS coordinates but does not become the clinical system of record.

**Stress variation**  
The procedure is delayed by three hours after arrival. The caregiver's pickup estimate changes, while unrelated private medical information remains undisclosed.

**Capabilities that emerge**  
Authoritative source vs personal plan; minimum-necessary caregiver sharing; derived impact from schedule change; sensitive-data separation; external system boundary.

### Scenario 15 — Lawyer and client around a filing deadline

**Context and actors**  
A lawyer needs documents from a client before an external filing deadline. An assistant helps collect material. A third-party accountant must provide one document.

**Without LifeOS**  
The deadline is in the lawyer's professional system. Requests are emailed. The client forgets one item. The accountant sends a document to the wrong person. Follow-ups are manual. The client does not know which missing item is actually blocking the process.

**With LifeOS**  
LifeOS on the client side can represent the external deadline and document requests without replacing the law firm's matter-management system. Requested items have responsible parties and receipt state. The client sees which action is currently required from them. The accountant can satisfy a specific request without receiving broader matter access. Private legal reasoning remains outside the shared coordination layer.

**Stress variation**  
The external authority extends the deadline, but the lawyer intentionally keeps an earlier internal target. LifeOS must allow the authoritative external date and the professional planning target to coexist instead of overwriting one with the other.

**Capabilities that emerge**  
External authoritative deadline; request/receipt; third-party contribution; sensitive boundary; multiple legitimate dates with different meaning; professional/internal target vs shared requirement.

---

# Level 6 — Complex multi-actor organization

### Scenario 16 — Surgical operation

**Context and actors**  
A patient is scheduled for surgery. Relevant actors include the patient, surgeon, assistant surgeon, anaesthetist, nurses, operating-room coordination, hospital scheduling, diagnostic services, pre-op assessment, post-op ward, equipment/resources, a family contact and possibly external transport or rehabilitation support.

The scenario is intentionally complex because it exposes weaknesses in simplistic multi-user models. Not every actor has the same authority, information, timing, responsibility or relationship to the patient. Many participants operate through specialist hospital systems rather than LifeOS.

**Without LifeOS from the patient's real-world perspective**  
The hospital and clinicians operate through clinical and operational systems. The patient may receive letters, portal messages, calls and preparation instructions. The family contact has only the information the patient forwards. The patient manually coordinates work leave, transport, packing, medication questions, pre-op tests and post-op support. If the operation moves, many personal commitments must be changed. The hospital knows resource and staff constraints that the patient should not see in detail. The patient knows personal constraints that the hospital may not need to know. Neither side should expose its entire internal state merely to coordinate one procedure.

**Actor-by-actor needs**

- **Patient:** authoritative date/location/instructions; personal preparation plan; clarity about what is confirmed or pending; selective caregiver sharing; privacy; understandable changes.
- **Surgeon:** correct clinical/operational assignment through hospital systems; relevant readiness facts; no need for the patient's unrelated LifeOS data.
- **Anaesthetist:** role-specific clinical readiness and timing, again within appropriate specialist systems.
- **Nursing/ward teams:** operational hand-offs and actual participation.
- **Hospital scheduling:** room, staff and resource capacity; authority to confirm or move operational slots.
- **Family contact:** only agreed logistics, visiting/pickup information and emergency contact responsibilities.
- **External rehabilitation/transport:** only the downstream facts necessary for their service.

**With LifeOS from the coordination perspective**  
LifeOS does not attempt to replace the hospital's clinical or operating-room systems. Instead it can maintain the patient's personal model around authoritative external facts and, where integrations or explicit sharing exist, exchange the minimum coordination information required.

A confirmed procedure time can drive the patient's personal preparation, travel, work leave and caregiver commitments. Pre-op requirements can be represented with their authoritative source and confirmation status. The family contact can receive only transport or support responsibilities. If the hospital changes the operation time, LifeOS can calculate which personal commitments are affected and ask the patient how to adapt them. The hospital does not need the patient's full personal calendar; it may only need availability/confirmation relevant to the procedure.

Inside an institution using LifeOS-like coordination concepts, the same event may have many role-specific operational views: surgeon assignment, anaesthesia coverage, nursing team, room capacity, equipment readiness and patient readiness. A participant's local state can differ from the shared canonical procedure facts without corrupting those facts.

**Stress variation A — delayed operation**  
An emergency case takes the operating room. The procedure is delayed. Hospital operational truth changes first. The patient and family contact need the new timing, while internal details of the emergency case remain private. Personal transport and work-leave consequences change; unrelated health data does not.

**Stress variation B — staff replacement**  
The assigned anaesthetist becomes unavailable and another qualified clinician replaces them. The procedure remains the same shared event; participant assignment changes. Historical responsibility is not rewritten.

**Stress variation C — missing prerequisite**  
A required pre-op result is not available. The operation may be at risk but not yet cancelled. The system must represent uncertainty and a blocking prerequisite rather than collapsing everything into a binary scheduled/cancelled state.

**Stress variation D — patient withdraws consent or procedure is cancelled**  
The future procedure and dependent plans change, but historical preparation and prior decisions remain part of the record. Different actors may require different follow-up actions.

**What improves / what does not**  
LifeOS can improve the patient's personal coordination, selective support sharing, impact analysis and clarity around external requirements. The same multi-actor principles can also inform institutional coordination. LifeOS must not pretend that a consumer coordination layer is a hospital clinical system, expose protected information merely to calculate availability, or let a generic participant model erase professional authority and specialist requirements.

**Capabilities that emerge**  
Canonical shared event with role-specific state; authority/source distinction; role/capability requirements; scarce resource capacity; prerequisite readiness; actual participation; replacement without history rewrite; selective disclosure; external specialist-system boundary; uncertainty; dependent personal replanning; downstream care hand-off.

---

# Part III — Cross-scenario stress simulation

The following variations should be applied mentally across many scenarios rather than treated as isolated edge cases. They repeatedly expose needs that normal happy-path collaboration misses.

## Participant does not use LifeOS

A dinner guest, grandparent, client approver, supplier or technician may never create an account. The collaboration is still real.

**Discovery:** essential participation must be possible through bounded external interaction such as a link, message, email, calendar artifact or another provider. Full membership should not be a prerequisite for every shared commitment.

## Participant joins late

A friend joins a trip, a contractor enters a project, a replacement worker takes a shift or a new caregiver starts.

**Discovery:** joining should expose the current relevant state without pretending the person participated historically. Access and responsibility have effective periods.

## Participant leaves early or permanently

A traveller leaves before the group, an employee changes team, a caregiver contract ends or a couple stops sharing a household area.

**Discovery:** future participation, access and responsibility can end while historical contribution remains attributable.

## No response

A person may not accept, decline or even see a request.

**Discovery:** silence is not consent, attendance or completion. The system needs unresolved state and, where important, escalation or alternate coverage.

## Provisional commitment

A parent waits for childcare, a worker waits for roster confirmation or a traveller waits for leave approval.

**Discovery:** yes/no is often insufficient. Tentative, conditional and pending-authority states are real social facts.

## Two people change the same shared fact

Two household members receive different service-provider messages, or two organizers edit an event.

**Discovery:** shared facts can conflict. Last-write-wins is not always semantically correct; source, authority and explicit review can matter.

## Someone delegates but remains accountable

A manager delegates review, a parent asks a grandparent to pick up a child, or a trip organizer asks someone else to book accommodation.

**Discovery:** doing, owning, approving and being accountable are different roles even if many simple cases collapse them into one person.

## Shared resource becomes unavailable

A car is already booked, a room is unavailable, equipment fails or required stock is missing.

**Discovery:** multi-user coordination often involves resources as well as people. Resource capacity and participant availability interact.

## Information is relevant but private

A person cannot attend because of a medical appointment, financial issue or private relationship.

**Discovery:** coordination often needs only the consequence — unavailable, cannot pay yet, requires accessibility — not the underlying reason.

## Participants need different levels of detail

The event organizer needs supplier status. An attendee needs only time and location. A caregiver needs medication instruction. A sibling needs only pickup time.

**Discovery:** one shared object does not imply one identical view.

## Different personal meaning around one shared fact

The same wedding may be a simple event for one guest, a project milestone for the organizer, a travel trigger for another and a childcare constraint for another.

**Discovery:** the shared fact and each person's local planning meaning must coexist.

## Temporary substitution

A colleague covers a shift, another technician performs the visit, or a family member assumes care for one week.

**Discovery:** replacement should affect the relevant period and responsibility without rewriting who was originally planned or who acted previously.

## Relationship ends badly

A couple separates, a client relationship terminates, a collaborator leaves a project or a family member loses permission to help.

**Discovery:** revoking future access must be possible without deleting legitimate historical facts or continuing unwanted sharing.

## Minor or vulnerable subject

The person affected may not be the account holder or may not have full ability to manage permissions alone.

**Discovery:** actor, subject, guardian/helper and authority cannot always be collapsed into one “user” concept.

## Conflicting evidence about what happened

One caregiver says medication was taken; the cared-for person is unsure. One teammate says delivery occurred; the recipient says it is incomplete.

**Discovery:** actual state may require evidence, confirmation, disagreement or review rather than a single unchallengeable checkbox.

---

# Part IV — Longitudinal simulations

Multi-user relationships are not static. Several needs only appear when the same coordination is followed over months or years.

## Recurring friend group

A group that initially organizes one dinner later plans recurring activities and trips. Some members participate often, others occasionally.

**Discovery:** a persistent group can reduce repeated setup, but membership should not imply automatic access to every future activity. Each shared activity can still have its own participant set and privacy.

## Couple → shared household → separation

Two people progressively share groceries, maintenance, pets, bills and perhaps a vehicle. Later they separate.

**Discovery:** increasing collaboration should not require merging personal histories. When the relationship ends, future sharing and responsibility can split while legitimate shared history, costs or asset records remain understandable.

## Employee → team lead → leaves organization

A person first contributes tasks, later approves work and eventually leaves.

**Discovery:** authority and responsibility change over time. Historic actions must retain the role/context under which they occurred; future access should end cleanly.

## Family caregiver → professional caregiver transition

A family member initially manages most care. Later a paid professional takes over some duties.

**Discovery:** responsibility can be redistributed gradually. The new actor needs relevant current context, not unrestricted access to years of family-private notes.

## Student → graduate → professional collaborator

Two people first share a university project, then later collaborate professionally.

**Discovery:** the relationship between people does not need one permanent global meaning. Different shared contexts can coexist or end independently.

---

# Part V — What consistently improves when LifeOS is useful

Across the simulations, LifeOS creates value when it reduces one or more of the following real-world frictions:

- repeated asking for availability;
- dependence on one human organizer as the only source of truth;
- final decisions buried in chat history;
- duplicated or stale calendar copies;
- ambiguity about whether something is proposed, accepted, confirmed or completed;
- ambiguity about who is responsible;
- silent assumption that a message was seen;
- over-sharing private context just to coordinate one fact;
- loss of personal planning around a shared commitment;
- unclear hand-offs and substitutions;
- inability to coordinate people and scarce resources together;
- mixing authoritative external information with personal interpretation;
- losing history when responsibility or membership changes;
- forcing every participant onto the same tool;
- copying the same shared fact separately into several personal systems;
- confusing planned participation with actual participation.

LifeOS adds less value when the situation is tiny, one-off, low-risk and already solved adequately by a single message. The product should not add process merely because collaboration is possible.

---

# Part VI — Cross-case capabilities discovered

The following categories are derived from repeated simulated needs. They are discovery findings, not final domain-model names.

## 1. Shared canonical fact + personal context

A shared dinner, trip, shift, appointment or deadline needs common facts, but each person may attach different local calendar placement, reminders, preparation, notes, travel, priorities or linked goals.

This distinction appears in almost every scenario and is one of the strongest findings of the study.

## 2. Participation is stateful

Participation is not simply “member / not member.” Real states include invited, unseen, accepted, declined, tentative, conditional, waitlisted, replaced, cancelled, attended and absent.

Not every scenario needs every state, but the underlying need recurs widely.

## 3. Proposal and confirmation are different

A suggested dinner time, shift swap, project deadline or booking choice is not automatically the canonical shared fact.

Multi-user systems need to preserve the difference between suggestion, agreement, authority confirmation and later change.

## 4. Responsibility is richer than assignment

Real situations distinguish:

- who owns the outcome;
- who currently performs the action;
- who may claim it;
- who approves it;
- who is accountable if it remains unresolved;
- who temporarily substitutes for someone else.

The product does not need enterprise workflow everywhere, but a single `assigned_to` idea is insufficient for the full problem space.

## 5. Availability can be coordinated without disclosing the calendar

People often need to answer “can you do one of these windows?” rather than expose why other periods are unavailable.

This is universal across friends, families, work, care and professional relationships.

## 6. Shared information needs selective disclosure

Close relationships do not eliminate privacy. Family, colleagues, caregivers and professionals all require different levels of information.

Useful coordination frequently depends on sharing the consequence rather than the underlying private reason.

## 7. One shared item can have role-specific views

Organizer, attendee, caregiver, client, technician, manager and clinician may all interact with the same shared reality but require different information and actions.

Identical views for every participant are neither necessary nor desirable.

## 8. External participants are normal, not exceptional

Many real relationships cross product boundaries. Grandparents, clients, suppliers, medical providers, restaurants, schools and service technicians may not use LifeOS.

A collaboration model that requires universal adoption would fail many ordinary scenarios.

## 9. Membership, access and responsibility have lifecycles

People join late, leave, substitute temporarily, lose access or change role.

History should preserve what happened while future access and responsibility change from an effective point.

## 10. Actual participation differs from planned participation

A person can accept and then not attend; a different technician can perform the visit; a replacement worker can cover the shift.

The plan must not be treated as proof of what occurred.

## 11. Shared resources are first-class coordination constraints

Cars, rooms, equipment, tickets, accommodation capacity, stock and facilities repeatedly affect multi-user plans.

People and resources must often be considered together.

## 12. Hand-offs require acknowledgement

Sending a message does not mean responsibility transferred. Care, child pickup, project review, service work and shift coverage all show the need to distinguish requested hand-off from accepted hand-off.

## 13. Authority and source matter

A hospital time, school deadline, client request, family suggestion and AI proposal are not equally authoritative merely because they produce the same date field.

Multi-user coordination makes provenance more important, not less.

## 14. Conflict and uncertainty are legitimate states

Real life contains conflicting reports, provisional facts, unconfirmed changes and missing prerequisites.

Forcing immediate binary truth can be more dangerous than preserving uncertainty until review.

## 15. Communication is necessary, but LifeOS should not automatically become a general chat app

Many scenarios require comments, explanations, requests or acknowledgements. However, the primary recurring value is structured coordination around commitments, state, responsibility and change — not an endless social message stream.

## 16. Shared financial responsibility is common but not universal

Trips, tickets, households and shared resources produce payer/contributor/settlement needs. These are important common capabilities but do not define every collaboration scenario.

## 17. Groups are useful containers but should not imply global sharing

A family, friend group, team or club can reduce repeated setup, but membership in the group should not automatically expose every item or make every member a participant in every activity.

## 18. Collaboration should not erase personal autonomy

A shared plan may affect a person's day, but the person's private goals, capacity, notes and replanning remain theirs unless explicitly shared or governed by an accepted external authority relationship.

This principle recurs from informal dinners through highly structured professional scenarios.

---

# Part VII — Universality classification

## Strongly universal

These appear across social, household, work, care and specialist scenarios:

- participant identity and participation state;
- shared facts separated from personal context;
- selective visibility/privacy;
- proposal vs confirmation;
- responsibility and hand-off;
- change propagation and acknowledgement;
- external/non-LifeOS participants;
- personal autonomy around shared commitments;
- planned vs actual participation;
- source/provenance of important shared facts.

## Very common

These appear across several, but not all, domains:

- group/container continuity;
- temporary substitution;
- review/approval;
- shared resources and capacity;
- dependency across people;
- shared documents/evidence;
- financial contribution or settlement;
- role-specific views;
- recurring shared activities.

## Contextual

These matter strongly in some areas but should not automatically burden all collaboration:

- guardian or caregiver authority;
- professional/client boundaries;
- formal approvals;
- shift qualification and coverage rules;
- ticket/entitlement transfer;
- institutional source hierarchy.

## Specialist

These require dedicated domain knowledge or external systems and should not be generalized merely because LifeOS coordinates around them:

- clinical diagnosis/treatment records;
- operating-room management;
- legal matter management;
- full workforce management;
- enterprise project administration;
- accounting/settlement systems;
- school information systems.

The simulation repeatedly supports a coordination layer around specialist systems, not replacement of every specialist system.

---

# Part VIII — Negative evidence: what the simulation does not justify

The study does **not** provide evidence that LifeOS should become:

- a generic social network or public feed;
- a mandatory all-purpose group chat;
- a complete enterprise project-management platform;
- a hospital clinical system;
- a school administration system;
- a legal matter-management system;
- a full workforce/roster system;
- a universal accounting platform;
- one giant shared workspace where participants lose personal boundaries;
- a platform that requires every external person to create an account;
- a system that exposes detailed calendars in order to compute coordination;
- a system where the creator of an item automatically owns all decisions about every participant;
- a system where acceptance means actual attendance or where elapsed time means completion.

The strongest recurring opportunity is narrower and more distinctive: **coordinate shared reality while preserving each person's independent personal model.**

---

# Part IX — Questions intentionally left open for later product/technical work

The simulations reveal questions that matter but should not be prematurely fixed here:

- What exact reusable concepts should represent participant, role, responsibility, shared state and personal overlay?
- Which shared facts require one authoritative owner, multi-party agreement or external authority?
- Which changes require acknowledgement versus silent synchronization?
- What is the minimum useful experience for a non-LifeOS participant?
- How should sensitive sharing defaults differ between family, work, healthcare and casual social contexts?
- How are conflicting shared facts resolved when sources have different authority?
- Which collaboration needs belong in core LifeOS versus specialist modules or integrations?
- When does a persistent group add enough value to justify existence beyond individual shared items?
- How should temporary delegation, substitution and later restoration appear to users?
- Which cost-sharing needs justify native support and which should remain integrations?
- How much structured communication is needed before LifeOS risks becoming another messaging platform?
- How should a person inspect and revoke what they currently share across all active relationships?

These are follow-up questions, not unresolved defects in the study.

---

# Part X — Follow-up external research

External research should be conducted **after** this simulation and documented separately.

Its purpose should be to challenge and validate these findings rather than generate them from competitor feature lists.

Research should examine, among other things:

- coordination and privacy patterns in shared calendars;
- family/household coordination products;
- group travel and expense workflows;
- collaborative task/project products;
- shift scheduling and hand-over systems;
- caregiving coordination;
- patient/caregiver portals and healthcare coordination boundaries;
- education/parent/student coordination;
- event and resource scheduling;
- HCI research on groupware, awareness, privacy, consent, shared artifacts and common-ground failures;
- failure modes in notification, acknowledgement, hand-off and responsibility transfer;
- patterns for including participants who do not use the same application.

The research should explicitly identify:

1. findings that reinforce the simulation;
2. findings that contradict it;
3. important multi-actor needs missing from the simulation;
4. approaches that existing products handle poorly;
5. areas where LifeOS should deliberately avoid competing;
6. implications that deserve later product-model or architecture review.

---

# Conclusion

The earlier feature-discovery study showed that broad personal use cases could be expressed through a relatively small set of reusable primitives. This multi-actor study suggests an analogous result for collaboration.

Across dinners, trips, families, shared resources, team work, shifts, caregiving, client relationships, education, healthcare coordination and complex institutional scenarios, the same core problems recur:

1. several people need to refer to some common reality;
2. each person still has a different personal context around that reality;
3. participation, responsibility and authority are not identical concepts;
4. proposals, confirmations and actual outcomes are different states;
5. privacy requires selective disclosure even between close collaborators;
6. people join, leave, substitute and change role over time;
7. external/non-LifeOS participants are normal;
8. resources and prerequisites often matter alongside people;
9. changes need scoped propagation and sometimes acknowledgement;
10. history must preserve who actually did, knew, approved or changed what;
11. uncertainty and disagreement must sometimes remain visible rather than being overwritten;
12. LifeOS creates the most distinctive value when it coordinates shared commitments **without merging the participants' personal operating systems into one**.

The strongest product hypothesis emerging from the simulations is therefore not “LifeOS should add collaboration features.”

It is:

> **LifeOS should allow independent personal systems to coordinate around shared facts, responsibilities and resources while preserving personal autonomy, privacy, provenance and historical truth.**

This remains discovery evidence. The next independent step is external research; only after simulation and research are compared should the project promote specific multi-actor concepts into binding product/domain decisions.
