
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.*;

public class PreprocessClass {

	String removeElements(String s){
	
		return s.replaceAll("[^A-Za-z0-9\\s]", "");
	
	}
	
}
