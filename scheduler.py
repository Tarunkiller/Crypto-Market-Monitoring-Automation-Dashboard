from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from etl.pipeline import run_coingecko_pipeline, run_binance_pipeline
from automation.alerts import check_alerts
from reports.insight_generator import generate_daily_insight

scheduler = BackgroundScheduler()

def start_scheduler():
    """
    Starts all background automation jobs.
    """
    # 1. ETL Pipelines (Every 15 minutes)
    scheduler.add_job(
        run_coingecko_pipeline,
        trigger=IntervalTrigger(minutes=15),
        id='coingecko_etl',
        name='CoinGecko ETL Pipeline',
        replace_existing=True
    )
    
    # scheduler.add_job(
    #     run_binance_pipeline,
    #     trigger=IntervalTrigger(minutes=5),
    #     id='binance_etl',
    #     name='Binance ETL Pipeline',
    #     replace_existing=True
    # )

    # 2. Alert Checker (Every 5 minutes)
    scheduler.add_job(
        check_alerts,
        trigger=IntervalTrigger(minutes=5),
        id='alert_checker',
        name='Check User Alerts',
        replace_existing=True
    )

    # 3. AI Report Generator (Daily at 08:00 AM)
    scheduler.add_job(
        generate_daily_insight,
        trigger=CronTrigger(hour=8, minute=0),
        id='ai_daily_report',
        name='Generate Daily AI Market Insight',
        replace_existing=True
    )

    scheduler.start()
    logger.info("APScheduler started with background jobs.")

if __name__ == "__main__":
    import time
    start_scheduler()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
