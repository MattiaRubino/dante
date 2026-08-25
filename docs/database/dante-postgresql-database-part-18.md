<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-17.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 18

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DB-U26 DATABASE SECURITY EXECUTION HARDENING CLOSED  
**Scope:** section 57 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–17  
**PRE-SCOPE:** `3a7d744028ef9263bb26d08001807b1a32403fb1`  
**PostgreSQL target:** PostgreSQL 18 major family / current repository patch 18.6  
**Pinned driver evidence:** `psycopg==3.3.4` + `psycopg-binary==3.3.4`  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 17 closed the five concrete semantic/database findings discovered by the second tombstone repair. A separate pre-Gate-03 security request then required a fresh database-execution security audit against the real backend foundation, the frozen Parts 1–17 contract and current PostgreSQL/psycopg behavior.

That audit found **no C finding**, no semantic contradiction and no reason to reopen Domain, Whole Logical or the accepted Physical model. It did identify bounded execution-hardening requirements that must be frozen before CP6-04 is allowed to implement the database.

This Part closes those requirements as `DB-U26`.

No business migration, SQLAlchemy business mapping, PostgreSQL table, view, routine, trigger, index, CHECK, FK, grant or revoke is executed by this document.

Frozen structural counts remain:

```text
DANTE-owned tables                  68
ordinary current views               5
integrity routines                  14
trigger attachments                 75
physical indexes                    95
foreign keys                        68
CHECK constraints                  120
custom DANTE enum/domain/sequence    0
materialized views                   0
RLS policies                         0
```

---

## 57. DB-U26 — Database Security Execution Hardening — CLOSED

### 57.1 Purpose and classification

`DB-U26` closes the database-execution security surface that must be deterministic before implementation begins.

Audit classification:

```text
C — Domain / Logical / Physical contradiction             0
B — bounded database-execution hardening                  5 families
new semantic root                                          0
new baseline PostgreSQL object                             0
baseline count change                                      0
```

The five B families are:

```text
B-SEC-01  query construction / SQL injection boundary
B-SEC-02  search_path / temporary/public object-hijack boundary
B-SEC-03  credentials / SCRAM / database-secret handling
B-SEC-04  runtime/migrator/owner identity + role graph fail-closed posture
B-SEC-05  exact negative PostgreSQL security proof / staged security boundary
```

The old CP3 blanket runtime ACL posture remains the already-known P0 implementation debt frozen by Parts 12–13. It is not reclassified as a new DB-U26 semantic finding.

---

## 58. External technical verification used by DB-U26

The security audit reverified current behavior rather than copying API names from chat memory.

Official authority used:

```text
PostgreSQL 18 — schema/search-path security
https://www.postgresql.org/docs/18/ddl-schemas.html

PostgreSQL 18 — client search_path behavior, including implicit pg_temp ordering
https://www.postgresql.org/docs/18/runtime-config-client.html

PostgreSQL 18 — safe function search_path guidance
https://www.postgresql.org/docs/18/sql-createfunction.html

PostgreSQL 18 — libpq PQencryptPasswordConn / PQchangePassword
https://www.postgresql.org/docs/18/libpq-misc.html

PostgreSQL 18 — password authentication / SCRAM
https://www.postgresql.org/docs/18/auth-password.html

PostgreSQL 18 — SET ROLE semantics
https://www.postgresql.org/docs/18/sql-set-role.html

psycopg 3 — pq.PGconn low-level API
https://www.psycopg.org/psycopg3/docs/api/pq.html
```

Verified implications:

```text
- schemas in search_path are trust surfaces when an untrusted principal can CREATE there;
- pg_catalog is implicitly searched first when omitted;
- pg_temp, when it exists and is omitted, is implicitly searched before pg_catalog for relation/type names;
- listing pg_temp explicitly last prevents that implicit-first relation/type lookup behavior;
- libpq provides password-encryption/password-change helpers specifically to avoid sending the original cleartext password in ALTER ROLE/USER commands;
- psycopg 3.3.4 exposes the corresponding PGconn password APIs;
- SCRAM-SHA-256 is the required DANTE password-storage/authentication baseline; MD5 storage is not accepted;
- SET ROLE changes current_user while session_user remains the login identity and does not by itself make arbitrary role escalation acceptable.
```

These external facts constrain implementation only. They do not redefine DANTE semantic authority.

