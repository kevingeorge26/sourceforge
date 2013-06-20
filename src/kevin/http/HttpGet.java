package kevin.http;

import java.io.File;
import java.io.IOException;
import java.net.URL;

import javax.swing.plaf.SliderUI;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class HttpGet {

	public static int timeout= 1000 * 20;
	
	public static void main(String[] args) {
		try {			
			getProjectList();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void getProjectList(){
		String link = "http://sourceforge.net/directory/?q=rfc&page=";
		int pageLimit = 1;
		try {
			for(int i = 1 ; i <= pageLimit ; i++ ){

				Document doc = Jsoup.connect(link + Integer.toString(i)).userAgent("Mozilla").data("name", "jsoup").timeout(timeout).get();
				getProjectPage(doc);
			}
		}
		catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
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
			String projectName = temp.substring(21, temp.length());
			System.out.println(projectName);
			Project project = new Project(link,projectName);
			
		}
	}


}
