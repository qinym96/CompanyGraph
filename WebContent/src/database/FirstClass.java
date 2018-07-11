package database;

//package mavenTest.maven;

//package mydb.firstproject;
import com.alibaba.fastjson.*;
import net.sf.json.JSONObject;


import java.util.List;
import java.util.Map;

import javax.management.Query;

import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;

import com.arangodb.ArangoCollection;
import com.arangodb.ArangoCursor;
import com.arangodb.ArangoDB;
import com.arangodb.ArangoDBException;
import com.arangodb.ArangoDatabase;
import com.arangodb.entity.BaseDocument;
import com.arangodb.entity.CollectionEntity;
import com.arangodb.model.AqlQueryOptions;
import com.arangodb.util.MapBuilder;
import com.arangodb.velocypack.VPackSlice;
import com.arangodb.velocypack.exception.VPackException;

public class FirstClass {
	public static String getVertexJSONString() {
		//取得全部数据@@
		final ArangoDB arangoDB = new ArangoDB.Builder().build();	    
		ArangoDatabase mydb = arangoDB.db("_system");
		 // mydb.createCollection("test");
		ArangoCollection collectionName = mydb.collection("_system");

		String queryCmmd = "for doc in @@collection return doc";
	    Map bindVars =new MapBuilder().put("@collection", "entity").get();
	    //map.put("@collection","test");
	    
	    ArangoCursor<BaseDocument> cursor = mydb.query(queryCmmd, bindVars, null, BaseDocument.class);
	    int i = 0;	    
	    JSONObject[] jsonArray;	    
	    int len=1484;
	    jsonArray = new JSONObject[len];
	    
	    //System.out.println("test");
	    while (cursor.hasNext()) {
	       
	        BaseDocument object = cursor.next();
	        object.addAttribute("n", i);
	        // String name =object.getAttribute("name").toString();     //输出 
	        
		    //System.out.println(i+"   " +object.toString()); 		    
		   // String jsonStr = JSON.toJSONString(object);	       
	        Object key1="name";
	        Object key2="legal_man";
	        Object key3="establishment_date";
	        Object key4="company_address";
	        Object key5="registered_capital";
	        //Object key6 ="id";
	        //Object key7 ="n";
	        //System.out.println("jsonString: " + object.getProperties().get(key1));
	        //System.out.println("legalman:  "+object.getProperties().get(key2));
	        
	        //Map m= new HashMap();
	        //m.put(key1, object.getProperties().get(key1));
	        //m.put(key2, object.getProperties().get(key2));
	        
	        //JSONObject jsonStu = JSONObject.fromObject(object);
	        
	        
	        JSONObject jsonObj = new JSONObject();
	        jsonObj.put("name", object.getProperties().get(key1));
	        jsonObj.put("legal_man", object.getProperties().get(key2));
	        jsonObj.put("establishment_date", object.getProperties().get(key3));
	        jsonObj.put("company_address", object.getProperties().get(key4));
	        jsonObj.put("registered_capital", object.getProperties().get(key5));
	        jsonObj.put("id", object.getId());
	        
	        JSONObject newjsonObj =new JSONObject();
	        newjsonObj.put("id", i);
	        
	        
	        //System.out.println(jsonObj);
	        jsonArray[i]=jsonObj;
	        i++;
	        
	        //System.out.println(i+"   "+jsonArray[i]);
		}
	   // System.out.println(jsonArray[1]);
	   String s=Arrays.toString(jsonArray);
	    return s;
	}
	
	public static String getEdgeJSONString() {
		//取得全部数据@@
		final ArangoDB arangoDB = new ArangoDB.Builder().build();	    
		ArangoDatabase mydb = arangoDB.db("_system");
		 // mydb.createCollection("test");
		ArangoCollection collectionName = mydb.collection("_system");
		String queryCmmd = "for doc in @@collection return doc";
	    Map bindVars =new MapBuilder().put("@collection", "relation").get();
	    
	    ArangoCursor<BaseDocument> cursor = mydb.query(queryCmmd, bindVars, null, BaseDocument.class);
	    int i = 0;	    
	    JSONObject[] jsonArray;	    
	    int len=1451;
	    jsonArray = new JSONObject[len];
	    
	    while (cursor.hasNext()) {
	       
	        BaseDocument object = cursor.next();
	        object.addAttribute("n", i);
	        
	        Object key1="_from";
	        Object key2="_to";
	      
	       	        
	        JSONObject jsonObj = new JSONObject();
	        jsonObj.put("source", object.getProperties().get(key1));
	        jsonObj.put("target", object.getProperties().get(key2));
	        jsonObj.put("relation", object.getProperties().get("name"));
	      	        
	        //System.out.println(jsonObj);
	        jsonArray[i]=jsonObj;
	        i++;	        
	        //System.out.println(i+"   "+jsonArray[i]);
		}
	    String s=Arrays.toString(jsonArray);
	    return s;
	}


}