---

## 59. SEC-QRY — SQL query-construction contract

### 59.1 Business/user values are always data

Any value originating from a request, product state, provider payload, user-controlled content or mutable business data MUST be transmitted as a parameter/value, never as SQL syntax.

Allowed baseline:

```text
SQLAlchemy Core / ORM expression construction

or

SQLAlchemy text(<static statement>)
+ named bound parameters

or

psycopg execute(<static/composed statement>, params)
```

Forbidden baseline:

```text
f-string containing business/untrusted values
%-formatting containing business/untrusted values
str.format() containing business/untrusted values
string concatenation containing business/untrusted values
caller-provided arbitrary WHERE / ORDER BY / JOIN / SQL fragments
"trusted because frontend validated it" as a database security argument
```

Escaping a value manually is not a substitute for parameter binding.

### 59.2 SQL identifiers are a separate security class

PostgreSQL identifiers cannot be treated as value parameters.

Dynamic identifier construction is allowed only when there is a real bounded technical need and the caller cannot choose arbitrary SQL syntax.

Required order of preference:

```text
1. static schema/table/column/routine identifiers;
2. SQLAlchemy schema objects / mapped metadata;
3. exact internal allow-list mapped to known identifiers;
4. psycopg.sql.Identifier for the resulting known identifier.
```

Forbidden:

```text
raw caller-provided table name
raw caller-provided schema name
raw caller-provided column/expression
raw caller-provided function name
identifier passed through quoting and then assumed semantically authorized
```

Quoting makes an identifier syntactically safe; it does not make an arbitrary identifier semantically allowed.

### 59.3 Current foundation audit result

The current pre-business backend has no discovered business query path that constitutes an exploitable SQL-injection surface.

Positive existing foundation facts retained:

```text
runtime readiness SQL is static
DatabaseSettings constructs SQLAlchemy URLs structurally rather than concatenating DSNs
provisioning uses psycopg.sql.Identifier for genuinely dynamic database identifiers
current business migration is empty
business SQLAlchemy mappings do not yet exist
```

This is not permission for CP6-04 to introduce unsafe construction.

### 59.4 Fourteen integrity routines — zero generic dynamic SQL baseline

The 14 frozen integrity routines operate over a database schema known at authoring time.

Therefore:

```text
baseline PL/pgSQL dynamic EXECUTE                         0
generic table/routine identifier supplied through TG_ARGV 0
runtime-supplied SQL fragment                             0
```

Known DANTE relations/routines MUST be referenced statically and schema-qualified where resolution matters.

A future use of dynamic SQL requires a new concrete requirement, a bounded identifier allow-list/composition contract and a dedicated security review. It is not available as an implementation convenience during CP6-04.

### 59.5 Injection proof is a construction proof, not one payload

CP6-05 MUST NOT claim "SQL injection tested" merely because one quote/semicolon payload failed.

Qualifying evidence combines:

```text
construction-policy review/static checks
+
malicious-value tests proving values remain data
+
bounded-identifier rejection tests where such a path exists
+
integrity-routine source/catalog proof of zero baseline dynamic EXECUTE
```

---

## 60. SEC-PATH — search_path and object-hijack contract

### 60.1 Why the earlier `dante,public` envelope is not the final baseline

Current CP3 foundation uses `dante,public` in runtime/migration connection setup.

DB-U21 already freezes the future privilege posture:

```text
runtime CREATE on dante     NO
runtime USAGE on public     NO
runtime CREATE on public    NO
runtime TEMP                NO
migrator direct dante USAGE NO
migrator public USAGE       NO
migrator public CREATE      NO
migrator TEMP               NO
PUBLIC CREATE on public     NO
```

That posture removes the obvious current DANTE-role hijack path, but DB-U26 makes resolution deterministic rather than relying only on privilege side effects.

### 60.2 Final technical session search_path

For DANTE runtime and migration sessions, the CP6 materialized baseline MUST use:

```text
pg_catalog, dante, pg_temp
```

Properties:

```text
pg_catalog
→ explicit first trusted built-in namespace

dante
→ sole DANTE application schema in ordinary resolution

pg_temp
→ explicitly last
→ prevents PostgreSQL's implicit "temporary schema first" relation/type lookup behavior
```

`public` is not part of the baseline DANTE runtime/migrator search path.

