from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class AlertAgent(Agent):
    class AlertBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                # print(f"[AlertAgent] Received prediction: {msg.body}")
                name, risk = msg.body.split(",")

                # Autonomous decision
                if risk == "High":
                    print(f"[AlertAgent] High risk detected. Alerting user.")
                    alert_msg = Message(to="user@localhost")
                    alert_msg.body = f"Hi {name}, based on your data, you may be at high risk for diabetes. Please consult a doctor."
                    await self.send(alert_msg)
                else:
                    print(f"[AlertAgent] Risk is low. No alert sent.")
                    

    async def setup(self):
        print("[AlertAgent] Starting...")
        self.add_behaviour(self.AlertBehaviour())
