package com.industrial.backend.ai;

import java.util.ArrayList;
import java.util.List;

public class TextChunker {

    private static final int CHUNK_SIZE = 1000;
    private static final int OVERLAP = 200;

    public static List<String> split(String text) {

        List<String> chunks = new ArrayList<>();

        if (text == null || text.isBlank()) {
            return chunks;
        }

        int start = 0;

        while (start < text.length()) {

            int end = Math.min(start + CHUNK_SIZE, text.length());

            chunks.add(text.substring(start, end));

            if (end == text.length()) {
                break;
            }

            start = end - OVERLAP;
        }

        return chunks;
    }
}