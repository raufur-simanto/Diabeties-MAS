
---

```markdown
# 🩺 Diabetes Risk Detection Multi-Agent System

This project is a **Multi-Agent System (MAS)** for early detection of potential diabetes risks using XMPP-based communication between autonomous agents. Built using the **SPADE framework**, the system simulates a cooperative environment where each agent plays a specific role in collecting, validating, storing, analyzing, and alerting based on user health data.

---

## 📌 Features

- Collect user health data interactively
- Validate and sanitize inputs
- Persist validated data for analysis
- Perform rule-based detection
- Predict diabetes risk using a trained ML model (logistic regression)
- Alert users on medium/high risk

---

## 🧠 Architecture Overview

Agents involved:

1. **UserAgent**: Collects data from user.
2. **DataValidationAgent**: Validates data input.
3. **StorageAgent**: Stores and forwards data.
4. **DetectionAgent**: Detects potential risks using heuristics.
5. **PredictorAgent**: Predicts diabetes risk using ML.
6. **AlertAgent**: Notifies users based on prediction results.

📊 Each agent communicates using XMPP (via SPADE framework) and performs an asynchronous, message-driven workflow.

---

## 📁 Project Structure

```

project/
├── agents/
│   ├── useragent.py
│   ├── datavalidation\_agent.py
│   ├── storage\_agent.py
│   ├── detection\_agent.py
│   ├── predictor\_agent.py
│   └── alert\_agent.py
├── model/
│   └── diabetes\_model.pkl
├── data/
│   └── health\_records.csv
├── main.py
├── requirements.txt
└── README.md

````

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10
- SPADE
- scikit-learn
- aioxmpp
- asyncio

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/diabetes-mas.git
   cd diabetes-mas
````

2. Create a virtual environment and activate it:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Train and export the ML model if needed (or use provided `diabetes_model.pkl`).

4. Make sure you have an **XMPP server** (like `ejabberd` or `prosody`) running locally with the following users created:

   * `user@localhost`
   * `datavalidation@localhost`
   * `storage@localhost`
   * `detection@localhost`
   * `prediction@localhost`
   * `alert@localhost`

---

## ▶️ Running the System

Start the system via:

```bash
python main.py
```

This will:

* Start all agents.
* Wait for behavior setup.
* Launch the user interaction for 60 seconds.
* Process and propagate messages among agents.

---

## ⚙️ Customization

* You can customize validation rules and ML model in:

  * `datavalidation_agent.py`
  * `predictor_agent.py`

* Update features and training logic in `model/` directory.

---

## 📌 Example Inputs

```
Enter name: Bob
Enter age: 45
Enter glucose level: 135
Enter BMI: 32.4
Enter insulin level: 88
Enter Blood Pressure: 120
...
```

---

## 📬 Communication Flow

```text
UserAgent
   ↓
DataValidationAgent
   ↓
StorageAgent
   ↓
DetectionAgent
   ↓
PredictorAgent
   ↓
AlertAgent → UserAgent
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Raufur Rahman**
MSc in Artificial Intelligence
University of Jyväskylä

---

## 🤝 Acknowledgements

* [SPADE Framework](https://github.com/javipalanca/spade)
* [Scikit-learn](https://scikit-learn.org/)
* Open-source diabetes datasets

```