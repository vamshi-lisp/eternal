package lfs;

import java.util.Scanner;
import java.io.IOException;

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
        Scanner input = new Scanner(System.in);
        while (true) {
            String prompt = "-=) ";
	    String line = "";
	    System.out.print(prompt);
	    try{
            	line =   input.nextLine().trim();
            	if (line == null) {
                	continue;
            	}
	    }catch(Exception e){
	    	System.out.println("IOException : " + e.getMessage());
	    	break;
	    }
            System.out.println(PRINT(RE(null,line)));
        }
    }
}
