

import java.io.File;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author amirb
 */
public class StylometricTechniques {
	
    double[] getLexicalFeatures(String text){
    	
    	 double vals[]=new double[28];
    	 StylometricTechniques tech = new StylometricTechniques();
        
    	 vals[0]= tech.characterCount(text);
    	 vals[1]= tech.characterCountWithoutSpaces(text);
    	 vals[2]= tech.ratioOfDigitsToN(text);
    	 vals[3]= tech.ratioOfLettersToN(text);
    	 vals[4]= tech.ratioOfUpperCaseLettersToN(text);
    	 vals[5]= tech.ratioOfWhiteSpacesToN(text);
    	 vals[6]= tech.ratioOfTabsToN(text);
    	 vals[7]= tech.ratioOfSpecialCharacterToN(text);
    	 vals[8]= tech.numberOfUpperCaseCharacters(text);
    	 vals[9]= tech.digitCount(text);
    	 vals[10]= tech.numberOfWhiteSpaces(text);
    	 vals[11]= tech.numberOfTabs(text);
    	 vals[12]= tech.percentageOfQuestionSentences(text);
    	 vals[13]= tech.percentageOfPunctuationCharacters(text);
    	 vals[14]= tech.percentageOfSemiColons(text);
    	 vals[15]= tech.percentageOfCommas(text);
    	 vals[16]= tech.averageWordLength(text);
    	 vals[17]= tech.yuleKMeasure(text);
    	 vals[18]= tech.hapaxLegomena(text);
    	 vals[19]= tech.totalNumberofWords(text);
    	 vals[20]= tech.averageSentenceLengthinCharacters(text);
    	 vals[21]= tech.ratioOfWordsWithLength3(text);
    	 vals[22]= tech.averageSentenceLengthinWords(text);
    	 vals[23]= tech.totalUniqueWords(text);
    	 vals[24]= tech.simpsonDMeasure(text);
    	 vals[25]= tech.sichelSMeasure(text);
    	 vals[26]= tech.brunetWMeasure(text);
    	 vals[27]= tech.honoreRMeasure(text);
    	// System.out.println("Honour measure is: "+ tech.honoreRMeasure(text));
    	 
    	 return vals;
    }
    /*
    public static void main(String[] args) {
        // average document length
        StylometricTechniques tech = new StylometricTechniques();
        String filePath =Constants.SAMPLE_DATA;
        String text = new FileUtils().readFileContents(filePath);
       
        double characterCount = tech.characterCount(text);
        double characterCountWithoutSpaces = tech.characterCountWithoutSpaces(text);
        double ratioOfDigits = tech.ratioOfDigitsToN(text);
        double ratioOfLetters = tech.ratioOfLettersToN(text);
        double ratioOfUpperCaseLetters = tech.ratioOfUpperCaseLettersToN(text);
        double ratioOfSpaces = tech.ratioOfWhiteSpacesToN(text);
        double ratioOfTabs = tech.ratioOfTabsToN(text);
        double ratioOfSpecialCharacters = tech.ratioOfSpecialCharacterToN(text);
        //int tokenCount = tech.tokenCount(text, "#");
        int numberOfUpperCaseCharacters = tech.numberOfUpperCaseCharacters(text);
        int numberOFdigits = tech.digitCount(text);
        int numberOfWhiteSpaces = tech.numberOfWhiteSpaces(text);
        int numberOfTabSpaces = tech.numberOfTabs(text);
        double pertentageOfQuestionSentences = tech.percentageOfQuestionSentences(text);
        double percentageOfPunctuationCharacters = tech.percentageOfPunctuationCharacters(text);
        double percentageOfSemiColons = tech.percentageOfSemiColons(text);
        double percentageOfCommas = tech.percentageOfCommas(text);
        
        System.out.println("Input text for Character based Features");
        System.out.println(text);
        System.out.println("Character Count    = " +characterCount);
        System.out.println("Ratio of Digits      = " + ratioOfDigits);
        System.out.println("Ratio of Letters     = " + ratioOfLetters);
        System.out.println("Ratio of UpperCase   = " + ratioOfUpperCaseLetters);
        System.out.println("Ratio of Spaces      = " + ratioOfSpaces);
        System.out.println("Ratio of Tabs        = " + ratioOfTabs);
        System.out.println("Ratio of Special     = " + ratioOfSpecialCharacters);
        System.out.println("Number of UpperCase  = " + numberOfUpperCaseCharacters);
        System.out.println("Number of Digits     = " + numberOFdigits);
        System.out.println("Number of Spaces     = " + numberOfWhiteSpaces);
        System.out.println("Number of Tabs       = " + numberOfTabSpaces);
        System.out.println("Percentage of Question sentences    = " + pertentageOfQuestionSentences);
        System.out.println("Percentage of punctuation characters= " + percentageOfPunctuationCharacters);
        System.out.println("Percentage of Semicolons            = " + percentageOfSemiColons);
        System.out.println("Percentage of Commas                = " + percentageOfCommas);
        
        
        
        double averageWordLength = tech.averageWordLength(text);
        double yuleMeasure = tech.yuleKMeasure(text);
        double hapaxLegomena = tech.hapaxLegomena(text);
        int totalWords = tech.totalNumberofWords(text);
        double averageSentenceLengthInCharacters = tech.averageSentenceLengthinCharacters(text);
        //System.out.println("averageSentenceLengthInCharacters = " + averageSentenceLengthInCharacters);
        double ratioOfLength3Words = tech.ratioOfWordsWithLength3(text);
        double averageSentenceLengthInWords = tech.averageSentenceLengthinWords(text);
        int totalUniqueWords = tech.totalUniqueWords(text);
        double simpsonDMeasure = tech.simpsonDMeasure(text);
        double sichelSMeasure = tech.sichelSMeasure(text);
        double brunetWMeasure = tech.brunetWMeasure(text);
        double honoreRMeasure = tech.honoreRMeasure(text);
        System.out.println("Input text for Word based Feature");
        System.out.println(text);
        
        System.out.println("Average Word Length     = " + averageWordLength);
        System.out.println("Yule K Measure          = " + yuleMeasure);
        System.out.println("Hapax Legomena          = " + hapaxLegomena);
        System.out.println("Total Words             = " + totalWords);
        System.out.println("Total Unique Words      = " + totalUniqueWords);
        System.out.println("Simpson Measure         = " + simpsonDMeasure);
        System.out.println("Sichel Measure          = " + sichelSMeasure);
        System.out.println("Brunet Measure          = " + brunetWMeasure);
        System.out.println("Honore Measure          = " + honoreRMeasure);
        System.out.println("Average Sentence Length in Characters = " + averageSentenceLengthInCharacters);
        System.out.println("Average Sentence Length in Words      = " + averageSentenceLengthInWords);
    }
    */