A later extension-backed feature that genuinely requires objects in another schema must activate that exact schema/object privilege and resolution contract explicitly; it must not restore a broad `public` trust surface by convenience.

### 60.3 Schema qualification remains mandatory for privileged/static code

A safe session search path does not justify casual unqualified privileged SQL.

Provisioning, migration DDL and integrity routines SHOULD schema-qualify DANTE relations/routines where PostgreSQL grammar permits and where ambiguity/object masking could matter.

Built-in function/operator semantics that are security-sensitive SHOULD use explicit `pg_catalog` qualification or otherwise be proven independent of an untrusted search path.

### 60.4 Integrity routine function-level search_path

Part 16 froze `pg_catalog,dante` for the 14 routines. DB-U26 narrowly hardens that execution contract to:

```text
function search_path = pg_catalog, dante, pg_temp
```

Reason: PostgreSQL documents that an existing temporary schema omitted from `search_path` is searched first for relation/type names. Explicit `pg_temp` last removes that implicit-first behavior.

This is a security hardening only; it changes no routine count, trigger attachment, routine semantic role or business invariant.

All 14 routines remain:

```text
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
leakproof = false
owner = dante_owner
PUBLIC EXECUTE = revoked
dante_runtime direct EXECUTE = revoked
dante_migrator direct EXECUTE = revoked
```

### 60.5 TEMP denial is independently required

The safe search path and TEMP denial are complementary defenses.

Baseline remains:

```text
dante_runtime TEMPORARY  NO
dante_migrator TEMPORARY NO
PUBLIC TEMPORARY         NO
```

CP6-05 must prove both privilege denial and effective search-path ordering.

---

## 61. SEC-CRED — password, SCRAM and secret-handling contract

### 61.1 Current provisioning finding

Current CP3 provisioning correctly protects SQL syntax by wrapping password text as a psycopg literal, but it still constructs a password-bearing `ALTER ROLE ... PASSWORD <cleartext>` command.

That is syntactically injection-safe but does not satisfy the final credential-leakage baseline.

PostgreSQL explicitly recommends avoiding the original cleartext password in such SQL because it can surface in command logs/activity displays.

### 61.2 Final password algorithm

DANTE database login-role password material MUST use:

```text
SCRAM-SHA-256
```

Forbidden:

```text
MD5 verifier generation
MD5 as an accepted DANTE password-storage fallback
cleartext password literal embedded in SQL text
```

Implementation MUST be deterministic rather than relying silently on a mutable server default.

### 61.3 Approved psycopg/libpq implementation family

The pinned stack is:

```text
psycopg        3.3.4
psycopg-binary 3.3.4
```

The implementation MUST use the real psycopg/libpq password facility rather than hand-building cleartext password SQL.

Accepted design family:

```text
A. verify/set the provisioning session password_encryption contract to scram-sha-256;
B. use psycopg PGconn/libpq password-change functionality that encrypts before issuing ALTER USER/ROLE;

or

A. use PGconn password encryption explicitly with algorithm scram-sha-256;
B. send only the resulting verifier through an identifier-safe bounded role-password command.
```

The concrete CP6-04 implementation must be tested against the pinned driver and PostgreSQL 18.6. Conversation-memory pseudo-APIs are not accepted.

### 61.4 Verifiers remain sensitive

Replacing cleartext SQL with a SCRAM verifier does not make logs unrestricted.

Do not log:

```text
cleartext passwords
SCRAM verifiers
full credential-bearing DSNs
SecretStr revealed values
provisioning connection URLs
migration/runtime passwords
```

`hide_parameters=True`, `SecretStr` redaction and current non-debug production posture are retained.

Operational SQLSTATE, constraint names, table names and bounded non-secret diagnostics remain available; security hardening must not make PostgreSQL supportability blind.

### 61.5 Owner credential posture

`dante_owner` is a NOLOGIN ownership role and MUST have no retained password credential.

Final required posture:

```text
dante_owner.rolcanlogin = false
dante_owner.rolpassword = NULL
```

P0/provisioning must remove an inherited/residual password if the role pre-existed with one.

Only the two login identities require DANTE role credentials:

```text
dante_migrator
dante_runtime
```

Admin/bootstrap credentials remain outside normal application settings/runtime.

### 61.6 Repository/local secret posture retained

Current positive baseline remains:

