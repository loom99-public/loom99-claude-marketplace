# Config/Infrastructure Evaluation Profile

## Characteristics
- Configuration files (YAML, JSON, TOML, etc.)
- Infrastructure as Code (Terraform, CloudFormation, etc.)
- CI/CD pipelines (GitHub Actions, etc.)
- Docker/container configs
- No direct "runtime" - validated by deployment/application

## ALWAYS RUN (~20 seconds)

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Syntax valid | Parse file | No syntax errors |
| Schema valid | Validate against schema (if exists) | No schema violations |
| Required fields | Check for mandatory config | All required present |
| No secrets | Grep for patterns | No hardcoded secrets |
| References resolve | Check file paths, env vars | Referenced items exist |

## RUN IF APPLICABLE

| Check | Condition | How |
|-------|-----------|-----|
| Terraform plan | Is Terraform | `terraform plan` succeeds |
| Docker build | Is Dockerfile | `docker build` succeeds |
| CI syntax | GitHub Actions/etc. | Linter validates |
| Env example | Has .env.example | All vars documented |
| K8s validation | Is K8s manifests | `kubectl --dry-run` |

## SKIP UNLESS USER REQUESTS

| Check | Why Skip | When User Might Request |
|-------|----------|------------------------|
| Actual deployment | Dangerous | "Test in staging" |
| Cost estimation | Requires cloud APIs | "How much will this cost?" |
| Security scanning | Specialized tool | "Security review" |
| Drift detection | Requires state | "Does infra match config?" |

## SKIP ENTIRELY

| Check | Reason |
|-------|--------|
| Runtime testing | Config doesn't run |
| UI testing | No UI |
| Unit tests | Config isn't code |
| API testing | No API |
| Performance testing | Not applicable |

## Common Config Blind Spots

Check these specifically:
- **Environment-specific values**: Are prod values hardcoded?
- **Default credentials**: Default passwords, keys
- **Resource sizing**: Reasonable CPU/memory limits?
- **Networking**: Correct ports, security groups
- **Dependencies**: Order of operations correct?
- **Rollback**: Can this be safely reverted?

## Secret Detection

Scan for these patterns:
```
password=
secret=
api_key=
apikey=
token=
AWS_SECRET
PRIVATE_KEY
-----BEGIN RSA
-----BEGIN OPENSSH
```

If found: **FAIL** - secrets must use env vars or secret management.

## Validation Commands by Type

**Terraform:**
```bash
terraform fmt -check
terraform validate
terraform plan -out=plan.tfplan
```

**Docker:**
```bash
docker build -t test:local .
hadolint Dockerfile  # if available
```

**GitHub Actions:**
```bash
# Use actionlint if available
actionlint .github/workflows/*.yml
```

**Kubernetes:**
```bash
kubectl apply --dry-run=client -f manifest.yaml
kubeval manifest.yaml  # if available
```

**JSON/YAML:**
```bash
# JSON syntax
python -m json.tool < config.json

# YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

## Evidence to Capture

```
File: <path>
Type: <terraform/docker/k8s/etc>
Syntax: valid/invalid
Schema: valid/invalid/no schema
Secrets found: yes/no
Validation command: <command>
Validation result: <output>
```

## User Validation Suggestions

> "Config files cannot be fully validated without deployment. To verify:
> 1. Deploy to a non-production environment
> 2. Verify the application/service starts correctly
> 3. Check logs for configuration warnings"