    public double averageWordLength(String text) {
        StylometricTechniques tech = new StylometricTechniques();
        double average = tech.characterCount(text) / tech.totalNumberofWords(text);
        return average;
    }

    public double averageDocumentLength(String authorFolder) {
        FileUtils dataReader = new FileUtils();
        int numOfDocs = new File(authorFolder).list().length;
        int totalWords = 0;
        for (File f : new File(authorFolder).listFiles()) {
            String fileContents = dataReader.readFileContents(f.getAbsolutePath());
            int wordCount = new StylometricTechniques().totalNumberofWords(fileContents);
            totalWords += wordCount;
            System.out.println("Words in File " + f.getName() + "\t " + wordCount);

        }

        double result = totalWords / numOfDocs;
        System.out.println("Total documents in folder " + numOfDocs);
        System.out.println("Total words in all documents " + totalWords);
        System.out.println("Average document length is " + result);

        return result;
    }

    // Average Number of Words per Sentence
//    public double averagWordsPerSentence(String text) {
//        String[] data = text.split("\\r?\\n");
//        int sentenceCount = 0;
//        for (String token : data) {
//            for (String obj : token.split(" ")) {
//                if (obj.contains(".") || obj.contains("?") || obj.contains("!")) {
//                    sentenceCount++;
//                }
//            }
//        }
//
//        System.out.println("num of sentences in the text : " + sentenceCount);
//
//        String[] wordsInText = text.split(" ");
//        System.out.println("num of words in the text : " + wordsInText.length);
//
//        double wordsPerSentence = wordsInText.length / sentenceCount;
//        System.out.println("Average words per sentence : " + wordsPerSentence);
//        return wordsPerSentence;
//    }

