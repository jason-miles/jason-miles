<!--
  This README is partly generated. The hero banner, the "Currently building"
  strip and the project spec cards are SVGs rebuilt nightly by
  .github/workflows/profile-refresh.yml (scripts/generate_*.py, sharing the
  brand kit in scripts/brand.py — one embedded typeface, one red accent).
  Edit prose freely; regenerate visuals with `python3 scripts/generate_*.py`.
-->

<p align="center">
  <a href="https://jason-miles.github.io">
    <img src="assets/hero.svg" alt="Jason Miles — Senior Solutions Architect at Databricks" width="100%" />
  </a>
</p>

<p align="center">
  <a href="https://jason-miles.github.io"><b>Homepage</b></a>
  &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/jasonmiles/"><b>LinkedIn</b></a>
  &nbsp;·&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet"><b>Credentials wallet</b></a>
</p>

---

## About

I'm a Solutions Architect at Databricks, helping enterprise customers turn data and AI ambitions into production reality on the Data Intelligence Platform — from architecture and POC delivery to scaling ML and Generative AI workloads in production.

My focus spans Unity Catalog and Delta Lake governance, Lakeflow / Spark Declarative Pipelines, Structured Streaming, MLflow, Vector Search, and Agent systems. Databricks Certified across the Data Engineer, Machine Learning Engineer, and Generative AI tracks. Facilitator for the Databricks Vibe Coding workshop series.

Based in London · working with customers across the UK, EMEA, and South Africa.

<br/>

<p align="center">
  <img src="assets/now.svg" alt="Currently building — most recently updated public repositories" width="100%" />
</p>

---

## Featured projects

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/jason-miles/sentinel-app"><img src="assets/proj-sentinel.svg" alt="Sentinel — Fraud & AML" width="100%" /></a>
      <p><sub>Multi-tenant fraud &amp; AML detection — one codebase, per-bank branding (Capitec · Nedbank · Investec), shipped as a Databricks App.</sub></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/jason-miles/discovery-vitality-pulse-app-V1"><img src="assets/proj-vitality.svg" alt="Discovery Vitality Pulse" width="100%" /></a>
      <p><sub>Shared-value analytics portal quantifying how healthier member behaviour lowers claims and funds rewards — a governed Databricks App with an Ask-Genie NL hub.</sub></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/jason-miles/dbx-mlpro-cert"><img src="assets/proj-mlpro.svg" alt="Databricks ML Professional exam prep" width="100%" /></a>
      <p><sub>171-question ML Professional mock-exam app — Advanced MLOps &amp; ML at Scale, three full practice exams with AI-reasoned answer keys.</sub></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/jason-miles/dbx-depro-cert"><img src="assets/proj-depro.svg" alt="Databricks Data Engineer Professional exam prep" width="100%" /></a>
      <p><sub>Data Engineer Professional mock-exam app — same companion format, focused on Lakeflow, streaming, Delta, and Unity Catalog.</sub></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/jason-miles/Operationalizing-AI-SAP-Databricks"><img src="assets/proj-sap.svg" alt="Operationalizing AI — SAP x Databricks" width="100%" /></a>
      <p><sub>End-to-end reference pattern for operationalizing AI workloads across SAP business data and the Databricks Data Intelligence Platform.</sub></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/jason-miles/vibe-coding-workshop"><img src="assets/proj-vibe.svg" alt="Vibe Coding Workshop" width="100%" /></a>
      <p><sub>Materials, demos and exercises from the Nov 2025 Vibe Coding workshop on building production AI assistants on Databricks.</sub></p>
    </td>
  </tr>
</table>

<details>
  <summary><b>Architecture at a glance</b> — how the two flagship Databricks Apps are wired</summary>

<br/>

**Sentinel — Fraud & AML**

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#12161C','primaryTextColor':'#EDF0F3','primaryBorderColor':'#FF3621','lineColor':'#FF3621','clusterBkg':'#12161C','fontFamily':'-apple-system, Segoe UI, sans-serif'}}}%%
flowchart LR
  T[Transactions & core banking] --> BZ[Bronze<br/>Delta]
  W[Sanctions & watchlists] --> BZ
  BZ --> SV[Silver<br/>cleansed & joined]
  SV --> GD[Gold<br/>features & risk scores]
  GD --> ML[Model Serving<br/>fraud / AML models]
  ML --> APP[Databricks App<br/>per-bank UI]
  GD --> APP
  UC[(Unity Catalog<br/>governance & lineage)] -.governs.-> BZ
  UC -.-> SV
  UC -.-> GD
```

**Discovery Vitality Pulse**

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#12161C','primaryTextColor':'#EDF0F3','primaryBorderColor':'#FF3621','lineColor':'#FF3621','clusterBkg':'#12161C','fontFamily':'-apple-system, Segoe UI, sans-serif'}}}%%
flowchart LR
  M[Member health, claims & rewards] --> BZ[Bronze] --> SV[Silver] --> GD[Gold<br/>shared-value metrics]
  GD --> DASH[AI/BI dashboards<br/>GM Morning Brief]
  GD --> GEN[Ask Genie<br/>natural-language hub]
  GD --> APP[Databricks App<br/>Health · Rewards · Bridge]
```

