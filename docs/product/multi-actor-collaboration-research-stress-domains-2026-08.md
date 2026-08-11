# LifeOS — Multi-Actor Deep Research: Stress Domains

**Date:** 11 August 2026  
**Status:** Product research / external evidence  
**Scope:** targeted deep-research appendix for four high-risk multi-actor domains that deserve separate treatment beyond the broad collaboration research: adversarial relationship exits, children/adolescent agency, accessibility and low digital literacy, and AI-mediated multi-party privacy.  
**Relationship to other evidence:** complements `multi-actor-collaboration-discovery-simulation-2026-08.md` and `multi-actor-collaboration-research-2026-08.md`. It does not change accepted V1 scope, architecture or authorization decisions.

---

# 1. Why these four stress domains matter

The broad multi-actor research identified four areas where ordinary collaboration assumptions become especially unsafe:

1. a relationship can end in conflict rather than through a clean voluntary leave flow;
2. one participant can be a child or adolescent whose autonomy changes over time and exists alongside guardian responsibilities;
3. a necessary participant may have low digital literacy, accessibility needs or limited ability/willingness to maintain another app;
4. an AI agent may coordinate several people while possessing private context that must not leak across those people.

These domains are useful precisely because they challenge assumptions that work in friendly, digitally competent adult peer groups.

---

# 2. Stress Domain A — Adversarial relationship exits and coercive contexts

## 2.1 Normal `leave group` semantics are insufficient

Many collaboration designs assume that relationships end cooperatively: a member leaves a project, a caregiver contract ends, a household member is removed, or a former partner stops sharing a calendar.

Real-world safety guidance for technology-facilitated abuse shows that shared accounts, location sharing, connected devices and persistent access can be used for coercive control or surveillance. In these situations the person attempting to leave may need to inspect and revoke sharing without negotiating with the other participant.

Apple's Safety Check is an important current product pattern. It provides:

- review of sharing with people and apps;
- review of devices connected to the account;
- an Emergency Reset path to stop sharing quickly;
- account/password/security review.

The significance for LifeOS is not the Apple UI itself. It is the product principle that **relationship termination can be a safety operation, not merely a membership edit**.

Sources:

- Apple Safety Check user guide: https://support.apple.com/guide/personal-safety/how-safety-check-works-ips2aad835e1/web
- Apple Safety Check emergency reset: https://support.apple.com/guide/personal-safety/use-emergency-reset-ips2aad835e1/web
- National Network to End Domestic Violence, Technology Safety & Privacy: https://nnedv.org/content/technology-safety/
- NNEDV Safety Net Project: https://www.techsafety.org/

## 2.2 Shared-device and smart-home research adds another failure mode

Intimate-partner-violence research on smart homes shows that one household member can possess asymmetric technical control over devices, accounts or automation. The same physical home does not imply equal digital authority.

A system therefore should not infer that household membership permanently legitimizes access to household-related personal information.

**Research implication:** collaborative access must have a lifecycle independent from historical participation and independent from physical/social proximity.

## 2.3 Revocation must not erase history

Safety-oriented revocation creates a subtle requirement:

- future visibility/action rights may need to stop immediately;
- valid historical records may still need attribution;
- a former participant should not continue receiving future updates merely because they appear in history;
- revocation itself may be sensitive and should not necessarily expose unnecessary detail to the revoked participant.

This reinforces the simulation's `effective period` finding but raises its consequence level.

## 2.4 Global sharing audit becomes a user need

In friendly collaboration it can be sufficient to manage sharing item by item. Under relationship breakdown, the user may need a simple answer to:

> Who can currently see, change, receive or infer something about me through LifeOS?

This suggests a cross-cutting inspection capability stronger than ordinary per-object settings.

It does **not** imply exposing raw ACLs. The product need is an understandable relationship-oriented sharing audit.

## 2.5 Adversarial-exit findings

Strong findings:

- future access revocation must be separable from historical attribution;
- some users need emergency/global review of active sharing;
- household/family membership cannot be treated as permanent consent;
- connected resources/devices can carry indirect information leakage;
- relationship termination can require immediate safety-first defaults rather than consensus;
- access history and current access are distinct user questions.

Open questions for later product modeling:

- whether emergency revocation affects all shared contexts or allows scoped exceptions;
- what metadata about the revocation is visible to the other party;
- how shared ownership of genuinely joint assets survives an adversarial relationship exit;
- how LifeOS distinguishes revoking data access from abandoning legal/real-world responsibilities.

---

# 3. Stress Domain B — Children, adolescents, guardians and evolving autonomy

## 3.1 `Parent controls child account` is too simplistic

HCI research on parent–teen privacy shows that family oversight is a negotiated relationship, not merely a parental settings panel.