    // Average Number of words per Paragraph
    public double averageWordsPerParagraph(String text) {
        String[] paragraphs = text.split("\\r?\\n");
        //    String[] paragraphs1 = text.split(System.getProperty("line.separator"));
        System.out.println("Number of paragraphs in text : " + paragraphs.length);
        String[] wordsInText = text.split(" ");
        System.out.println("Total words in Text : " + wordsInText.length);
        double result = wordsInText.length / paragraphs.length;
        System.out.println("Average words per paragraph : " + result);
        return result;
    }

    public double characterCount(String text) {
        text = text.replaceAll("\\r", "");
        text = text.replaceAll("\\n", "");
        return text.toCharArray().length;
    }

    public double characterCountWithoutSpaces(String text) {
        text = text.replaceAll(" ", "");
        text = text.replaceAll("\\r", "");
        text = text.replaceAll("\\n", "");
        return text.toCharArray().length;
    }

    public int digitCount(String text) {
        int digitCount = 0;
        for (char c : text.toCharArray()) {
            String temp = "" + c;
            try {
                Double.parseDouble(temp);
                digitCount++;
            } catch (NumberFormatException ex) {

            }
        }
        return digitCount;
    }

    public double ratioOfDigitsToN(String text) {
        double characterCount = characterCount(text);
        double digitCount = digitCount(text);
        double result = (digitCount / characterCount) * 100;
        return result;
    }

    public double ratioOfLettersToN(String text) {
        char[] array = text.toCharArray();
        double count = 0;
        String expression = "^[a-zA-Z]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }

        return (count / (new StylometricTechniques().characterCount(text))) * 100;
    }

    public double ratioOfUpperCaseLettersToN(String text) {
        char[] array = text.toCharArray();
        double count = 0;
        String expression = "^[A-Z]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }

        return (count / (new StylometricTechniques().characterCount(text))) * 100;
    }

    public int numberOfUpperCaseCharacters(String text) {
        char[] array = text.toCharArray();
        int count = 0;
        String expression = "^[A-Z]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }

        return count;
    }

    public double ratioOfWhiteSpacesToN(String text) {
        char[] array = text.toCharArray();
        double count = 0;
        String expression = "^[ ]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }

        return (count / (new StylometricTechniques().characterCount(text))) * 100;

    }

    public int numberOfWhiteSpaces(String text) {
        char[] array = text.toCharArray();
        int count = 0;
        String expression = "^[ ]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }

        return count;
    }

    public double ratioOfTabsToN(String text) {
        String[] tokens = text.split("\t");
        double result = tokens.length - 1;
        return (result / new StylometricTechniques().characterCount(text)) * 100;

    }

    public int numberOfTabs(String text) {
        String[] tokens = text.split("\t");
        int result = tokens.length - 1;
        return result;

    }

    public double ratioOfSpecialCharacterToN(String text) {
        char[] array = text.toCharArray();
        double count = 0;
        String expression = "^[<>%j{}\\[\\]/\\@#wþ*()^&O${}]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }

        return (count / (new StylometricTechniques().characterCount(text))) * 100;

    }

//    public int tokenCount(String text, String token) {
//        int count = 0;
//        char[] data = text.toCharArray();
//        for (char c : data) {
//            String t = "" + c;
//            if (t.equals(token)) {
//                count++;
//            }
//        }
//        return count;
//    }

