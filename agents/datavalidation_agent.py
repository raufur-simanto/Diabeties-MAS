# This agent validates data received from the user and forwards it to the storage agent if valid.
# """DataValidationAgent for validating user data.

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class DataValidationAgent(Agent):
    class ValidateBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg:
                data = msg.body
                print(f"[Validator] Received: {data}")
                parts = data.split(",")

                if len(parts) < 5:
                    feedback = Message(to=str(msg.sender))
                    feedback.body = "Invalid data. Incomplete input."
                    await self.send(feedback)
                    return

                name, age, sugar, blood_pressure, insulin, bmi, *symptoms = parts
                try:
                    age = int(age)
                    sugar = float(sugar)
                    blood_pressure = float(blood_pressure)
                    insulin = float(insulin)
                    bmi = float(bmi)
                except ValueError:
                    feedback = Message(to=str(msg.sender))
                    feedback.body = "Invalid data types."
                    await self.send(feedback)
                    return

                if not (0 < int(age) < 120 and
                    70 <= float(sugar) <= 200 and
                    10 <= float(bmi) <= 50 and
                    0 <= float(insulin) <= 300 and
                    40 <= float(blood_pressure) <= 200):

                    feedback = Message(to=str(msg.sender))
                    feedback.body = "Invalid data. Check age/sugar/blood pressure/insulin/bmi ranges."
                    await self.send(feedback)
                else:
                    print("[Validator] Valid data. Forwarding to Storage Agent.")
                    forward = Message(to="storage@localhost")
                    forward.body = data
                    await self.send(forward)

                    confirm = Message(to=str(msg.sender))
                    confirm.body = "Data validated and sent to storage."
                    await self.send(confirm)

                    reply = await self.receive(timeout=15)
                    if reply:
                        print(f"[Validator] Storage reply: {reply.body}")
                    else:
                        print("[Validator] No response from Storage Agent.")

    async def setup(self):
        print("[DataValidationAgent] Starting...")
        self.add_behaviour(self.ValidateBehaviour())
