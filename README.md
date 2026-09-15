<!-- ===== HEADER ===== -->
<div align="center">

<a href="https://nullcadre.com">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=30&duration=3000&pause=900&color=00E5FF&center=true&vCenter=true&width=800&lines=Hi%2C+I'm+Robert+Huzo+%F0%9F%91%8B;Founder+%26+Pen+Tester+%40+HuzoSecurity+Ltd;Building+NullCadre+%F0%9F%9B%B0%EF%B8%8F;AI-assisted+offensive+security;Proven%2C+gated%2C+local-only" alt="Typing SVG" />
</a>

<p>
<em>Founder and penetration tester &nbsp;•&nbsp; AI-assisted offensive security &nbsp;•&nbsp; Manchester, UK 🔐</em>
</p>

<!-- ===== SOCIAL BADGES ===== -->
<a href="https://nullcadre.com">
<img src="https://img.shields.io/badge/NullCadre-nullcadre.com-00E5FF?style=for-the-badge&logo=target&logoColor=white" alt="NullCadre" />
</a>
<a href="https://huzosecurity.com">
<img src="https://img.shields.io/badge/Website-huzosecurity.com-0D1117?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website" />
</a>
<a href="https://www.linkedin.com/in/robert-huzo">
<img src="https://img.shields.io/badge/LinkedIn-Robert%20Huzo-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
<a href="mailto:robert@huzosecurity.com">
<img src="https://img.shields.io/badge/Email-robert@huzosecurity.com-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
</a>
<br/>
<img src="https://komarev.com/ghpvc/?username=huzorobi&style=for-the-badge&color=00E5FF&label=Profile+Views" alt="Profile views" />

</div>

---

## 🧠 About Me

```yaml
name: Robert Huzo
role: Founder and lead penetration tester, HuzoSecurity Ltd
building: NullCadre, an AI-assisted penetration testing and bug-hunting platform
also: HuzoHunter AI, a local-first defensive threat-hunting platform
principle: The engine proves the facts. The AI reasons about them. The model never decides whether a bug exists.
focus: Web and API testing · Authorisation (BOLA/IDOR/BFLA) · LLM application security · Security automation
certs: CompTIA Security+ · CompTIA A+ · EC-Council CEH (5-day hands-on training)
bounty: HackerOne · Bugcrowd · Intigriti · YesWeHack
```