    public double percentageOfQuestionSentences(String text) {
        double count = 0;
        String[] data = text.split(" ");
        for (String token : data) {
            if (token.contains("?")) {
                count++;
            }
        }
//       if(!data[data.length-1].contains(".")) {
//           count--;
//       
        data = text.split("\\r+?\\n+");
        int sentenceCount = 0;
        for (String token : data) {
            for (String obj : token.split("\\s+")) {
                if (obj.contains(".") || obj.contains("?") || obj.contains("!")) {
                    sentenceCount++;
                }
            }

        }

        return (count / sentenceCount) * 100;
    }

    public double percentageOfPunctuationCharacters(String text) {
        char[] array = text.toCharArray();
        double count = 0;
        String expression = "^['\";:!.,]+";
        for (int i = 0; i < array.length; i++) {
            CharSequence seq = "" + array[i];

            Pattern pat = Pattern.compile(expression);
            Matcher mat = pat.matcher(seq);
            if (mat.matches()) {
                count++;
            }
        }
        return (count / (new StylometricTechniques().characterCount(text))) * 100;
    }

    public double percentageOfSemiColons(String text) {
        char[] data = text.toCharArray();
        double count = 0;
        for (char c : data) {
            String obj = "" + c;
            if (obj.equals(";")) {
                count++;
            }
        }
        return (count / (new StylometricTechniques().characterCount(text))) * 100;
    }

    public double percentageOfCommas(String text) {
        char[] data = text.toCharArray();
        double count = 0;
        for (char c : data) {
            String obj = "" + c;
            if (obj.equals(",")) {
                count++;
            }
        }
        return (count / (new StylometricTechniques().characterCount(text))) * 100;
    }

    public double averageSentenceLengthinCharacters(String text) {
        String[] data = text.split("\\r?\\n");
        double sentenceCount = 0;
        for (String token : data) {
            for (String obj : token.split("\\s+")) {
                if (obj.contains(".") || obj.contains("?") || obj.contains("!")) {
                    sentenceCount++;
                }
            }
        }
        text = text.replaceAll("\\r", "");
        text = text.replaceAll("\\n", "");
      //  text = text.replaceAll("\\.", "");
        double result = text.toCharArray().length / sentenceCount;
        
        return result;

    }

    public double averageSentenceLengthinWords(String text) {
        String[] data = text.split("\\r?\\n");
        double sentenceCount = 0;
        for (String token : data) {
            for (String obj : token.split(" ")) {
                if (obj.contains(".") || obj.contains("?") || obj.contains("!")) {
                    sentenceCount++;
                }
            }
        }
        int totalWords = new StylometricTechniques().totalNumberofWords(text);
        double result = totalWords / sentenceCount;
        return result;

    }

    public int totalNumberofWords(String text) {
        Scanner sc = new Scanner(text);
        int wordCount = 0;
        while (sc.hasNext()) {
            sc.next();
            wordCount++;
        }
        return wordCount;
    }

    public double honoreRMeasure(String text) {
        HashMap s = new StylometricTechniques().wordFrequency(text);
        Iterator it = s.keySet().iterator();
        double V1 = 0;
        while (it.hasNext()) {
            String word = (String) it.next();
            if (Integer.parseInt(s.get(word).toString()) == 1) {
                V1++;
            }
        }
        double V = s.size();
        Scanner sc = new Scanner(text);
        double N = new StylometricTechniques().totalNumberofWords(text);
        return (100 * (Math.log(N))) / (1 - (V1 / V));
    }

    public double sichelSMeasure(String text) {
        HashMap s = new StylometricTechniques().wordFrequency(text);
        Iterator it = s.keySet().iterator();
        double V2 = 0;
        while (it.hasNext()) {
            String word = (String) it.next();
            if (Integer.parseInt(s.get(word).toString()) == 2) {
                V2++;
            }
        }
        double V = s.size();
        return V2 / V;
    }

