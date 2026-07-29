import logging
from fastapi import APIRouter, Depends, Request, HTTPException

from app.core import session_store
from app.core.rate_limit import rate_limit
from app.schemas.payment import (
    CreateOrderRequest, CreateOrderResponse, VerifyPaymentRequest, VerifyPaymentResponse,
)
from app.services.payment import razorpay_client

router = APIRouter(prefix="/api/v1/payment", tags=["payment"])
logger = logging.getLogger(__name__)


@router.post("/create-order", response_model=CreateOrderResponse, dependencies=[Depends(rate_limit)])
async def create_order(payload: CreateOrderRequest):
    """Create a Razorpay payment order"""
    try:
        order = razorpay_client.create_order(payload.plan)
        session_store.set_value(payload.session_id, "pending_order_id", order["order_id"])
        session_store.set_value(payload.session_id, "plan", payload.plan)
        
        logger.info(f"Order created for session {payload.session_id}: {order['order_id']}")
        
        return CreateOrderResponse(**order)
    
    except Exception as e:
        logger.error(f"Error creating order: {e}", exc_info=True)
        raise HTTPException(500, f"Error creating payment order: {str(e)}")


@router.post("/verify", response_model=VerifyPaymentResponse, dependencies=[Depends(rate_limit)])
async def verify_payment(payload: VerifyPaymentRequest):
    """Verify payment signature and activate premium features"""
    try:
        verified = razorpay_client.verify_signature(
            payload.razorpay_order_id,
            payload.razorpay_payment_id,
            payload.razorpay_signature
        )
        
        if verified:
            # Idempotency: use payment_id as key to prevent double-activation
            already_activated = session_store.get_value(
                payload.session_id,
                "activated_payment_id"
            )
            
            if already_activated != payload.razorpay_payment_id:
                # Activate premium features
                session_store.set_value(payload.session_id, "premium", True)
                session_store.set_value(
                    payload.session_id,
                    "activated_payment_id",
                    payload.razorpay_payment_id
                )
                
                logger.info(
                    f"Premium activated for session {payload.session_id} "
                    f"(payment: {payload.razorpay_payment_id})"
                )
            else:
                logger.info(f"Payment {payload.razorpay_payment_id} already processed")
        else:
            logger.warning(
                f"Payment verification failed for session {payload.session_id}"
            )
        
        return VerifyPaymentResponse(
            verified=verified,
            premium_unlocked=verified
        )
    
    except Exception as e:
        logger.error(f"Error verifying payment: {e}", exc_info=True)
        raise HTTPException(500, f"Error verifying payment: {str(e)}")


@router.post("/webhook")
async def razorpay_webhook(request: Request):
    """
    Handle Razorpay webhooks for payment confirmation.
    
    Provides a second, independent confirmation path in case the
    client-side verification callback fails.
    
    SECURITY: Verifies X-Razorpay-Signature header to prevent fake webhooks.
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        
        # Get signature from header
        signature = request.headers.get("X-Razorpay-Signature", "")
        
        # Verify webhook signature
        if not razorpay_client.verify_webhook_signature(body, signature):
            logger.warning("Webhook signature verification failed - possible attack!")
            raise HTTPException(401, "Invalid webhook signature")
        
        # Parse payload
        payload = await request.json()
        event = payload.get("event", "")
        
        logger.info(f"Received webhook event: {event}")
        
        # Handle payment.captured event
        if event == "payment.captured":
            payment = payload.get("payload", {}).get("payment", {}).get("entity", {})
            payment_id = payment.get("id")
            order_id = payment.get("order_id")
            
            if payment_id and order_id:
                # Find session with this order_id
                # Note: In production, use a database to map orders to sessions
                logger.info(f"Payment captured: {payment_id} for order {order_id}")
                
                # TODO: Activate premium for the session that created this order
                # This requires a proper database to map order_id -> session_id
        
        return {"status": "received", "event": event}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}", exc_info=True)
        # Return 200 to Razorpay so they don't retry
        return {"status": "error", "message": str(e)}
