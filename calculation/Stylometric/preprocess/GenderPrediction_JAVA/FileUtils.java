

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;


public class FileUtils {

    public String readFileContents(String filePath) {
        FileInputStream fstream = null;
        BufferedReader br = null;
        String text = "";
        try {
            fstream = new FileInputStream(new File(filePath));
            br = new BufferedReader(new InputStreamReader(fstream));
            String strLine;
//Read File Line By Line
            while ((strLine = br.readLine()) != null) {
                text += strLine+"\n";
            }
            br.close();
        } catch (Exception ex) {
        }
        return text;
    }
    public static void detectLinkFile(String folder) {
        File[] files = new File(folder).listFiles();
        for(File f : files) {
            String text = new FileUtils().readFileContents(f.getAbsolutePath());
            if(text.contains("http")) {
                System.out.println("link file : " + f.getAbsolutePath());
            }
        }
    }
}
