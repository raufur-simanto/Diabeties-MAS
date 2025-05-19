# """Storage Agent for storing data sent by users.
# This agent receives data from the DataValidationAgent and simulates storing it."""

import os
import csv
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class StorageAgent(Agent):
    class StoreBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                msg = await self.receive(timeout=10)
                if msg:
                    print(f"[StorageAgent] Storing data: {msg.body}")
                    data = msg.body.strip().split(",")
                    # Define CSV file path
                    csv_file = "data/health/records.csv"

                    # Check if file exists to decide if header should be written
                    file_exists = os.path.isfile(csv_file)

                    with open(csv_file, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        
                        # Write header if file is new
                        if not file_exists:
                            writer.writerow(["Name", "Age", "Sugar", "BP", "Insulin", "BMI", "Symptoms"])
                        
                        # Write the row of data
                        writer.writerow(data)

                    print("[StorageAgent] Data stored successfully in CSV format.")
                    # with open("storage.txt", "a") as f:
                    #     f.write(msg.body + "\n")
                    # print("[StorageAgent] Data stored successfully.")
                    # Optionally notify the user of success
                    # Notify validator
                    success_msg = Message(to="datavalidation@localhost")
                    success_msg.body = "Success, Your data has been successfully stored."
                    await self.send(success_msg)
                    
                    # After data stored successfully
                    notify_detection = Message(to="detection@localhost")
                    notify_detection.body = msg.body
                    await self.send(notify_detection)
                    print("[StorageAgent] Data forwarded to DetectiontAgent.")


            except Exception as e:
                print(f"[StorageAgent] Error: {e}")
                # Notify the user about the failure
                failure_msg = Message(to="datavalidation@localhost")
                failure_msg.body = "Sorry, there was an error storing your data. Please try again later."
                await self.send(failure_msg)
    async def setup(self):       
        print("[StorageAgent] Starting...")
        self.add_behaviour(self.StoreBehaviour())

