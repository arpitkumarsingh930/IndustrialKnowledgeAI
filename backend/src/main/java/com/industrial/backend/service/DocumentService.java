package com.industrial.backend.service;

import com.industrial.backend.ai.TextChunker;
import com.industrial.backend.config.FileStorageConfig;
import com.industrial.backend.dto.ProcessRequest;
import com.industrial.backend.entity.Document;
import com.industrial.backend.entity.DocumentChunk;
import com.industrial.backend.repository.DocumentChunkRepository;
import com.industrial.backend.repository.DocumentRepository;
import com.industrial.backend.util.PdfExtractor;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class DocumentService {

    @Autowired
    private DocumentRepository repository;

    @Autowired
    private DocumentChunkRepository chunkRepository;

    @Autowired
    private FileStorageConfig storageConfig;

    @Autowired
    private RestTemplate restTemplate;

    public Document upload(MultipartFile file) throws IOException {

        // Original file name
        String fileName = file.getOriginalFilename();

        // Upload path
        Path path = Paths.get(storageConfig.getUploadDir(), fileName);

        // Save PDF
        Files.copy(file.getInputStream(), path, StandardCopyOption.REPLACE_EXISTING);

        // Extract text
        String extractedText = PdfExtractor.extractText(path.toString());

        // Split into chunks
        List<String> chunks = TextChunker.split(extractedText);

        System.out.println("Total Chunks : " + chunks.size());

        for (int i = 0; i < chunks.size(); i++) {
            System.out.println("========== CHUNK " + (i + 1) + " ==========");
            System.out.println(chunks.get(i));
        }

        // Create document
        Document document = new Document();

        document.setFileName(fileName);
        document.setFileType(file.getContentType());
        document.setFileSize(file.getSize());
        document.setFilePath(path.toString());
        document.setUploadTime(LocalDateTime.now());
        document.setExtractedText(extractedText);

        // Save document
        Document savedDocument = repository.save(document);

        // Save chunks
        for (int i = 0; i < chunks.size(); i++) {

            DocumentChunk chunk = new DocumentChunk();

            chunk.setChunkIndex(i);
            chunk.setChunkText(chunks.get(i));
            chunk.setDocument(savedDocument);

            chunkRepository.save(chunk);
        }

        // -------------------------------
        // Send chunks to FastAPI
        // -------------------------------

        ProcessRequest request = new ProcessRequest();

        request.setDocumentId(savedDocument.getId());
        request.setChunks(chunks);

        System.out.println("==================================");
        System.out.println("Before FastAPI call");
        System.out.println("Document ID : " + savedDocument.getId());
        System.out.println("Total Chunks : " + chunks.size());

        try {

            String response = restTemplate.postForObject(
                    "http://127.0.0.1:8000/process",
                    request,
                    String.class
            );

            System.out.println("After FastAPI call");
            System.out.println("FastAPI Response: " + response);

        } catch (Exception e) {

            System.out.println("FastAPI call failed!");
            e.printStackTrace();

        }

        System.out.println("==================================");

        return savedDocument;
    }
}