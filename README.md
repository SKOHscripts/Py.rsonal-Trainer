# 🏃‍♂️🐍 Py.rsonal-Trainer 
![release](https://img.shields.io/github/v/release/SKOHscripts/Py.rsonal-Trainer?include_prereleases&label=latest%20tag)
![issues open](https://img.shields.io/github/issues/SKOHscripts/Py.rsonal-Trainer)
![milestones open](https://img.shields.io/github/milestones/open/SKOHscripts/Py.rsonal-Trainer)<!-- Milestones -->
![milestones closed](https://img.shields.io/github/milestones/closed/SKOHscripts/Py.rsonal-Trainer)

<a href="https://html-preview.github.io/?url=https://github.com/SKOHscripts/Py.rsonal-Trainer/blob/main/donate/redirect.html" target="_blank"><img src="http://KristinitaTest.github.io/donate/Bitcoin-Donate-button.png"></a>

**Py.rsonal-Trainer** (*Python Personal Trainer*) is a modular Python application to **track, analyze and optimize endurance training** — running, trail, cycling, or ultra-distance — with integrated **load analysis**, **nutrition guidance**, and **performance testing tools**.

> ⚠️ This project is currently **under active development**.  
> Release planning and delivery dates are tracked via [GitHub Milestones](https://github.com/SKOHscripts/Py.rsonal-Trainer/milestones).

<p align="center">
  <!-- Temporary placeholder logo (not created yet) -->
  <img
    src="https://img.shields.io/badge/Logo-pending-lightgrey?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjNjY2IiB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDI0MCAyNDAiIHJvbGU9ImltZyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMjQwIiBoZWlnaHQ9IjI0MCIgcng9IjIwIiByeT0iMjAiIGZpbGw9IiNlZWVlZWUiIHN0cm9rZT0iI2NjYyIgc3Ryb2tlLXdpZHRoPSI0Ii8+PHBhdGggZD0iTTUwIDE1MGMxNS0zMCA0MC00MCA2MC0yMCAxMC0xNSAyNS0yMCA0MC0xMCIgc3Ryb2tlPSIjOTk5IiBzdHJva2Utd2lkdGg9IjgiIGZpbGw9Im5vbmUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjxjaXJjbGUgY3g9IjkwIiBjeT0iMTAwIiByPSIxMiIgZmlsbD0iI2ZmZiIgc3Ryb2tlPSIjOTk5IiBzdHJva2Utd2lkdGg9IjQiLz48dGV4dCB4PSI3MCUiIHk9IjkwJSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM3Nzc3NzciIGZvbnQtc2l6ZT0iMTJweCIgZm9udC1mYW1pbHk9IkFyaWFsLCBTZWdvZSBVSSwgU3lzdGVtVUIiPkxPR08gUEVORElORzwvdGV4dD48L3N2Zz4="
    alt="Py.rsonal-Trainer logo placeholder - not created yet"
    width="240"
    height="240"
  />
</p>

<p align="center">
  <em>Official logo not created yet — placeholder shown above.</em><br/>
  <a href="#contributing">Contributions welcome</a>: propose a logo concept via an Issue or PR.
</p>

<!-- Optional compact badges row -->
<p align="center">
  <img alt="logo status" src="https://img.shields.io/badge/logo-status_pending-lightgrey">
  <img alt="status" src="https://img.shields.io/badge/status-in_construction-orange">
</p>

---

## 📌 Overview

Py.rsonal-Trainer is designed for athletes and coaches who want to go **beyond basic GPS stats**, implementing **scientifically grounded metrics** like:
- Acute & Chronic Training Loads (ATL / CTL)
- Weekly ramp rate and ACWR (Acute:Chronic Workload Ratio)
- Training Stress Balance (TSB)
- Nutrition guidance and gap analysis
- Integration of sports test results (VMA, FTP, LTHR) for training zones

It uses a **JSON database** as the central data store, with:
- Modular architecture (`models`, `data`, `analytics`, `nutrition`, `cli`, `ui`)
- Flexible import/export
- CLI-based and future GUI-based interaction

---

## 🛠 Current Status

**Stage:** 🚧 **In Construction**  
I am currently at **First Release (Alpha)** — building the **core data handling and basic load metrics**.  
Full roadmap is defined with **versioned milestones**: from Alpha → v1.0 (UI release) ([GitHub Milestones](https://github.com/SKOHscripts/Py.rsonal-Trainer/milestones)).

---

## 📂 Repository Structure

*Todo*

---

## 🚀 Installation
```bash
git clone https://github.com/SKOHscripts/Py.rsonal-Trainer.git
cd Py.rsonal-Trainer
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

---

## ✨ Features

### ✅ Available


### 🚧 In development
- [ ] YAML schema for athlete & activities
- [ ] Data loading/saving with validation
- [ ] Daily load calculation (sRPE)
- [ ] Weekly summaries
- [ ] ATL/CTL (Rolling Average 7/28 days)
- [ ] ACWR (RA + EWMA)
- [ ] Training Stress Balance (TSB)
- [ ] CLI "summary" and "forecast"
- [ ] Nutrition events schema + CRUD
- [ ] Import test results (VMA, FTP, LTHR)
- [ ] Training zones derivation

### 📅 Planned (See [GitHub Milestones](https://github.com/SKOHscripts/Py.rsonal-Trainer/milestones))
- [ ] Banister impulse–response model
- [ ] Multi-metric load plugins (TRIMP, distance, elevation)
- [ ] Data anomaly detection & alerts
- [ ] Intelligent CLI Q&A
- [ ] Complete GUI/TUI (v1.0)

---

## 📋 TODO & Roadmap

All feature delivery and timing are tracked in [GitHub Milestones](https://github.com/SKOHscripts/Py.rsonal-Trainer/milestones):  
- **0.1.0 First Release (Alpha)** → Data foundations, minimal CLI, basic loads.
- **0.2.0** → ATL/CTL (RA), ACWR v1.
- **0.3.0** → EWMA models, TSB.
- **0.4.0** → CLI essentials, reporting & what-if.
- **0.5.0** → Nutrition schema, basic guidance, gap reports.
- **0.6.0** → Test ingestion, zones, intensity-weighted load.
- **0.7.0** → Data QA, anomaly detection, performance benchmarks.
- **0.8.0** → Intelligent CLI queries & alerts.
- **0.9.0** → Banister model & alternative load metrics.
- **v1.0.0** → **Full release** with UI.

---

## 🔍 Example Usage

*Todo*

---

## 📜 Scientific References

This project’s metrics are based on:
- **sRPE Load**: Foster et al., "Monitoring Training in Athletes"
- **ATL/CTL/TSB**: Performance Manager Model
- **ACWR**: Hulin et al., "The Acute:Chronic Workload Ratio"
- **Banister Model**: Impulse–Response performance modeling
- **Nutrition Guidance**: Consensus recommendations for endurance sports fueling & hydration

- More references will be listed here while developing. References will also be provided in the relevant modules. 

---

## 🤝 Contributing

We welcome contributions:
1. Check open issues & milestones.
2. Fork and create feature branches.
3. Add unit tests for new code.
4. Submit a Pull Request with a clear description.

---

## 🗺 License

This project is released under the ![license](https://img.shields.io/github/license/SKOHscripts/Py.rsonal-Trainer).

