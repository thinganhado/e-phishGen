
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.util.StringUtils;

import java.util.*;
import java.io.IOException;
public class POSTagger {

	String applyPOSTagging(String s){
		
		   MaxentTagger tagger = new MaxentTagger("taggers/english-left3words-distsim.tagger");
	 
	        // The sample string
	        String sample = "This is a sample text";
	 
	        // The tagged string
	        String tagged = tagger.tagString(s);
	        //System.out.println(tagged);
	        return tagged;
	        // Output the result
	       
	}
	double[] countTaggings(String s){
		
		  double vals[]=new double[16];
		  // final String tagged = "World_NN Big_RBS old_RB stupid_JJ";
           final String tagged=s;
	        int nouns = 0;
	        int adjectives = 0;
	        int adverbs = 0;
            int verbs=0;
            int cd=0;  // Cardinal number
            int preposition=0;
            int fw=0; //Foreign word
            int particle=0;
            int symbol=0;
            int conjuction=0;
            int Determiner=0;
            int interrogative=0;
            int prp$=0; //Possessive pronoun
	        final String[] tokens = tagged.split(" ");
	        
	        
	        ArrayList tagList = new ArrayList();
	        HashMap bigrams = new HashMap();
	       System.out.println("Total tokens in postagers are: "+tokens.length);
	        for (final String token : tokens) {
	        	 //System.out.println(token);
	            final int lastUnderscoreIndex = token.lastIndexOf("_");
	            final String realToken = token.substring(lastUnderscoreIndex + 1);
	            tagList.add(realToken);
	            if ("NN".equals(realToken)||  "NNS".equals(realToken) || "NNP".equals(realToken) || "NNPS".equals(realToken) ) {
	                nouns++;
	            }
	            if ("JJ".equals(realToken) || "JJR".equals(realToken) || "JJR".equals(realToken)) {
	                adjectives++;
	            }
	            if ("RB".equals(realToken) || "RBS".equals(realToken)|| "RBR".equals(realToken) ) {
	                adverbs++;
	            }
	            if ("VB".equals(realToken) || "VBD".equals(realToken)|| "VBG".equals(realToken) 
	            		|| "VBN".equals(realToken) || "VBP".equals(realToken) || "VBZ".equals(realToken))  {
	                verbs++;
	            }
	            if ("CD".equals(realToken) )  {
	                cd++;
	            }
	            if ("IN".equals(realToken) || "TO".equals(realToken) )  {
	            	preposition++;
	            }
	            if ("RP".equals(realToken) )  {
	            	particle++;
	            }
	            if ("SYM".equals(realToken) )  {
	            	symbol++;
	            }
	            if ("CC".equals(realToken) )  {
	            	conjuction++;
	            }
	            if ("DT".equals(realToken) )  {
	            	Determiner++;
	            }
	            if ("WDT".equals(realToken) || "WP".equals(realToken) ||"WRB".equals(realToken) )  {
	            	
	            	interrogative++;
	            }
	            if ("FW".equals(realToken) )  {
	            	fw++;
	            }
	            if ("PRP$".equals(realToken) )  {
	            	prp$++;
	            }
	            
	        }
            vals[0]=nouns;
            vals[1]=adjectives;
            vals[2]=adverbs;
            vals[3]=verbs;
            vals[4]=cd;
            vals[5]=preposition;
            vals[6]=particle;
            vals[7]=symbol;
            vals[8]=conjuction;
            vals[9]=Determiner;
            vals[10]=interrogative;
            vals[11]=fw;
            vals[12]=prp$;
            
            
            		
	       // System.out.println(String.format("Nouns: %d Adjectives: %d, Adverbs: %d, Verbs: %d,"
	       // 		+ " Cardinal_NO: %d, Prepositions: %d, Particles: %d, Symbols: %d, Conjuction: %d"
	       // 		+ " Determiner: %d, Interrogatives: %d, ForeignWords: %d, Possesive_Pronoun: %d"
	       // , nouns, adjectives, adverbs,verbs,cd,preposition, particle, symbol,
	       // conjuction,Determiner,interrogative,fw,prp$));
	    //   System.out.println(tagList);
	       String sc=StringUtils.join(tagList, " ");
	      // System.out.println(sc);
	       Set<Integer> set = new LinkedHashSet<Integer>(tagList);
	       System.out.println("Total Unigram tokens: "+tagList.size()+ " Unique Unigram tokens: "+set.size());
	       float unigramDensity=(set.size()/(float)tagList.size())*100;
	       System.out.println("Unigram Density is: "+unigramDensity);
	       
	        BigramClass bigram= new BigramClass();
	        bigram.countBigrams(sc);
	        
	        TrigramClass tc= new TrigramClass();
	        tc.countBigrams(sc);
	       
	        vals[13]=unigramDensity;
	        vals[14]=bigram.countDensity();
	        vals[15]=tc.countDensity();
	        
	       
	        return vals;
	       
	       
	}
}
