package com.fbreaperv1.controller;

import com.fbreaperv1.kafka.KafkaProducerService;
import com.fbreaperv1.model.KafkaMessage;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;

@RestController
@RequestMapping("/api/data")
public class DataController {
    private final KafkaProducerService kafkaProducerService;
    private final com.fbreaperv1.service.DataService dataService;
    private final com.fbreaperv1.common.EntityMapper entityMapper;

    public DataController(KafkaProducerService kafkaProducerService, com.fbreaperv1.service.DataService dataService, com.fbreaperv1.common.EntityMapper entityMapper) {
        this.kafkaProducerService = kafkaProducerService;
        this.dataService = dataService;
        this.entityMapper = entityMapper;
    }

    @GetMapping("/posts")
    public ResponseEntity<?> getAllPosts() {
        return ResponseEntity.ok(dataService.getAllPosts().stream().map(entityMapper::toPostDTO).toList());
    }

    @GetMapping("/comments")
    public ResponseEntity<?> getAllComments() {
        return ResponseEntity.ok(dataService.getAllComments().stream().map(entityMapper::toCommentDTO).toList());
    }

    @GetMapping("/stats")
    public ResponseEntity<?> getStats() {
        // Real stats: post count, comment count, and latest post/comment timestamp
        int postCount = dataService.getAllPosts().size();
        int commentCount = dataService.getAllComments().size();
        String latestPostTime = dataService.getAllPosts().stream()
            .map(p -> {
                try { return p.getTimestamp(); } catch (Exception e) { return null; }
            })
            .filter(java.util.Objects::nonNull)
            .max(String::compareTo)
            .orElse(null);
        String latestCommentTime = dataService.getAllComments().stream()
            .map(c -> {
                try { return c.getTimestamp(); } catch (Exception e) { return null; }
            })
            .filter(java.util.Objects::nonNull)
            .max(String::compareTo)
            .orElse(null);
        return ResponseEntity.ok(Map.of(
            "posts", postCount,
            "comments", commentCount,
            "latestPostTime", latestPostTime,
            "latestCommentTime", latestCommentTime
        ));
    }


    /**
     * Receives scraped data from scraper and sends it to Kafka
     * @param message KafkaMessage object containing type and payload
     * @return HTTP 200 if successful
     */
    @PostMapping("/ingest")
    public ResponseEntity<String> ingestData(@RequestBody KafkaMessage message) {
        if (message.getType() == null || message.getPayload() == null) {
            return ResponseEntity.badRequest().body("Invalid message: type and payload required");
        }
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            String jsonMessage = objectMapper.writeValueAsString(message);
            kafkaProducerService.sendMessage(message.getType(), jsonMessage);
            return ResponseEntity.ok("Data sent to Kafka successfully");
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to serialize message");
        }
    }

    /**
     * Simple health check for DataController
     */
    @GetMapping("/ping")
    public ResponseEntity<String> ping() {
        return new ResponseEntity<>("DataController is live", HttpStatus.OK);
    }
}
