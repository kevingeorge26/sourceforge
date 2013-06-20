package kevin.http;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Project
{
	private static final Pattern rfcPattern = Pattern.compile("(rfc\\s*[0-9]+|RFC\\s*[0-9]+)");	
	private static final String baseLink = "http://sourceforge.net";
	private static final String rfcBaseLink = "http://tools.ietf.org//rfc//";
	private static final String withRFC = "with_rfc";
	private static final String withoutRFC = "without_rfc";

	Set<String> rfcList = new HashSet<String>(); // to keep track which RFC were mentioned
	String projectName;

	int rfcFoundCounter = 0,rfcNotFoundCounter = 0;
	BufferedWriter bw;
	
	public Project(String link,String projectName) {
		getRFCString(link); // get rfc from link
		this.projectName = projectName;
		link = baseLink + link;
	
		try {
			Document doc = Jsoup.connect(link).userAgent("Mozilla").data("name", "jsoup").timeout(HttpGet.timeout).get();
			boolean foundRFC = searchRFC(doc);

			if(!foundRFC){
				rfcNotFoundCounter++;
				File folder = new File(withoutRFC + File.separator + projectName);
				folder.mkdir();
				bw = new BufferedWriter(new FileWriter(new File(withoutRFC + File.separator + projectName + File.separator + "ReadMe.txt")));
			}

			writeDetails("Project Name : " + projectName);
			writeDetails("Project link : " + link);
			
			getDownloadProject(doc,foundRFC);
			bw.close();

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private void writeDetails(String line){
		try {
			bw.write(line);
			bw.newLine();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private boolean getDownloadProject(Document doc,boolean foundRFC){
		boolean downloadPageFound = false;
		Elements elements = doc.select("section#download_button a.sfdl");
		for(Element element : elements){
			downloadPageFound = true;

			String filename = element.select("span").text().split(" ")[1];
			String link = element.attr("href");

			try {
				String filedownloadLink = Jsoup.connect(baseLink+link).userAgent("Mozilla").data("name", "jsoup").timeout(HttpGet.timeout).get().select("div#starting a.direct-download").attr("href");
				if(filedownloadLink != null){
					File test;
					if(foundRFC)
						test = new File(withRFC + File.separator + projectName + File.separator + filename);
					else
						test = 	new File(withoutRFC + File.separator + projectName + File.separator + filename);

					org.apache.commons.io.FileUtils.copyURLToFile(new URL(filedownloadLink), test);
					
				}
				else{
					System.out.println("there was no download link");
					writeDetails("No download link was found");
				}

			} catch (IOException e) {
				writeDetails("Error occurred while trying to download the file");
				e.printStackTrace();
			}
		}		

		return downloadPageFound;
	}

	private boolean searchRFC(Document doc){
		boolean rfcDocFound = false;
		//get all the rfc names
		Elements elements = doc.select("section#main-content");
		for(Element ele : elements){
			for(Element ele1 : ele.getAllElements()){
				getRFCString(ele1.ownText());
			}
		}

		// try to download the rfc
		for(String rfcName : rfcList){
			try {

				Document rfcdoc = Jsoup.connect(rfcBaseLink+ rfcName).timeout(HttpGet.timeout).get();

				File folder = new File(withRFC + File.separator + projectName );
				if(!folder.exists()){
					rfcFoundCounter++;
					folder.mkdir();					
					folder = new File(withRFC + File.separator + projectName + File.separator + "rfc");
					folder.mkdir();
					bw = new BufferedWriter(new FileWriter(new File(withRFC + File.separator + projectName + File.separator + "ReadMe.txt")));
				}
				writeDetails("RFC found " + rfcName);
				File file = new File(withRFC + File.separator + projectName + File.separator + "rfc" + File.separator + rfcName + ".txt");
				org.apache.commons.io.FileUtils.copyURLToFile(new URL(rfcBaseLink+ rfcName), file);
				rfcDocFound = true;				

			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return rfcDocFound;
	}

	private void getRFCString(String line){
		Matcher mat = rfcPattern.matcher(line);

		while(mat.find()){
			int start = mat.start();
			int end = mat.end();
			rfcList.add(line.substring(start,end).toLowerCase().replaceAll(" ", ""));
		}			
	}
}
