# DANTE — World Focus Substrate Combinatorial Evidence

**Status:** SUPPORTING WS1–WS5 FINAL CONVERGENCE EVIDENCE — PRE-WS7 / ANALYTICAL  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`  
**Parent closure authority:** `world-focus-substrate-final-convergence-proof.md`

This document preserves the exact compact combinatorial coverage design used by the final analytical hardening.

It is intentionally not production code and not WS7 executable proof. Its purpose is to make the N-way coverage auditable and reusable rather than leaving it as chat memory.

---

# 1. General 3-way covering matrix

## 1.1 Axes and codes

Every axis has three levels encoded `0 / 1 / 2`.

The vector position order is fixed:

```text
0 basis
1 disclosure
2 identity
3 governance
4 effect
5 sync
6 config
7 interaction
8 presentation
9 dante
10 time
```

### basis

```text
0 current
1 superseded_retracted
2 conflicted_incomplete
```

### disclosure

```text
0 allowed
1 revoked
2 purpose_recipient_mismatch
```

### identity

```text
0 stable
1 ambiguous_candidate
2 retired_merge_split
```

### governance

```text
0 none
1 revision_bound_binding
2 represented_delegated
```

### effect

```text
0 read_only
1 pending_ambiguous
2 partial_real_compensating
```

### sync

```text
0 online
1 offline_replay
2 provider_lag_timeout
```

### config

```text
0 transient
1 pinned_saved
2 concurrent_shared
```

### interaction

```text
0 none
1 primary_supporting
2 world_switch_late
```

### presentation

```text
0 normal
1 constrained_a11y
2 specialist_missing
```

### dante

```text
0 unavailable_quiet
1 contextual_analysis
2 proposal_action_late
```

### time

```text
0 simple
1 recurrence_exception_dst
2 ordering_effective_unclear
```

---

## 1.2 Coverage target

All 3-way interactions among 11 3-level axes:

```text
C(11,3) * 3^3
= 165 * 27
= 4,455 required triples
```

Selected covering rows:

```text
67
```

Verified analytical coverage:

```text
covered   4,455 / 4,455
uncovered 0
```

The fixed row-vector payload below has SHA-256:

```text
ca2e8b4aa19285eecd61ac072c0bc9a4f938e7863eea8393d2f2da26827610a0
```

The hash is over the newline-separated raw vectors, without row labels.

---

## 1.3 Fixed 3-way row vectors

Each vector has exactly eleven digits in the axis order above.

```text
T01 00000121012
T02 02121012100
T03 22212220201
T04 11110102121
T05 11001210210
T06 20222001022
T07 00120210222
T08 22210111110
T09 20001022121
T10 11102011001
T11 01211202012
T12 21022102200
T13 12221120021
T14 10112020112
T15 02010001201
T16 01200020100
T17 20101100002
T18 12012212020
T19 22120222011
T20 10021201100
T21 12200002222
T22 01102121220
T23 00222211111
T24 21000211122
T25 20211112201
T26 21020000011
T27 02022100122
T28 11121221212
T29 00112002210
T30 10220122200
T31 11202112112
T32 21111110020
T33 22011221102
T34 02202200010
T35 11211021221
T36 10110221000
T37 22101001111
T38 01021010002
T39 00200212021
T40 10012100211
T41 22122112212
T42 12002022002
T43 20020011220
T44 01112210101
T45 02201111201
T46 00021122110
T47 02110010022
T48 20202220120
T49 10101202221
T50 21221022120
T51 10220010010
T52 01010122202
T53 12222101000
T54 02022222101
T55 20200200211
T56 20210002102
T57 12000110101
T58 01221120122
T59 22100002220
T60 20112121021
T61 12120000211
T62 00102200202
T63 21002001102
T64 12210221020
T65 21201221010
T66 02020220112
T67 01222102011
```

---

# 2. High-risk 4-way covering matrix

The higher-order matrix focuses on the seven axes most likely to create unsafe coupling around truth, access and consequential effects.

Fixed position order:

```text
0 basis
1 disclosure
2 identity
3 governance
4 effect
5 sync
6 dante
```

Level meanings are the same as the general matrix.

## 2.1 Coverage target

```text
C(7,4) * 3^4
= 35 * 81
= 2,835 required four-way interactions
```

Selected rows:

```text
157
```

Verified analytical coverage:

```text
covered   2,835 / 2,835
uncovered 0
```

Fixed row-vector SHA-256:

```text
d6efbcd0306ee7d37fac0b4cbc59c7af356c8ac8cbf9ee0d08ed8efbc8f5d835
```

The hash is over newline-separated raw vectors without row labels.

---

## 2.2 Fixed 4-way high-risk row vectors

```text
Q001 0111222
Q002 2000211
Q003 2220110
Q004 0102020
Q005 1201220
Q006 1020020
Q007 2011002
Q008 1210101
Q009 2022122
Q010 0212012
Q011 1122001
Q012 2212221
Q013 0012100
Q014 0221121
Q015 1102212
Q016 1111110
Q017 0100102
Q018 2110200
Q019 0021210
Q020 2200022
Q021 0120011
Q022 1220202
Q023 0202201
Q024 2101121
Q025 1201011
Q026 1001102
Q027 2002010
Q028 1022111
Q029 0221000
Q030 0010021
Q031 2121012
Q032 1011201
Q033 0210210
Q034 2202100
Q035 2010112
Q036 1100221
Q037 2122220
Q038 1212122
Q039 0002222
Q040 2211020
Q041 0112111
Q042 0201112
Q043 1110022
Q044 2221201
Q045 0000120
Q046 0022002
Q047 1100000
Q048 2020101
Q049 1222010
Q050 0001001
Q051 1012220
Q052 2112001
Q053 0220222
Q054 2101210
Q055 1121100
Q056 1000012
Q057 2222212
Q058 1021222
Q059 2211111
Q060 2021021
Q061 1120112
Q062 1002021
Q063 2112102
Q064 0010202
Q065 2110120
Q066 0122200
Q067 1202002
Q068 1211212
Q069 2001200
Q070 0011010
Q071 0101211
Q072 2200001
Q073 1200110
Q074 0222120
Q075 2101202
Q076 1011121
Q077 0211102
Q078 2110010
Q079 2012211
Q080 0111001
Q081 1212000
Q082 1122121
Q083 0002111
Q084 1220211
Q085 1101022
Q086 0021112
Q087 0122022
Q088 2020000
Q089 0200121
Q090 2020222
Q091 1112201
Q092 1010210
Q093 0101120
Q094 1102101
Q095 0022221
Q096 2222011
Q097 0200000
Q098 2221102
Q099 0100212
Q100 2102112
Q101 1121211
Q102 0212021
Q103 0112210
Q104 2001120
Q105 1002200
Q106 0120101
Q107 1011011
Q108 1221022
Q109 2200220
Q110 0110221
Q111 2120121
Q112 2012022
Q113 2210002
Q114 0020110
Q115 2100122
Q116 1102120
Q117 1222200
Q118 2102021
Q119 0121020
Q120 1021000
Q121 2122202
Q122 1012212
Q123 0220012
Q124 1221110
Q125 2111222
Q126 1120210
Q127 1000201
Q128 0210122
Q129 2202111
Q130 0211200
Q131 2110211
Q132 1122012
Q133 0001012
Q134 1210021
Q135 2021010
Q136 2201000
Q137 1111002
Q138 1020120
Q139 2002201
Q140 2221122
Q141 0110220
Q142 2012110
Q143 0200210
Q144 0112112
Q145 1221101
Q146 1202221
Q147 0021221
Q148 0222011
Q149 1022100
Q150 0210100
Q151 0112220
Q152 1020202
Q153 0201212
Q154 0101102
Q155 2002122
Q156 1210111
Q157 1101011
```

---

# 3. High-risk intersections explicitly checked

The covering arrays guarantee tuple inclusion. On top of that, the analysis explicitly checked the following semantic intersections against the hardened concern map.

General 3-way selected-row occurrence counts:

```text
identity evolution + non-read effect                         16 rows
purpose mismatch + persistent config + active DANTE          8 rows
revocation + offline replay + non-read effect                 6 rows
retracted basis + pin + active DANTE                          4 rows
represented/delegated + non-read effect                      16 rows
conflicted basis + late DANTE + provider lag                  2 rows
World-switch-late + revoked disclosure + active DANTE         5 rows
recurrence exception + revision binding + non-read effect     6 rows
identity evolution + World-switch-late + pin                  3 rows
purpose mismatch + specialist missing + active DANTE          4 rows
```

High-risk 4-way selected-row occurrence counts:

```text
retracted basis + revoked + effect + active DANTE             7 rows
identity evolution + revoked + effect                        10 rows
offline replay + revoked + effect + late DANTE                5 rows
represented + retracted basis + effect + active DANTE         8 rows
identity evolution + offline replay + effect + active DANTE   6 rows
purpose mismatch + revision binding + effect + late DANTE     6 rows
```

After CG-37..CG-40 hardening, none requires a new architectural layer.

---

# 4. Hardened guard families used to evaluate rows

The analytical row oracle applies the following rule families as applicable.

```text
basis superseded/retracted
-> CG-36 + WL-H09

