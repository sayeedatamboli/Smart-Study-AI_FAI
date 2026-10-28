import streamlit as st

st.set_page_config(page_title="SmartStudy AI", page_icon="📚", layout="wide")

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"subject": "Mathematics", "topic": "Revise vectors", "difficulty": "Hard", "urgency": "Tomorrow", "minutes": 45, "done": False},
        {"subject": "Foundation of AI", "topic": "Search techniques", "difficulty": "Medium", "urgency": "This week", "minutes": 30, "done": False},
        {"subject": "Python", "topic": "Functions and lists", "difficulty": "Easy", "urgency": "Later", "minutes": 25, "done": True},
    ]

def priority_score(task):
    """Transparent rule-based priority; not a trained machine-learning model."""
    difficulty_points = {"Easy": 1, "Medium": 2, "Hard": 3}
    urgency_points = {"Tomorrow": 3, "This week": 2, "Later": 1}
    return difficulty_points[task["difficulty"]] + urgency_points[task["urgency"]]

st.markdown("""
<style>
.stApp {background:#f6f8fc}
.block-container {padding-top:1.7rem;max-width:1200px}
.hero {background:linear-gradient(120deg,#243b80,#667eea);padding:25px 30px;border-radius:18px;color:white;margin-bottom:20px}
.hero h1 {color:white;margin:0}
.hero p {color:#edf0ff;margin:8px 0 0;font-size:1.05rem}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>📚 SmartStudy AI</h1>
<p>Your intelligent study planner — organise subjects, prioritise tasks, and track progress.</p>
</div>
""", unsafe_allow_html=True)

tasks = st.session_state.tasks
total = len(tasks)
completed = sum(t["done"] for t in tasks)
pending = total - completed
progress = int(completed / total * 100) if total else 0
remaining_minutes = sum(t["minutes"] for t in tasks if not t["done"])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total study tasks", total)
m2.metric("Completed", completed)
m3.metric("Pending", pending)
m4.metric("Progress", f"{progress}%")

left, right = st.columns([1, 1.5], gap="large")
with left:
    st.subheader("➕ Add a study task")
    with st.form("add_task", clear_on_submit=True):
        subject = st.text_input("Subject", placeholder="e.g. Mathematics")
        topic = st.text_input("Topic to study", placeholder="e.g. Matrices")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        urgency = st.selectbox("When is it needed?", ["Tomorrow", "This week", "Later"])
        minutes = st.slider("Study duration (minutes)", 10, 120, 30, step=5)
        submitted = st.form_submit_button("Add task", use_container_width=True)
        if submitted:
            if subject.strip() and topic.strip():
                st.session_state.tasks.append({
                    "subject": subject.strip(), "topic": topic.strip(),
                    "difficulty": difficulty, "urgency": urgency,
                    "minutes": minutes, "done": False
                })
                st.success("Task added!")
                st.rerun()
            else:
                st.warning("Please enter both a subject and a topic.")

with right:
    st.subheader("🤖 Smart priority planner")
    st.caption("Rule-based suggestions: harder and more urgent tasks are placed first.")
    pending_tasks = sorted(
        [t for t in st.session_state.tasks if not t["done"]],
        key=priority_score, reverse=True
    )
    if pending_tasks:
        for i, task in enumerate(pending_tasks, 1):
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                c1.markdown(f"**{i}. {task['subject']} — {task['topic']}**")
                c1.caption(f"{task['difficulty']} difficulty · Due: {task['urgency']} · {task['minutes']} min")
                c2.markdown(f"**Priority {priority_score(task)}/6**")
    else:
        st.success("All tasks are complete. Great work!")

st.divider()
st.subheader("📝 My study tasks")
if st.session_state.tasks:
    for idx, task in enumerate(st.session_state.tasks):
        c1, c2, c3 = st.columns([4, 1, 1])
        c1.markdown(f"**{task['subject']}** — {task['topic']}  \n{task['minutes']} minutes · {task['difficulty']} · {task['urgency']}")
        done = c2.checkbox("Completed", value=task["done"], key=f"done_{idx}")
        if done != task["done"]:
            st.session_state.tasks[idx]["done"] = done
            st.rerun()
        if c3.button("Delete", key=f"delete_{idx}"):
            st.session_state.tasks.pop(idx)
            st.rerun()
        st.markdown("---")
else:
    st.info("No tasks yet. Add your first study task above.")

st.subheader("📈 Study progress")
p1, p2 = st.columns([1, 2])
with p1:
    st.progress(progress / 100 if total else 0)
    st.markdown(f"**{progress}% complete**")
    st.caption(f"About {remaining_minutes} minutes remain in pending tasks.")
with p2:
    st.bar_chart({"Tasks": {"Completed": completed, "Pending": pending}})

st.caption("Project note: This prototype uses transparent, rule-based prioritisation based on task difficulty and urgency. It does not use a trained machine-learning model or live student data.")
