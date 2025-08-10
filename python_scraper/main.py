import asyncio
import logging
import os
from dotenv import load_dotenv

from scraper.facebook_scraper import FacebookScraper
from nlp.nlp_pipeline import NLPPipeline
from kafka_client.kafka_producer import KafkaProducerClient
from kafka_client.kafka_consumer import KafkaConsumerClient

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_SCRAPE_TOPIC = os.getenv("KAFKA_SCRAPE_TOPIC", "scraped-posts")
KAFKA_COMMANDS_TOPIC = os.getenv("KAFKA_COMMANDS_TOPIC", "scraper-commands")
KAFKA_SCRAPE_TOPIC = os.getenv("KAFKA_SCRAPE_TOPIC", "fbreaper-topic")  # Align with Java backend topics
KAFKA_COMMANDS_TOPIC = os.getenv("KAFKA_COMMANDS_TOPIC", "scraper-control")
LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL", "http://localhost:5001/translate")

async def handle_scrape_command(command, scraper, nlp, producer):
    """
    Handles incoming scrape commands.
    """
    logging.info(f"Received command: {command}")
    if command['action'] == 'scrapeByKeyword':
        keyword = command['keyword']
        posts = await scraper.scrape_keyword(keyword)
        enriched_posts = []
        for post in posts:
            nlp_data = await nlp.process_post(post)
            enriched_posts.append({**post, **nlp_data})
        for enriched_post in enriched_posts:
            producer.send_message(KAFKA_SCRAPE_TOPIC, enriched_post)
            for enriched_post in enriched_posts:
                producer.send_message(KAFKA_SCRAPE_TOPIC, enriched_post)
        logging.info(f"Scraped and sent {len(enriched_posts)} posts for keyword '{keyword}'")
    elif command['action'] == 'start':
        # Custom scraping logic for full crawl or default action
        logging.info("Full crawl/start triggered (implement as needed)")
    elif command['action'] == 'stop':
        # Implement graceful shutdown or stop logic
        logging.info("Received stop command (not implemented)")
    else:
        logging.warning(f"Unknown command: {command}")

async def main():
    # Initialize components
    scraper = FacebookScraper()
    nlp = NLPPipeline(LIBRETRANSLATE_URL)
    producer = KafkaProducerClient(KAFKA_BROKER)
    consumer = KafkaConsumerClient(KAFKA_BROKER, KAFKA_COMMANDS_TOPIC)

    async def command_loop():
        async for command in consumer.listen():
            await handle_scrape_command(command, scraper, nlp, producer)

    await command_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("FBREAPER Scraper microservice stopped.")
