package lfs;

import java.util.Scanner;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;




public class Zero {
    public static String READ(String str){
        return str;
    }

    public static String EVAL(String ast,String env){
        return ast;
    }

    public static String PRINT(String exp){
        return exp;
    }

    public static String RE(String env, String str){
        return EVAL(READ(str),env);
    }
    public static void main(String[] args) {

        if (args.length > 0) {
            return;
        }
        //Scanner input = new Scanner(System.in);
        BufferedReader buffer=new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String prompt = "--> ";
	    String line = "";
	    System.out.print(prompt);
	    try{
            	line = buffer.readLine();
            	if (line == null) {
                	continue;
            	}
	    }catch(IOException e){
	    	System.out.println("IOException : " + e.getMessage());
	    	break;
	    }
            System.out.println(PRINT(RE(null,line)));
        }
    }
}
