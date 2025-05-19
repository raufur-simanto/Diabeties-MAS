from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class DetectionAgent(Agent):
    class DetectionBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                data = msg.body
                print(f"[DetectionAgent] Analyzing: {data}")

                try:
                    parts = data.split(",")
                    name = parts[0]
                    age = int(parts[1])
                    sugar = float(parts[2])
                    bp = float(parts[3])
                    insulin = float(parts[4])
                    bmi = float(parts[5])
                    
                    symptoms = parts[6:]  # optional symptoms

                    symptom_list = [s.strip().lower() for s in symptoms]
                    risky_symptoms = {"fatigue", "blurred vision", "weight loss", "frequent urination"}

                    # Rule-based detection logic
                    if (
                        sugar > 150 or
                        bmi > 30 or
                        insulin < 10 or
                        bp > 130 or
                        risky_symptoms.intersection(symptom_list)
                    ):
                        print("[DetectionAgent] Possible diabetes risk. Forwarding to PredictionAgent.")
                        forward = Message(to="prediction@localhost")
                        forward.body = data
                        await self.send(forward)
                    else:
                        print("[DetectionAgent] No major risk detected. Sending alert.")
                        notify = Message(to="alert@localhost")
                        notify.body = f"{name}, low"
                        await self.send(notify)

                except Exception as e:
                    print(f"[DetectionAgent] Error parsing data: {e}")

    async def setup(self):
        print("[DetectionAgent] Starting...")
        self.add_behaviour(self.DetectionBehaviour())