basis conflicted/incomplete
-> CG-15 + Reconciliation / no provider-wins

disclosure revoked
-> CG-32 + CG-40 + WL-H11/H12

recipient/purpose mismatch
-> CG-40 + WL-H03/H12

identity ambiguous
-> candidate/unresolved; no auto-merge

identity retired/merge/split
-> CG-38 + CG-39 + WL-H10

revision-bound binding
-> CG-33 + expected-state applicability

represented/delegated actor
-> Domain Representation + WL-H11

pending/ambiguous effect
-> L6 truthful pending/reconciliation

partial/real effect
-> CG-35 + WL-H07

offline replay
-> CG-37 + WL-H05/H06

provider lag/timeout
-> WL-H08; provider != canonical

pinned/saved result
-> CG-21; config != source

concurrent shared config
-> CG-07; explicit revision/conflict

primary/supporting refs
-> CG-18/19

World switch / late result
-> initiating generation/World binding

constrained/a11y presentation
-> L8; semantic identity unchanged

specialist missing
-> CG-09 local safe fallback/failure

DANTE contextual/late action
-> purpose-scoped authorized context + execution revalidation

recurrence/DST
-> existing Domain Time separation

ordering/effective time unclear
-> Reconciliation; arrival order != semantic truth
```

Cross-rule hardenings:

```text
non-read effect + changed basis/disclosure/identity/offline state
-> CG-37 execution-time revalidation

