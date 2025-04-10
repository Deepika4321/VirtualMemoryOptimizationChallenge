import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Virtual Memory Manager", layout="centered")

class MemoryManager:
    def __init__(self, frames):
        self.frames = frames
        self.reset()

    def reset(self):
        self.memory = []
        self.page_faults = 0
        self.history = []

    def simulate_lru(self, pages):
        self.reset()
        recent = []
        for i, page in enumerate(pages):
            if page in self.memory:
                recent.remove(page)
                recent.append(page)
                self.history.append((i + 1, page, list(self.memory), "Hit", self.page_faults))
            else:
                self.page_faults += 1
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                else:
                    lru = recent.pop(0)
                    self.memory.remove(lru)
                    self.memory.append(page)
                recent.append(page)
                self.history.append((i + 1, page, list(self.memory), "Miss", self.page_faults))
        return self.page_faults, self.history

    def simulate_optimal(self, pages):
        self.reset()
        for i in range(len(pages)):
            page = pages[i]
            if page in self.memory:
                self.history.append((i + 1, page, list(self.memory), "Hit", self.page_faults))
                continue
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory.append(page)
            else:
                future = pages[i+1:]
                idx = []
                for mem_page in self.memory:
                    if mem_page in future:
                        idx.append(future.index(mem_page))
                    else:
                        idx.append(float('inf'))
                self.memory[idx.index(max(idx))] = page
            self.history.append((i + 1, page, list(self.memory), "Miss", self.page_faults))
        return self.page_faults, self.history

    def simulate_fifo(self, pages):
        self.reset()
        queue = []
        for i, page in enumerate(pages):
            if page in self.memory:
                self.history.append((i + 1, page, list(self.memory), "Hit", self.page_faults))
            else:
                self.page_faults += 1
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                    queue.append(page)
                else:
                    out = queue.pop(0)
                    self.memory.remove(out)
                    self.memory.append(page)
                    queue.append(page)
                self.history.append((i + 1, page, list(self.memory), "Miss", self.page_faults))
        return self.page_faults, self.history


# Streamlit UI
st.title("📊 Virtual Memory Management Tool")
st.markdown("Simulate **Paging**, **Page Faults**, and Replacement Algorithms: **LRU**, **FIFO**, **Optimal**")

frames = st.number_input("🔢 Number of Memory Frames:", min_value=1, max_value=20, value=3)
page_input = st.text_input("📥 Page Reference String (space-separated):", "7 0 1 2 0 3 0 4 2 3 0 3 2")
algo = st.selectbox("🧠 Choose Replacement Algorithm:", ["LRU", "FIFO", "Optimal"])
simulate_btn = st.button("🚀 Run Simulation")

if simulate_btn:
    try:
        pages = list(map(int, page_input.strip().split()))
        manager = MemoryManager(frames)

        if algo == "LRU":
            faults, history = manager.simulate_lru(pages)
        elif algo == "FIFO":
            faults, history = manager.simulate_fifo(pages)
        else:
            faults, history = manager.simulate_optimal(pages)

        st.success(f"✅ Total Page Faults using {algo}: **{faults}**")
        st.write("---")
        st.subheader("📋 Simulation Steps")

        # Show table
        table_data = {
            "Step": [step for step, _, _, _, _ in history],
            "Page": [page for _, page, _, _, _ in history],
            "Memory State": [mem for _, _, mem, _, _ in history],
            "Status": [status for _, _, _, status, _ in history],
            "Cumulative Faults": [fault for _, _, _, _, fault in history],
        }
        st.dataframe(table_data, use_container_width=True)

        # Plot graph
        st.subheader("📈 Page Fault Trend")
        plt.figure(figsize=(10, 4))
        steps = [step for step, _, _, _, _ in history]
        faults_over_time = [fault for _, _, _, _, fault in history]
        plt.plot(steps, faults_over_time, marker='o', color='royalblue', linewidth=2)
        plt.xlabel("Step")
        plt.ylabel("Cumulative Page Faults")
        plt.title(f"Page Faults Over Time ({algo})")
        plt.grid(True)
        st.pyplot(plt)

    except Exception as e:
        st.error(f"❌ Error: {e}")