    public int totalUniqueWords(String text) {
        HashMap s = new StylometricTechniques().wordFrequency(text);
        return s.size();
    }

    public double brunetWMeasure(String text) {
        StylometricTechniques tech = new StylometricTechniques();
        double N = tech.totalNumberofWords(text);
        HashMap map = tech.wordFrequency(text);
        double V = map.size();
        double W = Math.pow(V, -.1654);
        W = Math.pow(N, W);
        return W;
    }

    public double yuleKMeasure(String text) {
        StylometricTechniques tech = new StylometricTechniques();
        double N = tech.totalNumberofWords(text);
        HashMap map = tech.wordFrequency(text);
        HashMap<Integer, Integer> yule = new HashMap<>();
        Iterator iter = map.keySet().iterator();

        while (iter.hasNext()) {
            int val = (Integer) map.get(iter.next());
            if (yule.containsKey(val)) {
                yule.put(val, yule.get(val) + 1);
            } else {
                yule.put(val, 1);
            }
        }
        double S2 = 0;
        iter = yule.keySet().iterator();
        while (iter.hasNext()) {
            int m = (Integer) iter.next();
            double VmN = (Integer) yule.get(m);
            double temp = (m * m) * VmN;
            S2 += temp;
        }
        double K = 10000 * ((S2 - N) / Math.pow(N, 2));
        return K;

    }

    public double simpsonDMeasure(String text) {
        StylometricTechniques tech = new StylometricTechniques();
        double N = tech.totalNumberofWords(text);
        HashMap map = tech.wordFrequency(text);
        HashMap<Integer, Integer> yule = new HashMap<>();
        Iterator iter = map.keySet().iterator();

        while (iter.hasNext()) {
            int val = (Integer) map.get(iter.next());
            if (yule.containsKey(val)) {
                yule.put(val, yule.get(val) + 1);
            } else {
                yule.put(val, 1);
            }
        }
        double D = 0;
        iter = yule.keySet().iterator();
        while (iter.hasNext()) {
            int m = (Integer) iter.next();
            double VmN = (Integer) yule.get(m);
            double mByN = m / N;
            double mMinus1ByNMinus1 = (m - 1) / (N - 1);
            double temp = VmN * mByN * mMinus1ByNMinus1;
            D += temp;
        }
        return D;
    }

    public HashMap<String, Integer> wordFrequency(String text) {
        HashMap<String, Integer> countByWords = new HashMap<String, Integer>();
        Scanner s = new Scanner(text);
        while (s.hasNext()) {
            String next = s.next();
            if (countByWords.containsKey(next)) {
                countByWords.put(next, countByWords.get(next) + 1);
            } else {
                countByWords.put(next, 1);
            }
        }
        s.close();

        return countByWords;
    }

    public double ratioOfWordsWithLength3(String text) {
        double totalWords = new StylometricTechniques().totalNumberofWords(text);
        Scanner sc = new Scanner(text);
        int counter = 0;
        while (sc.hasNext()) {
            String word = sc.next();
            if (word.length() <= 3) {
                counter++;
            }
        }
        return (counter / totalWords) * 100;
    }

    public double ratioOfWordsWithLength4(String text) {
        double totalWords = new StylometricTechniques().totalNumberofWords(text);
        Scanner sc = new Scanner(text);
        int counter = 0;
        while (sc.hasNext()) {
            String word = sc.next();
            if (word.length() == 3) {
                counter++;
            }
        }
        return (counter / totalWords) * 100;
    }

    public int hapaxLegomena(String text) {
        HashMap s = new StylometricTechniques().wordFrequency(text);
        Iterator it = s.keySet().iterator();
        int V1 = 0;
        while (it.hasNext()) {
            String word = (String) it.next();
            if (Integer.parseInt(s.get(word).toString()) == 1) {
                V1++;
            }
        }
        return V1;
    }
}