```text
SecretStr for application/provisioning passwords
SQLAlchemy URL.create rather than manual DSN concatenation
runtime engine hide_parameters=True
no implicit .env.local loading
local Docker postgres superuser secret from a file-backed Compose secret
*.local secret path ignored by Git
readiness response contains no database connection detail
```

Deployment secret-manager selection/rotation infrastructure remains a later deployment-security concern, not an excuse to weaken the database-side handling frozen here.

---

## 62. SEC-ID — exact database identity and role graph

### 62.1 Three DANTE database roles remain the only baseline topology

```text
dante_owner
  NOLOGIN
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  no password

dante_migrator
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS

dante_runtime
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
```

### 62.2 Runtime identity is not configurable to an arbitrary PostgreSQL role

Application database login identity is semantically fixed:

```text
session_user = dante_runtime
current_user = dante_runtime
```

Normal backend startup MUST fail closed when the effective connection identity is not exactly `dante_runtime`.

A configuration field containing a syntactically valid alternate username does not make that username authorized.

In particular normal backend runtime MUST reject operation under:

```text
postgres
dante_owner
dante_migrator
arbitrary custom role
```

CP6-04 may implement this through configuration validation plus a connection/startup assertion; direct PostgreSQL identity is the final proof.

### 62.3 Migration login and elevation precondition

Alembic migration login identity is exactly:

```text
session_user = dante_migrator
current_user = dante_migrator
```

before elevation.

Only after this exact precondition is verified may the migration session execute:

```text
SET ROLE dante_owner
```

After elevation the expected identity is:

```text
session_user = dante_migrator
current_user = dante_owner
```

An injected Alembic URL/test connection is not permitted to bypass the production migration-identity contract. Test-only harnesses may inject connection mechanics, but qualifying migration security proof must still assert the effective login/current-role state appropriate to the tested mode.

`SET ROLE` target is static; caller-selected target roles are forbidden.

### 62.4 Exact role-membership graph — new fail-closed hardening

Role attributes alone are insufficient. A pre-existing unexpected membership can create an escalation path even when the named roles themselves are NOINHERIT/NOSUPERUSER.

For the DANTE baseline, the **only membership edge involving any of the three DANTE roles** is:

```text
granting role  dante_owner
member         dante_migrator
INHERIT        FALSE
SET            TRUE
ADMIN          FALSE
```

Equivalent PostgreSQL 16+ membership semantics:

```text
GRANT dante_owner TO dante_migrator
WITH INHERIT FALSE, SET TRUE, ADMIN FALSE
```

No other direct membership may exist where any DANTE role is either the granted role or the member.

Therefore:

```text
dante_runtime belongs to                         0 roles
dante_owner belongs to                           0 roles
dante_migrator belongs to                        exactly {dante_owner}

unexpected members of dante_owner                0
unexpected members of dante_migrator             0
unexpected members of dante_runtime              0

unexpected transitive SET ROLE path from runtime 0
unexpected transitive SET ROLE path to owner      0
```

A PostgreSQL superuser/bootstrap administrator remains operationally outside this membership graph; superuser capability is not normal DANTE runtime/migration authority.

### 62.5 Provisioning reconciliation must be fail closed

P0/provisioning must inspect and reconcile the actual membership topology, not merely issue one `REVOKE dante_owner FROM dante_runtime` and assume no alternate path exists.

If the database contains an unexpected edge involving a DANTE role, provisioning must either remove the edge as part of the explicitly authorized exact reconciliation or fail closed. It must never silently bless the cluster as matching DANTE security posture.

### 62.6 No self-service privilege escalation

Runtime remains unable to:

```text
CREATE ROLE
ALTER ROLE
grant itself a role
SET ROLE dante_owner
SET ROLE dante_migrator
SET ROLE any unrelated privileged role
CREATE/ALTER/DROP DANTE schema objects
TRUNCATE business tables
EXECUTE the 14 integrity routines directly
```

Database role security does not replace future product AuthN/AuthZ.

---

## 63. SEC-MIG — migration and P0/M1/M7 security boundary

### 63.1 P0 remains before M1

Part 13 remains authoritative:

```text
P0 cp6_provisioning_acl_hardening
MUST be in effect before M1 creates a CP6 business table
```

DB-U26 extends P0's exact implementation responsibility to include the database-execution hardening frozen here:

