# PyGithub Object Groupings & Development Plan

For **each object** listed below, we plan to complete the following **development steps** (in order) before marking it fully done:

1. **Schemas & Schema Tests**: Define any request/response schemas or data models and their corresponding unit tests.  
2. **Converters & Converter Tests**: Implement any conversions or mappings between internal data structures and PyGithub’s objects, plus tests.  
3. **Operations & Operations Tests**: Implement the actual logic (CRUD or any needed interactions), with unit/integration tests.  
4. **Tool Inclusion & Tool Tests**: Finalize user-facing entry points, expose as an MCP tool, plus relevant test coverage and UAT.

---

## Phase 1: Core Parity + Projects

### A. Repository Management & Basic Git Objects
- [ ] `Repository`
- [ ] `Branch`
- [ ] `Commit`
- [ ] `GitRef`
- [ ] `GitTag`
- [ ] `GitBlob`
- [ ] `ContentFile`
- [ ] `GitTree` (optional advanced commit-tree manipulation)

### B. Issue & Comment Management
- [ ] `Issue`
- [ ] `IssueComment`
- [ ] `Label`
- [ ] `Milestone`
- [ ] `Reaction` (often used in issues/PR comments)

### C. Pull Request Lifecycle
- [ ] `PullRequest`
- [ ] `PullRequestReview`
- [ ] `PullRequestComment`
- [ ] `CommitStatus`
- [ ] `CommitCombinedStatus`

### D. Search & Discovery
- [ ] General Search Endpoints (mapping to `Repository`, `Issue`, `PullRequest`, `NamedUser`, etc.)
- [ ] `Search code`
- [ ] `Search issues`
- [ ] `Search users`

### E. **Projects** (Optional but High Priority for Internal Use)
- [ ] `Project`
- [ ] `ProjectCard`
- [ ] `ProjectColumn`

> **Goal**: Achieve parity with the official server’s capabilities for typical repositories/issues/PRs/search, plus add GitHub Projects early for your internal needs.

---

## Phase 2: Collaboration & Community

### A. GitHub Discussions
- [ ] `DiscussionBase`
- [ ] `DiscussionCommentBase`
- [ ] `RepositoryDiscussion`
- [ ] `RepositoryDiscussionComment`
- [ ] `RepositoryDiscussionCategory`

### B. Gists
- [ ] `Gist`
- [ ] `GistFile`
- [ ] `GistComment`

### C. Social Interactions
- [ ] `Stargazer` (via listing stargazers)
- [ ] `Watchers` (listing watchers/forks might rely on repository endpoints)
- [ ] Additional usage of `Reaction` (already partly in Phase 1 but also relevant here)

> **Goal**: Expand beyond basic issues/PRs into more interactive community features like Discussions and Gists.

---

## Phase 3: Security & Advanced Code/Artifact Management

### A. Security Alerts & Code Scanning
- [ ] `CodeScanAlert`
- [ ] `CodeScanAlertInstance`
- [ ] `CodeScanAlertInstanceLocation` (if needed)
- [ ] `DependabotAlert`
- [ ] `AdvisoryBase`
- [ ] `AdvisoryVulnerability`
- [ ] `AdvisoryVulnerabilityPackage`
- [ ] `GlobalAdvisory` (for global scope, if relevant)

### B. Deployments & Environments
- [ ] `Deployment`
- [ ] `DeploymentStatus`
- [ ] `Environment`
- [ ] `EnvironmentProtectionRule`
- [ ] `EnvironmentProtectionRuleReviewer` (if implementing advanced environment rules)

### C. Releases & Artifacts
- [ ] `GitRelease`
- [ ] `GitReleaseAsset`
- [ ] `Artifact`

> **Goal**: Provide advanced functionality for production pipelines—security scanning, deployments, environment protection, and release management.

---

## Phase 4: Enterprise & Administrative

### A. Enterprise Administration
- [ ] `Enterprise`
- [ ] `NamedEnterpriseUser`
- [ ] `EnterpriseConsumedLicenses`
- [ ] `OrganizationDependabotAlert` (for org-wide security issues)

### B. Analytics / Statistics
- [ ] `StatsCodeFrequency`
- [ ] `StatsCommitActivity`
- [ ] `StatsParticipation`
- [ ] `StatsPunchCard`
- [ ] `Referrer`
- [ ] `Clones`
- [ ] `Traffic`

### C. Miscellaneous / Edge Cases
- [ ] `Hook`, `HookDelivery`, `HookDeliveryRequest`, `HookDeliveryResponse`
- [ ] `SourceImport`

> **Goal**: Support larger org use cases and advanced analytics or administrative endpoints rarely needed by smaller projects.

---

## Configurable “Tool Groups”

Because we plan for configurations for the server that can toggle which tools are exposed, each phase can effectively become one or more “tool groups.” For example:

- **Core**: (Phase 1) Repositories, Issues, Pull Requests, Code Search (plus Projects for internal demand).
- **Collaboration**: (Phase 2) Discussions, Gists, social interactions.
- **Security**: (Phase 3) Dependabot, code scanning, deployments.
- **Enterprise**: (Phase 4) Admin, analytics, advanced hooks.

This modular design lets users opt into features incrementally while we systematically cover the entire PyGithub set of objects.
We can always reorganize or reprioritize based on user demand.
