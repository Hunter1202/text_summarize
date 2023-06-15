package com.ml.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class TextSummarizer {

    public static String summarizeText(String text) {
        try {
            // Provide the path to your Python interpreter and the script file
            ProcessBuilder pb = new ProcessBuilder("python3", "/app/TextSum.py");

            // Pass the text as an environment variable to the Python script
            pb.environment().put("text", text);

            Process process = pb.start();

            // Read the output of the Python script
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder summaryBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                summaryBuilder.append(line).append("\n");
            }

            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String errorLine;
            while ((errorLine = errorReader.readLine()) != null) {
                System.err.println(errorLine);
            }

            // Wait for the process to finish and get the exit code
            int exitCode = process.waitFor();

            if (exitCode == 0) {
                // Process the summary or return it as needed
                String summary = summaryBuilder.toString();
                return summary;
            } else {
                // Handle any errors or return an error message
                return "Error occurred";
            }

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return "Error occurred while summarizing the text.";
        }
    }

    public static Map<String, String> summarizeArticle(String url) {
        try {
            ProcessBuilder pb = new ProcessBuilder("python3", "/app/ArticleSum.py");
            pb.environment().put("url", url);

            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder originalTextBuilder = new StringBuilder();
            StringBuilder summaryBuilder = new StringBuilder();
            String line;
            boolean isSummary = false;
            while ((line = reader.readLine()) != null) {
                if (line.equals("Văn bản gốc:")) {
                    isSummary = false;
                } else if (line.equals("Văn bản tóm tắt:")) {
                    isSummary = true;
                } else {
                    if (isSummary) {
                        summaryBuilder.append(line).append("\n");
                    } else {
                        originalTextBuilder.append(line).append("\n");
                    }
                }
            }

            int exitCode = process.waitFor();

            if (exitCode == 0) {
                Map<String, String> result = new HashMap<>();
                result.put("originalText", originalTextBuilder.toString());
                result.put("summary", summaryBuilder.toString());
                return result;
            } else {
                return Collections.singletonMap("error", "HTTP Error 403: Forbidden\nOr the URL is wrong");
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return Collections.singletonMap("error", "Error occurred while summarizing the article.");
        }
    }
}