```text
- exact trusted session search_path posture;
- public/TEMP hardening already frozen by DB-U21;
- exact DANTE role attribute reconciliation;
- exact DANTE role-membership graph reconciliation;
- owner password removal;
- SCRAM-SHA-256 credential update path without cleartext password SQL;
- no provisioning rerun that broadens migration-owned M7 object ACLs.
```

This changes no Alembic node count.

### 63.2 M1 fail-closed preflight additions

Before M1 may create the first business relation, direct preflight must establish at least:

```text
P0 complete
runtime/migrator/owner attributes exact
DANTE membership graph exact
owner NOLOGIN + no password
PUBLIC/database/schema/TEMP posture exact
runtime/migrator effective search_path contract exact
migration login = dante_migrator
post-SET-ROLE current_user = dante_owner
legacy broad default runtime grants removed
```

Failure of any required preflight condition aborts before business DDL.

### 63.3 M7 remains the sole baseline runtime business-DML activation stage

Nothing in DB-U26 grants runtime business DML earlier.

M1..M6 remain deny-before-activation; M7 materializes the exact DB-U21/Part17 object ACL surface.

A later P0/provisioning rerun MUST NOT broaden M7's migration-owned object ACLs.

### 63.4 Migration SQL construction

Migration object names are static blueprint identifiers. Migration code must not accept arbitrary external schema/table/function names.

Alembic migrations MUST use explicit `schema="dante"`/qualified DDL where applicable and must not depend on `public` resolution.

Non-transactional migration operations remain subject to the existing CP6-02 MIG contract; DB-U26 does not introduce one.

---

## 64. SEC-LOG — diagnostics and logging boundary

### 64.1 Secret material never becomes ordinary diagnostic context

Forbidden in application/CI/migration/provisioning logs:

```text
plaintext DB password
SCRAM verifier
full password-bearing URL/DSN
SecretStr revealed value
raw environment dump containing secrets
password-bearing SQL statement
```

### 64.2 Structural PostgreSQL diagnostics remain usable

Allowed when non-secret:

```text
SQLSTATE
constraint name
schema/table/column name
DANTE stable error code
bounded invariant identifier
migration revision identifier
role name
```

Trigger/routine error `DETAIL` fields must remain bounded to structural/semantic diagnostic facts and must not echo arbitrary user payloads or credentials.

### 64.3 SQLAlchemy logging posture

Baseline retains:

```text
engine echo = false
pool echo = false
hide_parameters = true
```

A future diagnostic mode must not disable parameter hiding in production merely to simplify debugging.

---

## 65. SEC-PROOF — exact direct PostgreSQL security proof additions

DBP-01..DBP-20 remain frozen by Part 16. DB-U26 adds security obligations to the same CP6-04/05 proof system; it does not create a parallel security test framework.

### 65.1 Query-construction / injection proof

Prove:

```text
malicious text containing quotes/semicolon/comment tokens remains a bound value
statement shape is unchanged by malicious value content
arbitrary identifier/SQL-fragment business API does not exist
any bounded identifier API rejects values outside its internal allow-list
baseline integrity routine source contains no dynamic EXECUTE construction
```

### 65.2 Search-path / hijack proof

As actual roles, prove:

```text
runtime SHOW search_path / current_schemas matches trusted baseline
migrator migration session matches trusted baseline
pg_temp is explicitly last
public is absent from baseline runtime/migration search_path
runtime CREATE in dante denied
runtime CREATE in public denied
runtime CREATE TEMP TABLE denied
migrator direct CREATE in dante denied before SET ROLE
PUBLIC CREATE on public denied
```

Where a disposable privileged test fixture can safely create adversarial objects, prove that an identically named temp/public object cannot redirect the DANTE integrity/migration path.

### 65.3 Routine security proof

For all 14 routines, introspect and prove:

```text
SECURITY INVOKER
owner = dante_owner
search_path = pg_catalog,dante,pg_temp
PUBLIC EXECUTE denied
runtime direct EXECUTE denied
migrator direct EXECUTE denied
zero unexpected SECURITY DEFINER routine
zero baseline dynamic SQL integrity routine
```

### 65.4 Credential/SCRAM proof

Using disposable roles/secrets only, prove:

