import random
import requests
from datetime import datetime, timedelta
from app.data.postgres_adapter import PostgresAdapter
from app.utils.logger import logger
import boto3
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.postgres")

class OTPService:
    def __init__(self):
        self.adapter = PostgresAdapter()
        self.otp_expiry_minutes = 5
        self.sns_client = boto3.client(
            "sns",
            region_name=os.getenv("AWS_REGION", "ap-south-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    
    def generate_otp(self) -> str:
        return str(random.randint(100000, 999999))
    
    def send_otp(self, mobile: str) -> (bool, str):
        otp = self.generate_otp()
        expires_at = datetime.now() + timedelta(minutes=self.otp_expiry_minutes)
        
        try:
            self.adapter.store_otp(mobile, otp, expires_at)
            
            # Send SMS (implement your SMS provider here)
            success = self._send_sms(mobile, otp)
            
            if success:
                logger.info(f"OTP sent to {mobile}")
                return True, otp
            else:
                logger.error(f"Failed to send OTP to {mobile}")
                return False, ""
                
        except Exception as e:
            logger.error(f"Error sending OTP: {e}")
            return False, ""
    
    def verify_otp(self, mobile: str, otp: str) -> bool:
        return self.adapter.verify_otp(mobile, otp)
    
    def _send_sms(self, mobile: str, otp: str) -> bool:
        """
        Send OTP via AWS SNS.
        """
        try:
            message = f"Your LokSetu Application Login OTP is {otp}. It is valid for {self.otp_expiry_minutes} minutes."
            phone_number = f"+91{mobile}"  # international format

            logger.info(f"Sending OTP to {phone_number} via AWS SNS...")

            response = self.sns_client.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Transactional'}
                }
            )

            message_id = response.get("MessageId")
            if message_id:
                logger.info(f"OTP sent successfully to {phone_number}, MessageId: {message_id}")
                return True
            else:
                logger.error(f"Failed to send OTP via SNS: {response}")
                return False

        except Exception as e:
            logger.error(f"Exception while sending OTP: {e}")
            return False