- 🛰️ &nbsp;Building and running **[NullCadre](https://nullcadre.com)**, used daily on authorised engagements and bug bounty targets
- 🛡️ &nbsp;Building **[HuzoHunter AI](https://github.com/huzorobi/HuzoHunter-AI)**, the defensive counterpart, for organisations that can't ship telemetry to a cloud vendor
- 📄 &nbsp;Read a **[full worked assessment](https://huzosecurity.com/sample)** with the evidence behind every finding
- 🎓 &nbsp;BSc Cyber Security, Solent University (in progress) · NVIDIA Inception member
- 💬 &nbsp;Ask me about **authorisation testing, LLM attack surfaces, and running AI models locally**
- 📫 &nbsp;Reach me at **robert@huzosecurity.com** or via [huzosecurity.com](https://huzosecurity.com)

---

## 🚀 Featured Project

<div align="center">

### 🛰️ NullCadre
**AI-assisted penetration testing and bug-hunting platform**

Live, and exercised daily against authorised targets and known-answer benchmarks.

`Deterministic-first` · `Fail-closed scope gate` · `Local AI only` · `Under 5% false positives`

</div>

**How it works**

- A deterministic battery runs first, every applicable detector, exhaustively. Each finding carries structured evidence and a grade.
- An autonomous **Hunter** (a local LLM) then takes those findings as its starting knowledge and builds a real attack chain: observation, hypothesis, probe, pivot, evidence. It can only add to the baseline, never reduce it, and CI tests assert that on every build.
- Every action, from recon to confirmation, passes a fail-closed scope gate enforced in code (`scope.gate.validate()`) before a packet leaves. No prompt-based trust, no bypass, no trusted mode.
- Criticals are confirmed out of band with a working proof of concept. Anything that could not run is reported as **NOT TESTED**, with the reason, never as a clean result.

**Numbers**

- **Under 5% false-positive rate**, measured across several public vulnerable applications, a published authorisation-testing benchmark, and a fully patched self-hosted target where the correct answer is nothing found
- **432** integrated scanner and tool modules · **27** Hunter action modules · **8** report formats (HTML, PDF, Markdown, CSV, JSON, SARIF, OCSF, executive one-pager)
- Runs entirely on the operator's estate. No target data leaves the machine, including for report narration.

**What it covers**

Recon and attack surface mapping · injection classes confirmed out of band (SSRF, SSTI, XXE, SQLi, command injection, request smuggling, cache poisoning) · a two- and three-account **BOLA/IDOR/BFLA** engine with a third-account control to kill the classic false positives · JWT, SAML, OAuth and session attacks · secrets and exposure · cloud and container posture · Active Directory attack paths · WordPress and Drupal read-only assessment · **LLM application security** (prompt injection, sandbox escape, authorisation boundaries, exposed AI endpoints and MCP servers)

> ### *Nothing runs out of scope.*

**Principles**

Report impact, not observations. Absence of evidence is not evidence of absence. Never say "fixed"; the strongest honest claim is "not rediscovered". Confirm, don't weaponise: no persistence, no credential dumping, nothing destructive.

🔒 The core repository is **private** and proprietary to HuzoSecurity Ltd. The platform runs behind a HuzoSecurity engagement; it is not sold or licensed.

---

## 🛡️ Also Building

<div align="center">

### 🤖 HuzoHunter AI
**Local-first threat hunting and security automation**

The defensive counterpart to NullCadre. Explainable investigations, with sensitive data staying fully under your control.

`Local AI` · `Threat Hunting Automation` · `Explainable Investigations` · `M365 + Active Directory Integration`

<a href="https://github.com/huzorobi/HuzoHunter-AI">
<img src="https://github-readme-stats.vercel.app/api/pin/?username=huzorobi&repo=HuzoHunter-AI&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=00E5FF&icon_color=00E5FF" alt="HuzoHunter AI" />
</a>

</div>

---

## 🛠️ Tech & Tools

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kali Linux](https://img.shields.io/badge/Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![Burp Suite](https://img.shields.io/badge/Burp%20Suite%20Pro-FF6633?style=for-the-badge&logo=portswigger&logoColor=white)
![OWASP ZAP](https://img.shields.io/badge/OWASP%20ZAP-00549E?style=for-the-badge&logo=owasp&logoColor=white)
![Nuclei](https://img.shields.io/badge/Nuclei-0E0E0E?style=for-the-badge&logoColor=white)
![BloodHound](https://img.shields.io/badge/BloodHound-D32F2F?style=for-the-badge&logoColor=white)

![Local LLMs](https://img.shields.io/badge/Local%20LLMs-FF6F00?style=for-the-badge&logo=ollama&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA%20GPU-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Wazuh](https://img.shields.io/badge/Wazuh-3578E5?style=for-the-badge&logo=wazuh&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-D32F2F?style=for-the-badge&logo=mitre&logoColor=white)

</div>

---

## 📊 GitHub Stats

<div align="center">

<img height="170" src="https://github-readme-stats.vercel.app/api?username=huzorobi&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=00E5FF&icon_color=00E5FF&count_private=true" alt="GitHub Stats" />
<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=huzorobi&layout=compact&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=00E5FF" alt="Top Languages" />

<br/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=huzorobi&theme=tokyonight&hide_border=true&background=0D1117&ring=00E5FF&fire=00E5FF&currStreakLabel=00E5FF" alt="GitHub Streak" />

<br/>

<img src="https://github-profile-trophy.vercel.app/?username=huzorobi&theme=tokyonight&no-frame=true&column=7&margin-w=10" alt="Trophies" />

</div>

---

<div align="center">

### 🤝 Let's connect

[![NullCadre](https://img.shields.io/badge/-nullcadre.com-00E5FF?style=flat-square&logo=target&logoColor=white)](https://nullcadre.com)
[![Website](https://img.shields.io/badge/-huzosecurity.com-0D1117?style=flat-square&logo=google-chrome&logoColor=white)](https://huzosecurity.com)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/robert-huzo)
[![Email](https://img.shields.io/badge/-Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:robert@huzosecurity.com)

<em>Authorised testing only. Testing without written permission is an offence under the Computer Misuse Act 1990.</em>

</div>

---

<div align="center">
<sub><strong>Last updated 2026-09-15</strong> · Building <a href="https://nullcadre.com">NullCadre</a> 🛰️ &amp; <a href="https://github.com/huzorobi/HuzoHunter-AI">HuzoHunter AI</a> 🔐</sub>
</div>
