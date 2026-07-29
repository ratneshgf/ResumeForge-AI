"""
Purges expired upload/temp/output directories. Run periodically —
main.py schedules this on an asyncio background loop for local/single-
instance deployments. For production, prefer a real scheduler (cron,
APScheduler with a persistent jobstore, or a platform cron trigger)
so cleanup survives process restarts.
"""
import asyncio
import logging

from app.core.storage import purge_expired

logger = logging.getLogger("cleanup_job")


async def run_periodic_cleanup(interval_seconds: int = 600):
    while True:
        try:
            removed = purge_expired()
            if removed:
                logger.info("cleanup_job: removed %d expired session dirs", removed)
        except Exception:
            logger.exception("cleanup_job: purge failed")
        await asyncio.sleep(interval_seconds)
