package kevin.http;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import javax.swing.plaf.SliderUI;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class HttpGet {

	public static int timeout= 1000 * 20;
	static int pageLimit = 23;

	public static void main(String[] args) {
		try {			
			getProjectList();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void getProjectList(){
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String link = "http://sourceforge.net/directory/?q=rfc&page=";
		int i = 8;
		
		while(i<pageLimit){
			try {
				System.out.println("page ********" + i);
				Document doc = Jsoup.connect(link + Integer.toString(i)).userAgent("Mozilla").data("name", "jsoup").timeout(timeout).get();
				getProjectPage(doc);
				i++;
				System.out.println("enter y to continiue or n to stop");
				String choice = br.readLine();
				
				if(choice.equals("n")){
				System.out.println("going to exit. the  next page " + String.valueOf(i) );
				}
			}
			catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				synchronized (lock) {
					try {
						lock.wait(1000*20);
					} catch (InterruptedException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
				}	
			}
		}
		System.out.println("projects with rfc " + Project.rfcFoundCounter);
		System.out.println("projects without rfc " + Project.rfcNotFoundCounter);
	}

	static Object lock = new Object();

	public static void getProjectPage(Document doc){
		Elements elements = doc.select("section#result_data ul.projects a.project-icon");
		//Project project = new Project("/projects/libmd5-rfc/?source=dlp","test");

		for(Element ele : elements){
			try {
				synchronized (lock) {
					lock.wait(1000*4);
				}				
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			String link = ele.attr("href");
			String temp = ele.attr("title");
			String projectName = temp.replace("Find out more about ", "");
			System.out.println(projectName);

			Project project = new Project(link,projectName);			

		}
	}


}