```text
PostgreSQL target = 18.6 qualifying environment
pinned psycopg password API path works
resulting login credential is SCRAM-SHA-256, not MD5
provisioning path does not construct cleartext password-bearing SQL
owner NOLOGIN role has no password verifier
secret/password/verifier is absent from captured application/provisioning logs and exception text
```

Tests must not print the disposable secret on failure.

### 65.5 Identity / role graph proof

Catalog plus live-session proof must establish:

```text
runtime session_user/current_user = dante_runtime
migration pre-elevation session_user/current_user = dante_migrator
migration post-elevation session_user = dante_migrator
migration post-elevation current_user = dante_owner
runtime SET ROLE dante_owner denied
runtime SET ROLE dante_migrator denied
runtime SET ROLE via any transitive DANTE membership denied
only allowed DANTE role edge = dante_owner → dante_migrator
membership options = INHERIT false / SET true / ADMIN false
unexpected DANTE membership edges = 0
```

### 65.6 ACL / privilege-escalation proof

Retain and extend DBP-10/DB-U21 evidence:

```text
runtime cannot grant itself privileges
runtime cannot CREATE/ALTER/DROP schema objects
runtime cannot TRUNCATE
runtime cannot write shared base current-control tables directly
runtime cannot bypass current-view facet CHECK OPTION
runtime cannot direct-call integrity routines
PUBLIC cannot execute integrity routines
P0 before M1 is fail closed
M1..M6 expose no business DML
M7 grants exactly the frozen ACL matrix
post-M7 provisioning rerun does not broaden M7 ACLs
```

### 65.7 Proof honesty

Part 18 freezes proof obligations; it does not claim those future CP6-04/05 tests have executed.

Current status:

```text
DB-U26 design/security audit            COMPLETE
Part-18 execution contract              FROZEN
CP6-04 implementation                   NOT STARTED
CP6-05 direct PostgreSQL DB-U26 proof   STAGED / NOT YET EXECUTED
```

---

## 66. Security scope separation — frozen

### 66.1 Database security — current CP6 authority

The following are database concerns and are owned by CP6-03/04/05:

```text
SQL/query construction
SQL injection resistance
identifier construction
PL/pgSQL dynamic-SQL posture
PostgreSQL roles and exact membership graph
object/database/schema ACLs
search_path and object masking
TEMP/public trust surface
routine/trigger execution posture
password/SCRAM handling at the DB provisioning boundary
DB URL/parameter/verifier leakage prevention
migration SET ROLE escalation boundary
real PostgreSQL negative security proof
```

### 66.2 Deployment security — intentionally staged

Before real production deployment the platform/deployment work must decide and prove, as applicable:

```text
TLS / verify-full or managed-platform equivalent
CA/certificate trust strategy
private networking/firewall/VPC exposure
production PostgreSQL service controls
secret manager and operational rotation
backup encryption and restore-access control
PgBouncer production auth/TLS if activated
host/image/runtime hardening and patch process
```

These concerns are real but no current CP6-03 database blueprint fact determines their exact production topology.

### 66.3 Application/API security — intentionally staged to real application layers

The database blueprint does not invent persistence schema merely to pre-answer:

```text
AuthN
product AuthZ
IDOR/BOLA
mass assignment
rate limiting
CSRF
CORS
SSRF
XSS
file upload security
session/JWT/token security
product-level disclosure policy
```

WL-H11/WL-H12 remain upstream constraints and will govern future application design, but DB-U26 does not fabricate an Account/Permission/JWT/security schema without a real product contract.

---

## 67. Part-18 narrow supersessions

Part 18 changes no earlier semantic/object inventory.

It narrowly supersedes only these execution-security details:

```text
Part 12 / Part 16 compatibility wording that allowed runtime search_path dante,public
→ final CP6 implementation baseline is pg_catalog,dante,pg_temp

Part 16 integrity-routine search_path pg_catalog,dante
→ hardened to pg_catalog,dante,pg_temp

current CP3 provisioning cleartext password-bearing ALTER ROLE construction
→ implementation debt; CP6 P0 must use verified psycopg/libpq SCRAM-safe password handling

current arbitrary DatabaseSettings.user shape
→ does not imply runtime-role freedom; effective runtime identity must be exactly dante_runtime

current role-attribute reconciliation
→ insufficient alone; P0 must reconcile the exact whole DANTE membership graph and owner no-password posture
```

