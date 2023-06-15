package com.ml.controller;

import com.ml.service.TextSummarizer;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Map;

@Controller
public class TextSummarizerController {

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @PostMapping("/summarize")
    public String summarizeArticle(@RequestParam("url") String url, Model model) {
        try {
            Map<String, String> result = TextSummarizer.summarizeArticle(url);
            if (result.containsKey("error")) {
                model.addAttribute("error", result.get("error"));
            } else {
                model.addAttribute("originalText", result.get("originalText"));
                model.addAttribute("summary", result.get("summary"));
            }
            return "index";
        } catch (Exception e) {
            e.printStackTrace();
            model.addAttribute("error", "Error occurred while summarizing the article.");
            return "index";
        }
    }


    @GetMapping("/text")
    public String text() { return "text";}

    @PostMapping("/textSummarize")
    public String summarizeText1(@RequestParam("text") String text, Model model) {
        try {
            // Remove line breaks from the input text
            text = text.toLowerCase();
            text = text.replaceAll("\\r?\\n", ".");
            text = text.trim();

            String textSummary = TextSummarizer.summarizeText(text);
            model.addAttribute("textSummary", textSummary);
            return "text";
        } catch (Exception e) {
            e.printStackTrace();
            return "Error occurred while summarizing the article.";
        }
    }
}