saved/pinned result + invalid basis/disclosure/identity
-> revalidate/redact; never source ownership

active DANTE + invalid basis/disclosure/identity
-> rebuild minimized authorized context or reject attachment

recurrence + revision-bound binding
-> bind to authoritative material occurrence/basis, not series label

missing specialist + restricted disclosure
-> fail safely; never use generic raw-data fallback that leaks
```

Result:

```text
3-way selected rows with no applicable hardened owner  0 / 67
4-way selected rows with no applicable hardened owner  0 / 157
```

---

# 5. How the covering rows were selected

The analytical selection used a greedy set-cover style search over candidate ternary rows.

General matrix:

```text
candidate row sample count  ~30,000
selection target             uncovered 3-tuples
selected rows                67
seed used during analytical generation 42
```

High-risk matrix:

```text
candidate row sample count  ~25,000
selection target             uncovered 4-tuples
selected rows                157
seed used during analytical generation 123
```

Because candidate-set iteration details can vary across implementations, the **fixed vectors above are the canonical evidence**, not an assumption that regenerating from the same pseudo-random seed must produce identical rows.

WS7 should either:

```text
A. consume these fixed vectors and verify coverage + properties;

or

B. implement a deterministic covering-array generator and prove equivalent/full coverage.
```

---

# 6. What this evidence does and does not prove

It proves analytically:

```text
systematic 3-way interaction coverage across 11 axes
systematic 4-way coverage across the 7 highest-risk axes
no unowned row after CG-37..CG-40 hardening
no new ownership layer forced by those combinations
```

It does **not** prove:

```text
TypeScript code implements the oracle
runtime state machine is correct
property-based tests pass
browser behavior is correct
real backend/AuthZ effects are correct
```

Those are WS7/WS8 and later integration obligations.

---

# 7. WS7 carry-forward

At WS7, encode these vectors or equivalent deterministic covering arrays into executable/property-based tests over the actual closed WS6 contracts.

At minimum assert:

```text
no revoked/purpose-mismatched ref leaks through DANTE or cache
no identity-evolved ref silently retargets
no invalid/retracted basis presents as current
no queued/offline effect bypasses execution-time revalidation
no partial effect becomes cancelled history
no config pin owns source truth
no provider lag overwrites canonical truth
no recurrence exception rewrites past Actual
no missing specialist leaks/forges semantics
no narrow/a11y mapping changes semantic identity
```

The reason to preserve the vectors now is simple:

> future WS7 automation should inherit a fixed adversarial space, not reinvent it from memory.