Research on joint family oversight reports that both parents and teens can see value in transparency and co-management, while also identifying power imbalances and disagreement over acceptable monitoring. Parents can be more supportive of monitoring than teenagers, and design must account for tensions between safety, trust and autonomy.

Sources:

- Akter et al., *From Parental Control to Joint Family Oversight: Can Parents and Teens Manage Mobile Online Safety and Privacy as Equals?*, ACM 2022: https://dl.acm.org/doi/10.1145/3491102.3517507
- Author preprint: https://arxiv.org/abs/2202.12302

## 3.2 Autonomy changes over time and by context

A teenager's appropriate privacy around school tasks, location, health, friends or personal goals is not static. Different contexts can legitimately have different guardian involvement, and the balance can evolve with age and capability.

Mixed-method research on parental monitoring highlights that young people's autonomy and perceptions of monitoring are context-dependent. Restrictive monitoring can be experienced differently from supportive oversight.

This does not produce a universal product rule, but it invalidates a one-time binary `minor = parent sees everything` assumption.

## 3.3 Child, account holder, subject, guardian and responsible adult are different roles

The broad simulation already found this in caregiving. Research on parent–teen systems strengthens it:

- the child may be the subject of an event or program;
- a parent may hold legal/real-world responsibility;
- another adult may temporarily perform a responsibility;
- the child may still possess personal information and preferences that are not automatically operationally relevant to every adult;
- different adults may have different authority in different contexts.

## 3.4 Transparency may be more important than hidden monitoring

A recurring design direction in family privacy research is that family oversight is healthier when participants understand what is being shared/monitored and why, except where safety/legal constraints require otherwise.

For LifeOS this suggests a bias toward:

- explainable sharing relationships;
- age-appropriate visibility into who receives what;
- gradual autonomy rather than sudden full-control transitions;
- explicit distinction between support and surveillance.

## 3.5 Minor/autonomy findings

Strong findings:

- child/adolescent agency cannot be represented as ordinary adult peer collaboration;
- guardian authority can be legitimate without implying unrestricted visibility across all domains;
- autonomy should be capable of evolving over time and by context;
- support, safety oversight and surveillance are not equivalent concepts;
- temporary carers and guardianship/support roles need bounded scope;
- family privacy design must account for power imbalance, not assume freely negotiated peer consent.

Open questions:

- age/region-specific legal rules are jurisdictional and must not be hard-coded from this study;
- health, education, location and social domains may require different defaults;
- the exact transition mechanism from guardian-managed to self-managed LifeOS remains a later product/legal decision.

---

# 4. Stress Domain C — Accessibility, older adults and low digital literacy

## 4.1 External participation is not enough if external interaction is still too complex

The broad research established that LifeOS should not require every participant to create an account. This stress domain goes further:

> A link-based external flow can still exclude someone if it assumes high digital confidence, a modern smartphone, good vision, precise tapping, complex authentication or familiarity with app concepts.

A 2026 JMIR Aging scoping review on digital technology use among older adults identifies interacting barriers involving health limitations, usability/design, support, confidence, skills and resources. The practical problem is not simply device ownership.

Sources:

- JMIR Aging, 2026 scoping review on barriers/facilitators to digital technology use among older adults: https://aging.jmir.org/2026/1/e76138
- PubMed record: https://pubmed.ncbi.nlm.nih.gov/41511820/

## 4.2 Collaboration needs graceful modality degradation

For LifeOS, inclusive collaboration may require several levels of participation:

- full application;
- simple web interaction;
- email interaction;
- SMS or message-based confirmation where appropriate;
- voice-assisted flow;
- printed or human-mediated information for some contexts;
- another authorized person helping without impersonating the participant.

This is not a commitment to implement every channel. It is evidence against assuming `mobile app UI` is the universal interaction contract.

## 4.3 Assisted use must not erase attribution or autonomy

If a family member assists an older adult, the system should avoid silently turning helper actions into actions by the older adult.

Useful distinctions can include:

- person affected;
- person who physically entered the information;
- person who confirmed/approved it;
- source of the fact.

This reinforces the existing provenance and actual-state findings.

## 4.4 Accessibility is not only visual design

Multi-user accessibility includes:

- cognitive load from too many states/permissions;
- memory burden;
- notification overload;
- authentication friction;
- difficulty understanding who will see an action;
- difficulty reversing an accidental share;
- reliance on implicit platform conventions.

A highly expressive collaboration model can therefore become inaccessible even if individual controls meet visual accessibility standards.

## 4.5 Low-digital-literacy findings

Strong findings:

