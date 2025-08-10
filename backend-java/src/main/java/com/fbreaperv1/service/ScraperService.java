package com.fbreaperv1.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ScraperService {
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    private static final String SCRAPER_CONTROL_TOPIC = "scraper-control";
    private static final String SCRAPER_STATUS_URL = "http://localhost:5000/status";

    public void triggerScraper() {
        kafkaTemplate.send(SCRAPER_CONTROL_TOPIC, "{\"action\":\"start\"}");
    }

    public String getScraperStatus() {
        try {
            RestTemplate restTemplate = new RestTemplate();
            return restTemplate.getForObject(SCRAPER_STATUS_URL, String.class);
        } catch (Exception e) {
            return "Error fetching scraper status: " + e.getMessage();
        }
    }
}
