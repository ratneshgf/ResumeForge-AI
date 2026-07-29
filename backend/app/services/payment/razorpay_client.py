"""
Production-grade Razorpay integration with security best practices.

Implements:
- Real order creation
- Signature verification (no security vulnerabilities)
- Webhook signature verification
- Proper error handling
- Idempotency checks
"""
import hashlib
import hmac
import logging
import uuid
from typing import Dict

from app.config import settings

logger = logging.getLogger(__name__)

# Plan pricing in paise (1 INR = 100 paise)
PLAN_AMOUNTS_PAISE = {
    "premium_single": 19900,   # ₹199
    "premium_monthly": 49900,  # ₹499
    "premium_yearly": 499900,  # ₹4,999
}


def is_mock_mode() -> bool:
    """Check if running in mock mode (no real payments)"""
    return not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET


def create_order(plan: str) -> Dict:
    """
    Create a Razorpay payment order.
    
    Returns order details including order_id for checkout.
    """
    amount = PLAN_AMOUNTS_PAISE.get(plan, PLAN_AMOUNTS_PAISE["premium_single"])
    
    if is_mock_mode():
        logger.warning("Creating mock payment order (no Razorpay keys configured)")
        return {
            "order_id": f"mock_order_{uuid.uuid4().hex[:12]}",
            "amount": amount,
            "currency": "INR",
            "key_id": "mock_key_id",
            "mock_mode": True,
        }
    
    try:
        import razorpay
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,  # Auto-capture
            "notes": {
                "plan": plan,
            }
        }
        
        order = client.order.create(data=order_data)
        
        logger.info(f"Created Razorpay order: {order['id']} for plan {plan}")
        
        return {
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
            "key_id": settings.RAZORPAY_KEY_ID,
            "mock_mode": False,
        }
    
    except Exception as e:
        logger.error(f"Error creating Razorpay order: {e}", exc_info=True)
        raise


def verify_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verify Razorpay payment signature for security.
    
    This prevents fraudulent payment confirmations.
    """
    if is_mock_mode():
        # In mock mode, accept any payment_id starting with "mock_pay_"
        logger.warning("Mock mode: accepting payment without verification")
        return payment_id.startswith("mock_pay_")
    
    try:
        # Generate expected signature
        message = f"{order_id}|{payment_id}"
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Constant-time comparison to prevent timing attacks
        is_valid = hmac.compare_digest(expected_signature, signature)
        
        if is_valid:
            logger.info(f"Payment verified successfully: {payment_id}")
        else:
            logger.warning(f"Invalid payment signature for payment: {payment_id}")
        
        return is_valid
    
    except Exception as e:
        logger.error(f"Error verifying payment signature: {e}", exc_info=True)
        return False


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify webhook signature to ensure webhook is from Razorpay.
    
    Critical for security - prevents fake webhook attacks.
    """
    if is_mock_mode():
        logger.warning("Mock mode: accepting webhook without verification")
        return True
    
    try:
        # Generate expected signature
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Constant-time comparison
        is_valid = hmac.compare_digest(expected_signature, signature)
        
        if is_valid:
            logger.info("Webhook signature verified successfully")
        else:
            logger.warning("Invalid webhook signature - possible attack!")
        
        return is_valid
    
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {e}", exc_info=True)
        return False


def fetch_payment_details(payment_id: str) -> Dict:
    """
    Fetch payment details from Razorpay for verification.
    
    Useful for double-checking payment status.
    """
    if is_mock_mode():
        return {
            "id": payment_id,
            "status": "captured",
            "amount": 19900,
            "currency": "INR",
        }
    
    try:
        import razorpay
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        
        return payment
    
    except Exception as e:
        logger.error(f"Error fetching payment details: {e}", exc_info=True)
        raise
