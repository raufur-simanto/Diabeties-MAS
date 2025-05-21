# """This script defines a UserAgent that collects user data and sends it to a DataValidationAgent for validation."""

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class UserAgent(Agent):
    class SendDataBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.invalid_attempts = 0
            self.waiting_for_alert = False

        async def run(self):
            if not self.waiting_for_alert:
                print("\n[User] Please enter your health info:-----------------------------------------------------------")
                try:
                    # Collect user data
                    name = input("Name: ")
                    age = int(input("Age: "))
                    sugar = float(input("Blood Sugar Level (mg/dL): "))
                    blood_pressure = float(input("Blood Pressure (mmHg): "))
                    insulin = float(input("Insulin Level (µU/mL): "))
                    bmi = float(input("BMI: "))
                    symptoms = input("Symptoms (comma-separated): ")
                except ValueError:
                    print("[User] Invalid input format. Try again.")
                    return

                data = f"{name},{age},{sugar},{blood_pressure},{insulin},{bmi}, {symptoms}"
                print(f"[User] Sending data: {data}")

                msg = Message(to="datavalidation@localhost")
                msg.body = data
                await self.send(msg)

                reply = await self.receive(timeout=60)
                if reply:
                    if "Invalid" in reply.body:
                        print(f"[User] Received feedback: {reply.body}")
                        self.invalid_attempts += 1
                        if self.invalid_attempts >= 3:
                            print("[User] Too many failed attempts. Stopping.")
                            await self.agent.stop()
                    else:
                        print(f"[User] Validation success: {reply.body}")
                        # Now wait for alert agent message
                        self.waiting_for_alert = True
                else:
                    print("[User] No response from DataValidationAgent. Try again.")
            else:
                # Waiting for alert agent response
                alert_msg = await self.receive(timeout=60) 
                if alert_msg:
                    print(f"[User] Received alert: {alert_msg.body}")
                await self.agent.stop()

    async def setup(self):
        print("[UserAgent] Starting...")
        self.add_behaviour(self.SendDataBehaviour())