All earlier counts, names, FK/CHECK/index manifests, current/history semantics, migration allocation, SQLAlchemy mapping plan and Dictionary readiness remain intact.

---

## 68. Dictionary reconciliation from DB-U26

The Database Dictionary v1 security model remains structurally valid.

No object entry exists yet, so DB-U26 requires no object-specific JSON migration.

When the 14 routine entries materialize, their exact security facts must include:

```text
security mode          SECURITY INVOKER
owner                  dante_owner
function_search_path   ["pg_catalog", "dante", "pg_temp"]
direct runtime execute false
PUBLIC execute         false
```

Table/view grants remain governed by DB-U21 + Part17.

The semantic validator must treat unexpected routine search-path values, owner/ACL drift and later materialized security facts as defects.

Role membership itself remains a technical-foundation/P0 proof surface rather than a fake standalone Dictionary business object.

---

## 69. Final DB-U26 closure ledger

```text
SQL value binding contract                         CLOSED
identifier allow-list/composition contract        CLOSED
arbitrary SQL fragment posture                    FORBIDDEN
14-routine dynamic EXECUTE baseline               0
runtime/migration trusted search_path             FROZEN
pg_temp implicit-first hijack gap                 CLOSED BY EXPLICIT-LAST CONTRACT
public runtime/migrator trust surface             REMOVED FROM BASELINE PATH
runtime/migrator TEMP                             DENIED
routine function search_path                      HARDENED
cleartext password-bearing SQL                    FORBIDDEN FOR FINAL P0
SCRAM-SHA-256                                      REQUIRED
pinned psycopg/libpq password API                 VERIFIED AVAILABLE
owner password                                    FORBIDDEN / NULL
runtime effective role                            dante_runtime EXACT
migration login role                              dante_migrator EXACT
migration SET ROLE target                         dante_owner EXACT
allowed DANTE membership edges                    1
unexpected DANTE membership edges                 0
negative PostgreSQL security proof                FROZEN / STAGED
production deployment security                    STAGED TO DEPLOYMENT
application/API security                          STAGED TO APPLICATION/VERTICAL
Domain reopen                                     0
Logical reopen                                    0
Physical reopen                                   0
new DB object                                     0
structural count changes                          0
```

`DB-U26` is therefore **CLOSED as a CP6-03 database blueprint/security-design item**.

This is not CP6-05 execution evidence. The implementation and direct PostgreSQL proofs remain staged to CP6-04/05.

---

## 70. Mandatory final independent replay before Gate 03

Closing DB-U26 does **not** itself earn Gate 03.

The next operation is one fresh independent replay over the complete authority:

```text
Domain 57/57
15 native owners
Whole Logical + WL-H01..WL-H12
accepted Physical PostgreSQL mapping
CP6-01 57 + non-57/cross-cutting ledger
CP6-02 Constitution
Database Reference Parts 1–18 as one authority
final 68-table inventory
scoped families
MaterialState facets
PK/FK/UQ/CHECK manifest
95 indexes
14 routines
75 triggers
5 views
current/history/lifecycle
Recurrence and Occurrence-generation repairs
ACL/history column grants
P0/M1/M7 posture
SQLAlchemy mapping plan
advisory-lock/concurrency plan
Dictionary readiness
DBP-01..20 + DB-U26 proof additions
real backend/provisioning/migration/test drift
query construction / injection boundary
role escalation / membership graph
search_path / temp/public object hijack
credentials / SCRAM / logging
all tombstone/no-DDL supersessions
all staged-evidence honesty
```

The replay MUST start from zero and MUST NOT inherit PASS from the prior Parts 1–17 review.

Required clean target:

```text
missing concept                       0
unclassified concept/family           0
unresolved DB-U                       0
Domain/Logical/Physical reopen         0
new accidental semantic root           0
generic semantic fallback              0
dangling scoped family                 0
dangling MaterialState facet           0
contradictory supersession             0
missing structural constraint          0
missing lifecycle/history rule         0
missing ACL/security decision          0
missing index justification            0
SQL injection construction gap         0
privilege-escalation gap               0
search-path/object-hijack gap          0
credential/log secret-handling gap     0
backend/docs drift                     0
speculative schema                     0
```

Any real B/C finding must be repaired and the affected replay repeated. Gate 03 is not granted by elapsed effort.

If the replay is clean, record Gate 03 through a separate exact write gate and STOP before CP6-04.
