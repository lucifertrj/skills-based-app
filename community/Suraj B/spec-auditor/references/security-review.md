# Security review

Loaded by `spec-auditor` in any step when the document mentions authentication, authorization, credentials, cryptography, tokens, personally identifiable information (PII), health data (PHI), payment data (PCI), or similar.

Use this file to surface security-specific findings in addition to the generic Steps 1–7.

---

## When to load this reference

Trigger phrases in the document that should cause you to emit `[LOAD] references/security-review.md`:

- authentication, authn, login, signin, SSO, OAuth, OIDC, SAML, JWT
- authorization, authz, RBAC, ABAC, permissions, roles, scopes
- credentials, password, secret, API key, access token, refresh token, bearer
- encryption, cipher, AES, RSA, hashing, hash, salt, KDF, PBKDF2, bcrypt, scrypt, argon2
- TLS, SSL, certificate, mTLS
- PII, PHI, PCI, GDPR, HIPAA, CCPA, SOC 2
- session, cookie, CSRF, XSS, SQL injection, SSRF, RCE

Multiple hits justify the load; a single incidental mention ("uses TLS") does not.

---

## Checks to add on top of the standard workflow

### A. Threat model presence

A spec touching authentication or credentials without a threat model is a Major finding at minimum. The threat model must list:

- **Assets:** what is being protected (tokens, user data, database contents).
- **Actors:** who might attack (external attacker, malicious tenant, compromised insider, misconfigured service).
- **Attack surfaces:** where the attack would enter (public endpoints, internal service calls, config, logs).
- **Mitigations:** what the design does to address each surface.

Finding format: `Step-SEC: No threat model. Spec handles <auth/crypto/etc> without identifying assets, actors, attack surfaces, or mitigations. (Major)`

### B. Credential handling

For every place the spec stores or transmits a credential, confirm:

- **At rest:** named encryption algorithm, named key source (KMS, vault), key rotation policy.
- **In transit:** TLS 1.2+ required, mutual TLS if service-to-service.
- **In memory:** lifetime bounded to request scope where possible.
- **In logs:** never. Redaction must be explicit, not implied.
- **In URLs:** never. Credentials belong in headers or bodies, never query strings.

Finding format per missing item: `Step-SEC: <credential-type> stored <where> without <property>. (Major or Critical depending on exposure)`

### C. Authentication flow

For an authentication flow spec (OAuth, SAML, custom):

- Is the flow named against a standard (e.g. OAuth 2.0 Authorization Code + PKCE)? If "custom auth flow," flag Critical and ask for a stronger justification than "we want to."
- Are tokens scoped? Unscoped tokens are a Major finding.
- Is token revocation defined? An auth flow without revocation is a Major finding.
- Is session lifetime bounded? "Forever" is Critical.
- Are refresh tokens rotated on use? If not, flag Major.
- Is PKCE used for public clients? If not, flag Major.
- Is state / nonce checked for CSRF / replay? If not, flag Critical.

### D. Authorization

- Is the authz model named (RBAC, ABAC, ReBAC, capability-based)? "We'll check permissions" is Major.
- Are the roles / scopes enumerated?
- Is the enforcement point named (gateway, service layer, data layer)? Missing is Major; multiple conflicting points is also Major.
- Is there a deny-by-default default? If unspecified, flag Major.
- Is there a bypass or admin mode? If yes, how is its use logged and audited?

### E. Cryptography

- **Never roll your own.** If the spec describes a custom cipher, custom MAC, custom KDF, or custom handshake, flag Critical and request a cryptographer review.
- Algorithms must be named and current:
  - Symmetric: AES-GCM or ChaCha20-Poly1305. AES-CBC requires a separate MAC; call it out.
  - Asymmetric: RSA-2048+, ECDSA P-256+, Ed25519.
  - Hash: SHA-256+.
  - KDF: Argon2id (preferred), scrypt, or bcrypt for passwords. PBKDF2 with ≥ 600,000 iterations for compat.
- Named algorithms with inadequate parameters are still a finding. `RSA-1024` is Critical.

### F. Input validation and injection

For every external input:

- Where is validation performed? (edge, service, data layer.)
- What is the trust boundary? (inputs from clients are never trusted; inputs from internal services may be, but only if authenticated.)
- How are SQL, NoSQL, command, header, path, and template injections prevented? "We use prepared statements" is a good sentence; "we sanitize inputs" is not.

### G. Data classification and residency

If the spec handles PII, PHI, or PCI:

- Is the data classified in the document?
- Is the jurisdiction specified (GDPR, CCPA, HIPAA, etc.)?
- Is data residency stated? (Can data leave a region? A country?)
- Is there a retention policy? (Finite retention is required under most regimes.)
- Is there an access log? (Required under HIPAA. Best practice under GDPR.)

Missing any of these on a PII/PHI/PCI-handling spec is a Major finding. Missing the jurisdiction is often Critical because the rest cannot be evaluated without it.

### H. Secrets in the document

Grep the document for patterns that look like credentials:

- `AKIA[0-9A-Z]{16}` — AWS access key
- `ghp_[A-Za-z0-9]{36}` — GitHub personal access token
- `xox[baprs]-[A-Za-z0-9-]{10,}` — Slack tokens
- `-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----` — private key header
- Any base64 blob adjacent to the words "token", "secret", "key", "password"

If any match is found, Critical finding. Redact in the audit output. Recommend the author rotate the credential immediately — accidental commits to design docs are as leaky as accidental commits to code.

### I. Logging and observability

- Are PII fields excluded from logs? Explicitly?
- Are security events (login, privilege change, data export) logged with enough detail for forensics?
- Is log retention defined?
- Are log storage and access controls described?

### J. Supply chain

- Are dependencies named with version constraints?
- For any dependency that handles auth, crypto, or secrets, is there an explicit reason for the choice?
- Are dependency updates gated or automated?

---

## Severity calibration

| Signal | Severity |
|---|---|
| Credential appears in document | Critical |
| Custom crypto without cryptographer review | Critical |
| Missing auth/authz on a resource that handles PII | Critical |
| No threat model on an auth-touching spec | Major |
| Unpinned crypto dependency | Major |
| Authz model unnamed | Major |
| Log redaction unspecified | Major |
| No retention policy on PII | Major |
| Algorithm named but parameters weak (e.g. RSA-1024) | Critical |
| TLS version not specified | Minor (assume current default, but flag) |

---

## Finding format

Prefix security findings with `Step-SEC` so they are distinguishable from the main workflow steps in the synthesis.

```
Step-SEC: No threat model for OAuth flow. Spec handles access tokens without
          identifying assets, attackers, or mitigations. (Major)
Step-SEC: L78 "tokens should be stored securely" — no algorithm, no key source,
          no rotation policy. (Major)
Step-SEC: L112 references AWS_SECRET_ACCESS_KEY="AKIA..." — appears to be a
          real credential. REDACTED in this output. Rotate immediately. (Critical)
```

Include Step-SEC findings in the Step 7 synthesis under Critical / Major / Minor alongside the other findings.
