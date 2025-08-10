package com.fbreaperv1.kafka;

import com.fbreaperv1.service.DataService;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumerService {

    private final DataService dataService;

    public KafkaConsumerService(DataService dataService) {
        this.dataService = dataService;
    }

    @KafkaListener(topics = "fbreaper-topic", groupId = "fbreaper-group")
    public void consumeMessage(String message) {
        System.out.println("Received Kafka message: " + message);
        // Pass message to DataService for processing
        dataService.processIncomingData(message);
    }
}
