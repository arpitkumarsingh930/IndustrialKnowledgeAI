package com.industrial.backend.controller;

import com.industrial.backend.entity.Document;
import com.industrial.backend.service.DocumentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/api/documents")
@CrossOrigin(origins = "http://localhost:5173")
public class DocumentController {

    @Autowired
    private DocumentService service;

    @PostMapping("/upload")
    public Document upload(@RequestParam("file") MultipartFile file) throws IOException {
        return service.upload(file);
    }
}