</details>

---

## Toolchain

**Platform** &nbsp;—&nbsp; Data Intelligence Platform · Unity Catalog · Delta Lake · Lakehouse Architecture · DBSQL

**Data Engineering** &nbsp;—&nbsp; Lakeflow / Spark Declarative Pipelines · Spark Structured Streaming · Apache Spark / PySpark · Data Warehousing

**AI & ML** &nbsp;—&nbsp; MLflow · Model Serving · Vector Search · Generative AI Engineering · Agent Systems / Agent Bricks · RAG

**Cloud & Languages** &nbsp;—&nbsp; AWS · Azure · GCP · Python · SQL

---

## GitHub stats

<!-- Self-hosted stats — generated nightly by jason-miles/github-stats workflow.
     Light/dark variants via <picture> so they look right in both GitHub themes. -->

<table>
  <tr>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jason-miles/github-stats/generated/overview.svg#gh-dark-mode-only" />
        <img src="https://raw.githubusercontent.com/jason-miles/github-stats/generated/overview.svg" alt="Jason Miles's GitHub Statistics — Stars, Contributions, Lines of code changed, Repos contributed to" />
      </picture>
    </td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jason-miles/github-stats/generated/languages.svg#gh-dark-mode-only" />
        <img src="https://raw.githubusercontent.com/jason-miles/github-stats/generated/languages.svg" alt="Languages Used by File Size" />
      </picture>
    </td>
  </tr>
</table>

---

## Certifications

<p align="center"><strong>Databricks — Professional</strong></p>

<p align="center">
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Databricks Certified Machine Learning Engineer Professional">
    <img height="150" src="assets/databricks-ml-engineer-professional.png" alt="Databricks Certified Machine Learning Engineer Professional" />
  </a>
  &nbsp;&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Databricks Certified Data Engineer Professional">
    <img height="150" src="assets/databricks-data-engineer-professional.png" alt="Databricks Certified Data Engineer Professional" />
  </a>
  &nbsp;&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Academy Accreditation — Building Retrieval Agents on Databricks">
    <img height="150" src="assets/databricks-building-retrieval-agents.png" alt="Academy Accreditation — Building Retrieval Agents on Databricks" />
  </a>
</p>

<p align="center">
  <sub><em>Machine Learning Engineer Professional &nbsp;·&nbsp; Data Engineer Professional &nbsp;·&nbsp; Building Retrieval Agents on Databricks</em></sub>
</p>

<p align="center"><strong>Databricks — Associate &amp; Academy Accreditations</strong></p>

<p align="center">
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Databricks Certified Generative AI Engineer Associate">
    <img height="120" src="assets/databricks-genai-engineer-associate.png" alt="Databricks Certified Generative AI Engineer Associate" />
  </a>
  &nbsp;&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Databricks Certified Data Engineer Associate">
    <img height="120" src="assets/databricks-data-engineer-associate.png" alt="Databricks Certified Data Engineer Associate" />
  </a>
  &nbsp;&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Academy Accreditation — AI Agent Fundamentals on Databricks">
    <img height="120" src="assets/databricks-ai-agent-fundamentals.png" alt="Academy Accreditation — AI Agent Fundamentals on Databricks" />
  </a>
  &nbsp;&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Academy Accreditation — Generative AI Fundamentals">
    <img height="120" src="assets/databricks-genai-fundamentals.png" alt="Academy Accreditation — Generative AI Fundamentals" />
  </a>
  &nbsp;&nbsp;
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet" title="Academy Accreditation — Databricks Lakehouse Fundamentals">
    <img height="120" src="assets/databricks-lakehouse-fundamentals.png" alt="Academy Accreditation — Databricks Lakehouse Fundamentals" />
  </a>
</p>

<p align="center">
  <sub><em>GenAI Engineer Associate &nbsp;·&nbsp; Data Engineer Associate &nbsp;·&nbsp; AI Agent Fundamentals &nbsp;·&nbsp; GenAI Fundamentals &nbsp;·&nbsp; Lakehouse Fundamentals</em></sub>
</p>

<p align="center"><strong>External</strong></p>

<p align="center">
  <a href="https://achieve.snowflake.com/profile/jasonmiles/wallet" title="SnowPro Core Certification">
    <img height="120" src="assets/snowpro-core.png" alt="SnowPro Core Certification" />
  </a>
</p>

<p align="center">
  <sub><em>SnowPro Core Certification</em></sub>
</p>

<p align="center">
  <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet"><b>View full credentials wallet →</b></a>
</p>

---

<p align="center">
  <sub>
    <a href="https://jason-miles.github.io">Homepage</a> &nbsp;·&nbsp;
    <a href="https://www.linkedin.com/in/jasonmiles/">LinkedIn</a> &nbsp;·&nbsp;
    <a href="https://credentials.databricks.com/profile/jasonmiles-bcs/wallet">Databricks credentials</a>
  </sub>
</p>