- essential collaboration flows should degrade gracefully to simpler interaction modes;
- account creation and complex permission configuration should not be prerequisites for every bounded action;
- assisted interaction needs provenance rather than impersonation;
- progressive disclosure is a usability and accessibility requirement, not merely aesthetic preference;
- notification/confirmation burden should account for cognitive accessibility;
- recovery from mistakes should be easy and understandable.

---

# 5. Stress Domain D — AI-mediated multi-party coordination and privacy

## 5.1 Multi-party AI is not simply one assistant with a larger context window

If LifeOS eventually allows AI to coordinate among people, the AI may have access to private information for several actors:

- one person's full calendar;
- another person's health constraint;
- a third person's budget;
- shared event facts;
- relationship history;
- inferred preferences.

The AI must often compute a useful coordination result while **not revealing the private reasons used to compute it**.

Example:

```text
Person A: free after 18:00 except therapy 18:30–19:30
Person B: available after 19:00

Safe shared proposal:
20:00 works for both

Unsafe explanation:
20:00 is best because A has therapy until 19:30
```

This is the algorithmic version of the simulation's `share consequence, not reason` principle.

## 5.2 Current research shows multi-party privacy is harder than one-to-one privacy

Recent privacy research for LLM/agent systems finds that multi-party settings introduce leakage paths that do not appear in ordinary one-user interaction.

A 2026 benchmark on multi-party privacy evaluates whether models disclose information across actors and reports that existing safeguards remain incomplete.

Source:

- MuPPET / multi-party privacy benchmark (2026): https://arxiv.org/abs/2602.18718

## 5.3 Agent tool interfaces themselves can encourage over-disclosure

The 2026 ACL PrivateNLP paper *Agentic Disclosure* studies tool schemas and argues that generic free-text parameters can become disclosure channels that collapse context boundaries. The study reports a substantial fraction of analyzed tool specifications containing such channels.

The specific percentage is less important for LifeOS than the design warning:

> privacy can be lost at the tool/API boundary even when the high-level assistant intends to behave safely.

Source:

- *Agentic Disclosure: Privacy Risks in Tool-Using Language Models*, ACL PrivateNLP 2026: https://aclanthology.org/2026.privatenlp-1.8/

## 5.4 Contextual privacy can be treated as a reasoning problem

The ACL 2025 `1-2-3 Check` work explores multi-agent contextual privacy and reports reduced leakage compared with simpler single-agent handling in its evaluated scenarios.

This is early research, not a LifeOS architecture recommendation, but it supports the idea that privacy decisions require explicit reasoning about:

- who is asking;
- whose information is involved;
- purpose/context;
- what minimum disclosure satisfies the task.

Source:

- *1-2-3 Check: Enhancing Contextual Privacy in LLMs through Multi-Agent Reasoning*, ACL 2025: https://aclanthology.org/2025.findings-acl.1185/

## 5.5 Assistant-to-assistant coordination should negotiate minimal context

Microsoft Research's 2026 CONCORD work studies privacy-aware context recovery across assistants. The useful product direction is that an assistant should request/reveal relationship-relevant minimum context rather than automatically pooling the participants' entire personal histories.

Source:

- Microsoft Research, CONCORD (2026): https://www.microsoft.com/en-us/research/publication/concord-context-recovery-in-multi-agent-conversations-with-privacy-aware-assistant-coordination/

## 5.6 AI must not silently become a new authority actor

Another multi-party risk is decision authority.

If LifeOS AI proposes a shared time, delegates a task or summarizes disagreement, participants may begin treating the result as authoritative even when the AI merely optimized available information.

Therefore later AI coordination should preserve distinctions such as:

```text
AI-derived suggestion
participant proposal
participant agreement
external-authority fact
actual outcome
```

The AI's access to more context does not grant it more social authority.

## 5.7 Private optimization can create explainability tension

A difficult design problem appears when the AI uses private constraints to produce a shared recommendation.

The user receiving the recommendation may ask:

> Why can't we do 18:00?

The system must sometimes explain the decision without revealing the private reason.

Possible product-level answer pattern:

> “18:00 conflicts with another participant's private availability constraints.”

not:

> “Anna has a medical appointment.”

This indicates that multi-party AI needs **privacy-preserving explanations**, not only privacy-preserving computation.

## 5.8 Multi-party AI findings

Strong findings:

- private contexts must not be pooled into a shared narrative by default;
- the AI often needs minimum-necessary disclosure and relationship-aware context selection;
- tool/API design can create privacy leakage independently of conversational wording;
- explanations may need to preserve privacy while remaining operationally useful;
- AI proposal/optimization does not create social or institutional authority;
- actor-specific consent/authorization boundaries must apply to AI context building as well as ordinary UI/API access;
- multi-party coordination should be evaluated for leakage between participants, not only leakage to the model provider.

Open questions:

