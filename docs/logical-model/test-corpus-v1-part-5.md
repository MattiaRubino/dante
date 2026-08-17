<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1-part-4.md" -->
> **Canonical continuation of `test-corpus-v1.md`.** This Part 5 adds Integrated A+B+C+D cumulative regression pressure.

# V. Integrated A+B+C+D regression corpus

## TC-S01 — current knowledge of resolved state

LifeOS currently accepts that a fracture healed last week.

Required:

```text
knowledge-current = yes
world-applicable-now = no
history remains retrievable
```

## TC-S02 — unknown applicability

A state has known onset but no reliable end/current-status evidence.

Required:

```text
applicability remains unknown/unresolved
not forced active/inactive/permanent
```

## TC-S03 — historical but currently relevant

A healed fracture may matter to rehabilitation planning.

Required:

```text
not currently active
but retrievable/relevant for bounded query purpose
```

## TC-S04 — historical and irrelevant to current query

Past fever exists while planning an unrelated current music task.

Required:

```text
history preserved
not treated as active
retrieval may omit/deprioritize by purpose without deleting source
```

## TC-S05 — point Observation not continuing state

One high-temperature Observation exists.

Required:

```text
point fact preserved
no continuing fever state fabricated
```

## TC-S06 — AI candidate continuing state

AI infers possible ongoing fever from observations.

Required:

```text
candidate/inference attribution preserved
not canonical ongoing condition automatically
```

## TC-S07 — MaterialStateRef independence

A target state S1 is addressed historically.

Required:

```text
MaterialStateRef(S1) remains same historical state
knowledge-current/applicability may later change independently
```

## TC-S08 — bitemporal implementation candidate

A physical valid-time/transaction-time representation is proposed.

Required:

```text
can support chronology
cannot redefine semantic owner/materiality/current interpretation
```

## TC-S09 — current projection conflict

Two credible current assertions remain unresolved.

Required:

```text
knowledge projection can expose unresolved/conflicting state
no recency winner fabricated
```

## TC-S10 — resolved state and prior Confirmation

Condition state S1 active is confirmed; later same owner state S2 resolved.

Required:

```text
Confirmation remains bound to S1
S2 current state does not inherit Confirmation automatically
```

## TC-S11 — historical Evidence reuse

No-longer-current condition state is relevant to later retrospective Evaluation.

Required:

```text
historical MaterialStateRef usable as Evidence
not relabeled currently applicable
```

## TC-S12 — simple current fact

One ordinary user-entered currently applicable state has no conflict/history consequence.

Required:

```text
simple product experience remains compact
no visible bitemporal/version bureaucracy required
```

---

# W. Integrated mutations

```text
MUT-ABCD01 one generic current flag for knowledge + applicability
MUT-ABCD02 unknown applicability -> inactive
MUT-ABCD03 unknown applicability -> active/permanent
MUT-ABCD04 not-current state removed from all retrieval
MUT-ABCD05 latest stored historical state assumed active now
MUT-ABCD06 point Observation -> continuing condition
MUT-ABCD07 AI inference -> canonical continuing state
MUT-ABCD08 MaterialStateRef contains universal current flag
MUT-ABCD09 bitemporal row becomes semantic Fact owner
MUT-ABCD10 projection chooses winner by recency
MUT-ABCD11 resolved state deletes prior bindings
MUT-ABCD12 historical relevance => current applicability
```

All must remain rejected.

---

# X. Integrated counterfactuals

```text
CF-ABCD01 knowledge-current resolved fracture vs active fracture now
CF-ABCD02 unknown end vs explicitly ongoing state
CF-ABCD03 historical relevance vs current applicability
CF-ABCD04 point fever Observation vs fever episode
CF-ABCD05 AI candidate state vs accepted state
CF-ABCD06 current interpretation vs world-current state
CF-ABCD07 retrieval relevance vs canonical ownership
CF-ABCD08 same owner active->resolved vs distinct episode identity
```

These become permanent regression after integrated closure.