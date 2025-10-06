import streamlit as st
from datetime import datetime, date
import requests
import json
import os

st.set_page_config(page_title="Smart Daily Planner", page_icon="🗓️")

# 📁 File to store tasks
TASKS_FILE = "tasks.json"

# 💬 Live motivational quote from ZenQuotes
def get_motivational_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            return f"💬 {data[0]['q']} — {data[0]['a']}"
        else:
            return "💬 Stay positive and keep going!"
    except:
        return "💬 You’ve got this!"

st.sidebar.success(get_motivational_quote())

# 🔄 Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 💾 Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, default=str)

# 🧠 Initialize task list
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("🗓️ Smart Daily Planner")

# 📅 Date picker for weekly view
selected_date = st.date_input("Choose a date", value=date.today())

# 🏷️ Task input
task = st.text_input("Enter a task")
time = st.time_input("Choose time", value=datetime.strptime("09:00", "%H:%M").time())
category = st.selectbox("Select category", ["🏠 Home", "💼 Work", "🧘 Self-care", "🎓 Study"])

# ➕ Add task
if st.button("Add Task"):
    if task:
        new_task = {
            "date": str(selected_date),
            "time": str(time),
            "task": task,
            "category": category,
            "done": False
        }
        st.session_state.tasks.append(new_task)
        save_tasks(st.session_state.tasks)
        st.toast(f"✅ Task added: {task} at {time}", icon="🎉")
    else:
        st.toast("⚠️ Please enter a task before adding.", icon="⚠️")

# 📋 Display tasks for selected date
st.subheader(f"📅 Schedule for {selected_date.strftime('%A, %d %B %Y')}")
tasks_today = [t for t in st.session_state.tasks if t["date"] == str(selected_date)]

if tasks_today:
    for i, t in enumerate(sorted(tasks_today, key=lambda x: x["time"])):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            checked = st.checkbox("", value=t["done"], key=f"check_{i}")
        with col2:
            color = "green" if checked else "black"
            task_text = f"🕒 {t['time']} — {t['category']} {t['task']}"
            if checked:
                st.markdown(f"<span style='color:{color}'><s>{task_text}</s> ✅</span>", unsafe_allow_html=True)
                t["done"] = True
            else:
                st.markdown(f"<span style='color:{color}'>{task_text}</span>", unsafe_allow_html=True)
                t["done"] = False
    save_tasks(st.session_state.tasks)
else:
    st.info("No tasks for this date yet.")

# 📤 Export tasks
if st.button("Export Today's Tasks"):
    export_text = f"Tasks for {selected_date.strftime('%A, %d %B %Y')}\n\n"
    for t in tasks_today:
        status = "✅" if t["done"] else "❌"
        export_text += f"{status} {t['time']} — {t['category']} {t['task']}\n"
    with open("daily_tasks.txt", "w", encoding="utf-8") as f:
        f.write(export_text)
    st.toast("📤 Tasks exported to daily_tasks.txt", icon="📁")