- whether LifeOS uses one orchestrator, isolated per-user agents or another architecture remains deliberately undecided;
- exact cryptographic/privacy-preserving computation is outside this product study;
- some coordination tasks may be safer to perform deterministically from abstract free/busy/capability facts rather than exposing raw personal context to AI at all.

---

# 6. Cross-domain synthesis

These four stress domains add several high-confidence constraints to the broader research.

## 6.1 Relationship lifecycle includes safety state

The lifecycle is not merely:

```text
join → participate → leave
```

It may include:

```text
join
→ participate
→ reduce sharing
→ revoke one context
→ emergency revoke
→ preserve historical attribution
```

## 6.2 Authority and autonomy can coexist asymmetrically

A guardian, employer, clinician or caregiver relationship can create legitimate authority in one bounded context without granting broad ownership over the person's LifeOS.

## 6.3 Participation capability is a spectrum

A multi-actor system should be able to reason about people who range from:

- full LifeOS users;
- registered occasional collaborators;
- link/email/SMS responders;
- assisted participants;
- subjects who do not interact with the system directly.

These are product-discovery categories, not final account types.

## 6.4 Privacy must apply to derivation as well as direct viewing

It is insufficient to hide a private event in the UI if an AI explanation, optimization result, notification or derived status leaks the reason indirectly.

## 6.5 `Who can see what?` and `who can infer what?` are different questions

Multi-party AI makes this distinction particularly important.

## 6.6 Revocation usability matters as much as sharing usability

Many products optimize invitation and sharing flows. Safety research shows that ending sharing deserves equal design attention.

---

# 7. Additions to the multi-actor research risk register

## R13 — Coercive persistence

A former or abusive relationship retains access because collaboration was designed only for friendly departure.

## R14 — Guardian overreach

Legitimate guardian responsibility expands into unnecessary surveillance of the minor's unrelated personal context.

## R15 — Assisted-user impersonation

A helper enters data on behalf of another person and the system records it as if the subject personally asserted it.

## R16 — Accessibility by complexity failure

The collaboration model is logically expressive but too cognitively demanding for necessary participants.

## R17 — AI cross-participant leakage

The assistant reveals one participant's private reason, preference or history while explaining or coordinating with another.

## R18 — AI authority laundering

A model-generated optimization is presented socially as if it were a participant agreement or authoritative decision.

## R19 — Derived privacy leakage

No raw private field is displayed, but a recommendation, explanation or status makes the hidden information obvious.

## R20 — Unsafe revocation semantics

Revoking access unintentionally deletes history, breaks legitimate shared ownership or notifies an adversarial party in a harmful way.

---

# 8. Additional validation questions for later product/domain work

1. Can a user see all active sharing relationships in human terms rather than ACL terms?
2. Can future access end immediately without rewriting historical participation?
3. Is there a safe path when relationship termination is adversarial rather than consensual?
4. Does guardian/caregiver authority apply only to the context that justifies it?
5. Can a minor's autonomy evolve without an all-or-nothing account migration?
6. Can an older or low-digital-literacy participant complete the essential action without learning LifeOS?
7. If someone assists another user, is the actor/source recorded truthfully?
8. Can an AI compute a coordination result from private information without revealing the underlying reason?
9. Can the AI explain a recommendation while respecting other participants' privacy?
10. Are AI tools/schema constrained so private context cannot leak through generic payloads?
11. Does AI retain the distinction between suggestion, agreement, authority and actual outcome?
12. Does revocation stop derived notifications/AI context access as well as direct object access?
13. Can a user understand not only what is shared, but the likely inferences enabled by that sharing?
14. Are emergency privacy controls discoverable when the user is under stress?
15. Can collaboration degrade to email/SMS/voice/human assistance without corrupting provenance?

---

# 9. Conclusion

The stress-domain research does not change the central hypothesis from the broad simulation and research. It makes the required boundaries sharper.

A robust multi-actor LifeOS must not assume that collaborators are:

- peers;
- adults;
- friendly;
- equally powerful;
- equally digitally capable;
- permanent members;
- willing to reveal the reasons behind their constraints;
- safe recipients of every AI-generated explanation.

The stronger hypothesis after these stress tests is:

> **LifeOS should let independent people coordinate shared reality even when their relationships, authority, digital capability and privacy needs differ — and it must make joining, understanding, delegating, assisting, revoking and leaving as semantically truthful as ordinary happy-path collaboration.**

For future AI-mediated collaboration, an additional rule emerges:

> **An AI may use private context to help a person's own planning, but cross-person coordination must disclose only what the receiving actor is entitled and needs to know; useful inference is not permission to reveal its private inputs.**

This remains external product evidence. It should be synthesized with the main simulation and deep research before any concrete collaboration concepts are promoted into binding LifeOS domain or architecture decisions.