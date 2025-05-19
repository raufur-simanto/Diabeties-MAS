import joblib
import os
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class PredictorAgent(Agent):
    class PredictBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.model = None

        async def on_start(self):
            print("[PredictorAgent] Loading ML model...")
            model_path = "models/diabetes_model.pkl"
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print("[PredictorAgent] Model loaded successfully.")
            else:
                print("[PredictorAgent] Model file not found.")
                await self.agent.stop()

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[PredictorAgent] Received: {msg.body}")
                try:
                    name, age, sugar, bp, insulin, bmi, *symptoms = msg.body.split(",")
                    X = [[float(age), float(sugar), float(bp), float(insulin), float(bmi)]]
                    print(f"[PredictorAgent] Features: {X}")

                    prediction = self.model.predict(X)[0]
                    risk = "High" if prediction >= .50 else "Low"

                    print(f"[PredictorAgent] ML Predicted: {risk} risk")

                    # Send to AlertAgent
                    alert_msg = Message(to="alert@localhost")
                    alert_msg.body = f"{name},{risk}"
                    await self.send(alert_msg)

                except Exception as e:
                    print(f"[PredictorAgent] Prediction error: {e}")

    async def setup(self):
        print("[PredictorAgent] Starting...")
        self.add_behaviour(self.PredictBehaviour())

