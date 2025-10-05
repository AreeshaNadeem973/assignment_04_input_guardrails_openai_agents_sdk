
# 🛡️ Assignment – Input Guardrails (OpenAI Agents SDK)

This project demonstrates the implementation of **Input Guardrails** using the **OpenAI Agents SDK** in Python.  
It includes **three exercises** showcasing how agents can be controlled and restricted using predefined guardrail rules.

---

## 📝 Overview
The goal of this assignment is to understand how **Input Guardrails** can be applied to manage and restrict agent behavior based on user inputs.  
Guardrails act as safety layers that prevent agents from performing actions outside defined constraints.

---

## 🚀 Exercises Implemented

### **1️⃣ Exercise #1 – Input Guardrail Trigger**
- **Objective:** Create an agent that triggers an `InputGuardRailTripwireTriggered` exception.  
- **Prompt:** `"I want to change my class timings 😭😭"`  
- **Expected Outcome:** The guardrail blocks the request and logs the exception.

---

### **2️⃣ Exercise #2 – Father Agent & Guardrail**
- **Objective:** Implement a **Father Agent** that prevents actions when the temperature is below **26°C**.  
- **Outcome:** The agent restricts execution and logs the stop condition.

---

### **3️⃣ Exercise #3 – Gate Keeper Agent & Guardrail**
- **Objective:** Build a **Gate Keeper Agent** that blocks students from other schools.  
- **Outcome:** Guardrail checks the student's school name and blocks unauthorized access.

---

## 🧠 Objectives
- Understand input guardrails and restriction mechanisms  
- Implement agents with guardrail-based logic  
- Handle exceptions like `InputGuardRailTripwireTriggered` gracefully  
- Monitor logs for guardrail event tracking  

---

## 🛠️ Tech Stack
- **Python 3.10+**  
- **OpenAI Agents SDK**  
- **Asyncio** (for asynchronous agent execution)  
- **Logging** (for monitoring guardrail triggers)

---

## 📊 Results
- Guardrails successfully restricted agent actions based on defined conditions.  
- Each guardrail trigger and exception was logged for verification and debugging.

---

## 📂 Project Status
✅ Completed – All three exercises implemented successfully.
