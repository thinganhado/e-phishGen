

public class SyntacticFeatures {

	
	int countApostrophe(String s) {
		int c=0;
		for(int i = 0; i < s.length(); i++) {
		    if(s.charAt(i)=='’' || s.charAt(i)=='\'' || s.charAt(i)==39){
		    	
		    	c++;
		    }
		}
        return c;
	}
	int countBrackets(String s){
		int c=0;
		for(int i = 0; i < s.length(); i++) {
		    if(s.charAt(i)=='[' || s.charAt(i)==']' || s.charAt(i)=='(' || s.charAt(i)==')'
		    		|| s.charAt(i)=='{' || s.charAt(i)=='}' || s.charAt(i)=='<' || s.charAt(i)=='>'){
		    	
		    	c++;
		    }
		}
        return c;
	}
	int countColon(String s){
		
		int c=0;
		for(int i = 0; i < s.length(); i++) {
		    if(s.charAt(i)==':'){
		    	
		    	c++;
		    }
		}
        return c;
		
	}
	    
int countComma(String s){
		
		int c=0;
		for(int i = 0; i < s.length(); i++) {
		    if(s.charAt(i)==',' || s.charAt(i)=='،' || s.charAt(i)=='、' ){
		    	
		    	c++;
		    }
		}
        return c;
	}
int countDash(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
	    if(s.charAt(i)=='‒' ){
	    	
	    	c++;
	    }
	}
    return c;
}
int countEllipsis(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
		
	    if(s.charAt(i)=='…'){
	    	
	    	c++;
	    }
	}
	if(s.contains("...")){
    	
    	c++;
    	
    }
    return c;
}
int countExclamation(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
	    if(s.charAt(i)=='!' ){
	    	
	    	c++;
	    }
	}
    return c;
}
int countFullStop(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
	    if(s.charAt(i)=='.' ){
	    	
	    	c++;
	    }
	}
    return c;
}
int countQMark(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
	    if(s.charAt(i)=='?' ){
	    	
	    	c++;
	    }
	}
    return c;
}
int countSemicolon(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
		if(s.charAt(i)==';' ){
	    	
	    	c++;
	    }
	}
    return c;
}
int countSlash(String s){
	int c=0;
	for(int i = 0; i < s.length(); i++) {
		if(s.charAt(i)=='/' || s.charAt(i)=='\\'  ){
	    	
	    	c++;
	    }
	}
    return c;
}
}
