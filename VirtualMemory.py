import streamlit as st
import matplotlib.pyplot as plt

# Page title
st.title("🧠 Virtual Memory Educational Simulator")
st.markdown("Simulate Page Replacement Algorithms: FIFO, LRU, Optimal")

# Input controls
algo = st.selectbox("Choose Page Replacement Algorithm", ["FIFO", "LRU", "Optimal"])
ram_size = st.slider("RAM Size (number of frames)", 1, 10, 3)
input_method = st.radio("How do you want to input memory sequence?", ["Type manually", "Upload .txt file"])

# Get memory reference string
if input_method == "Type manually":
    input_text = st.text_input("Enter memory reference string (e.g., 7 0 1 2 0 3 0 4)")
    references = list(map(int, input_text.strip().split())) if input_text else []
else:
    uploaded_file = st.file_uploader("Upload Memory Reference File", type="txt")
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        references = list(map(int, content.strip().split()))
    else:
        references = []

# Replacement algorithms
def simulate_fifo(pages, frames):
    memory, faults = [], 0
    timeline = []
    for page in pages:
        if page not in memory:
            faults += 1
            if len(memory) >= frames:
                memory.pop(0)
            memory.append(page)
        timeline.append(memory.copy())
    return faults, timeline

def simulate_lru(pages, frames):
    memory, faults, recent = [], 0, {}
    timeline = []
    for i, page in enumerate(pages):
        if page not in memory:
            faults += 1
            if len(memory) >= frames:
                lru_page = min(recent, key=recent.get)
                memory.remove(lru_page)
                del recent[lru_page]
            memory.append(page)
        recent[page] = i
        timeline.append(memory.copy())
    return faults, timeline

def simulate_optimal(pages, frames):
    memory, faults = [], 0
    timeline = []
    for i, page in enumerate(pages):
        if page not in memory:
            faults += 1
            if len(memory) >= frames:
                future = pages[i+1:]
                indices = {p: future.index(p) if p in future else float('inf') for p in memory}
                page_to_remove = max(indices, key=indices.get)
                memory.remove(page_to_remove)
            memory.append(page)
        timeline.append(memory.copy())
    return faults, timeline

# Run Simulation
if st.button("Run Simulation") and references:
    if algo == "FIFO":
        faults, timeline = simulate_fifo(references, ram_size)
    elif algo == "LRU":
        faults, timeline = simulate_lru(references, ram_size)
    else:
        faults, timeline = simulate_optimal(references, ram_size)

    # Results
    st.success(f"Total Page Faults: {faults}")
    
    # Visualization
    st.subheader("Page Table Evolution")
    for i, frame in enumerate(zip(*timeline)):
        st.text(f"Time {i+1}: {frame}")

    fig, ax = plt.subplots()
    ax.plot(range(len(references)), [len(set(t)) for t in timeline], marker='o')
    ax.set_title("Page Set Size Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Pages in Memory")
    st.pyplot(fig)