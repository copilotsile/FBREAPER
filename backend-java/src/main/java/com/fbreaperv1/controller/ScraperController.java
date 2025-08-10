package com.fbreaperv1.controller;

import com.fbreaperv1.kafka.KafkaProducerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/scraper")
public class ScraperController {

	private final KafkaProducerService kafkaProducerService;

	public ScraperController(KafkaProducerService kafkaProducerService) {
		this.kafkaProducerService = kafkaProducerService;
	}

	/**
	 * Triggers the scraper to start scraping (all or default)
	 */
	@PostMapping("/start")
	public ResponseEntity<String> startScraper() {
		kafkaProducerService.sendMessage("scraper-control", "{\"action\":\"start\"}");
		return ResponseEntity.ok("Scraper start command sent");
	}

	/**
	 * Triggers the scraper to scrape by keyword or username
	 */
	@PostMapping("/scrapeByKeyword")
	public ResponseEntity<String> scrapeByKeyword(@RequestParam String keyword) {
		String msg = String.format("{\"action\":\"scrapeByKeyword\",\"keyword\":\"%s\"}", keyword);
		kafkaProducerService.sendMessage("scraper-control", msg);
		return ResponseEntity.ok("Scrape by keyword command sent");
	}
}
