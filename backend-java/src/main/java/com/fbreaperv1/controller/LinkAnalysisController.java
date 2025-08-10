package com.fbreaperv1.controller;

import com.fbreaperv1.service.LinkAnalysisService;
import com.fbreaperv1.model.LinkAnalysisResult;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/link-analysis")
public class LinkAnalysisController {

    private final LinkAnalysisService linkAnalysisService;

    public LinkAnalysisController(LinkAnalysisService linkAnalysisService) {
        this.linkAnalysisService = linkAnalysisService;
    }

    @GetMapping("/{postId}")
    public ResponseEntity<LinkAnalysisResult> analyzeLinks(@PathVariable String postId) {
        return ResponseEntity.ok(linkAnalysisService.analyzeLinks(postId));
    }
}
