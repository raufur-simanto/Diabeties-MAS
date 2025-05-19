import asyncio
from agents.useragent import UserAgent
from agents.datavalidation_agent import DataValidationAgent
from agents.storage_agent import StorageAgent
from agents.alert_agent import AlertAgent
from agents.predictor_agent import PredictorAgent
from agents.detection_agent import DetectionAgent

async def main():
    # Start agents
    alert_agent = AlertAgent("alert@localhost", "alertpwd")
    await alert_agent.start()
    predictor_agent = PredictorAgent("prediction@localhost", "predictionpwd")
    await predictor_agent.start()
    detection_agent = DetectionAgent("detection@localhost", "detectionpwd")
    await detection_agent.start()
    storage_agent = StorageAgent("storage@localhost", "storagepwd")
    await storage_agent.start()
    validation_agent = DataValidationAgent("datavalidation@localhost", "validationpwd")
    await validation_agent.start()

    # Wait to make sure behaviours are ready
    await asyncio.sleep(3)

    # Start user agent
    user_agent = UserAgent("user@localhost", "userpassword")
    await user_agent.start()

    print("[Main] Agents started. Running for 60 seconds...")
    await asyncio.sleep(60)

    await user_agent.stop()
    await validation_agent.stop()
    await storage_agent.stop()
    await predictor_agent.stop()
    await alert_agent.stop()
    await detection_agent.stop()
    print("[Main] All agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())

