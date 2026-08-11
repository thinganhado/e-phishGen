
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.*;



public class ReadData {

	
	 String removeUrl(String commentstr)
    {
        commentstr=commentstr.replaceAll("http?://\\S+\\s?", "");
        commentstr=commentstr.replaceAll("https?://\\S+\\s?", "");
        commentstr=commentstr.replaceAll("ftp?://\\S+\\s?", "");
        commentstr=commentstr.replaceAll("file?://\\S+\\s?", "");
        commentstr=commentstr.replaceAll("gopher?://\\S+\\s?", "");
        commentstr=commentstr.replaceAll("telnet?://\\S+\\s?", "");
        return commentstr;
    }
	 String readFile(String fileName) throws IOException {
		 
	    BufferedReader br = new BufferedReader(new FileReader(fileName));
	    try {
	        StringBuilder sb = new StringBuilder();
	        String line = br.readLine();

	        while (line != null) {
	            sb.append(line);
	            sb.append("\n");
	            line = br.readLine();
	        }
	        return sb.toString();
	    } finally {
	        br.close();
	    }
	}
	
}
