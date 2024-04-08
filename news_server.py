from flask import Flask, render_template, redirect,url_for
from requests import get,post
import json
import sqlite3
from time import sleep
import ast
class news:
        def __init__(self, arg=''):
                super(news, self).__init__()
                self.arg = arg
                self.error=""
                self.news=[]
                self.categories=["sports","fashion","politics","science","africa","religion","weather"]
                self.api_key=""
                self.query="kenya"
                self.db_name="news.db"
                self.news_url="https://newsdata.io/api/1/news?apikey="+self.api_key #"&q="+self.query
        def save_all(self):
                cats=self.categories
                for cat in cats:
                        newss=news()
                        newss.query=cat
                        newss.get_news()
                        sleep(2)
                        newss.save_News()
                        print(cat+" >> "+str(newss.error))
                        sleep(1)
        def get_news(self):
            try:
                re=get(self.news_url)
                if re.status_code==200:
                    self.news=json.loads(re.text)
                else:
                    self.error=re.status_code
            except Exception as err:
                 pass
                 self.error=err
                
        def save_News(self):
                if self.error=="":
                        self.create_DB()
                        hay=self.news['results']
                        for newsp in hay:
                                h=newsp
                                title=h["title"]
                                link=h["link"]
                                keywords=h["keywords"]
                                creator=h["creator"]
                                description=h["description"]
                                content=h["content"]
                                publish_date=h["pubDate"]
                                full_description=h["description"]
                                image_url=h["image_url"]
                                source_id=h["source_id"]
                                country=h["country"]
                                category=h["category"]
                                language=h["language"]
                                print("===================================================")
                                print(self.add_News(title,link,keywords,creator, description, content, publish_date, full_description,image_url, source_id,country, category,language))
                                print("===================================================")
        def create_DB(self,db_name="news.db"):
                con=sqlite3.connect(self.db_name)
                cur=con.cursor()
                q="""
                CREATE TABLE IF NOT EXISTS news(news_id INT AUTOINCREAMENT, title TEXT NOT NULL, link TEXT NOT NULL, keywords TEXT NOT NULL,
                creator TEXT NOT NULL, description TEXT NOT NULL, content TEXT NOT NULL, publish_date TEXT NOT NULL, full_description TEXT NOT NULL,
                image_url TEXT NOT NULL, source_id TEXT NULL, country TEXT NULL, category TEXT NULL, language TEXT NULL)
                """
                cur.execute(q)
                con.commit()
                cur.close()
                con.close()
                return "ok"

        def confirm_if_news_exists(self,title,link,keywords,creator, description, content, publish_date, full_description,image_url, source_id,country, category,language):
                q="select * from news where title=? and link=? and keywords=? and creator=? and description=? and content=? and publish_date=? and full_description=? and image_url=? and source_id=? and country=? and category=? and language=?"
                c2=sqlite3.connect(self.db_name)
                cur=c2.cursor()
                cur.execute(q,(str(title),str(link),str(keywords),str(creator), str(description), str(content), str(publish_date), str(full_description),str(image_url), str(source_id),str(country), str(category),str(language)))
                res=len(cur.fetchall())
                cur.close()
                c2.close()
                return res

        def add_News(self,title,link,keywords,creator, description, content, publish_date, full_description,image_url, source_id,country, category,language):
                q="insert into news(title,link,keywords,creator, description, content, publish_date, full_description,image_url, source_id,country, category,language) values(?,?,?,?,?,?,?,?,?,?,?,?,?)"
                
                n1=news()
                rex=n1.confirm_if_news_exists(title,link,keywords,creator, description, content, publish_date, full_description,image_url, source_id,country, category,language)
                if rex <1:
                        c2=sqlite3.connect(self.db_name)
                        cur=c2.cursor()
                        cur.execute(q,(str(title),str(link),str(keywords),str(creator), str(description), str(content), str(publish_date), str(full_description),str(image_url), str(source_id),str(country), str(category),str(language)))
                        c2.commit()
                        cur.close()
                        c2.close()
                        return "created"
                else:
                        return "\n----------------------------------------\n[ "+str(rex)+" Record(s) Found] Error, the record already exists. Entry was skipped!\n----------------------------------------\n"

        def readNews(self,news_id):
                q="select * from news where news_id=?"
                c22=sqlite3.connect(self.db_name)
                c22.row_factory=sqlite3.Row
                cur=c22.cursor()
                cur.execute(q,(news_id,))
                datas=cur.fetchall()
                datax=[]
                country=[]
                image=url_for('index_page')+"static/breaking-news.PNG"
                for row in datas:
                        kwd=[]
                        if row["image_url"]=="None" or "logo" in row["image_url"]:
                                image=image
                        else:
                                image=row["image_url"]
                        try:
                                kwd=json.loads(row["keywords"])
                                country=ast.literal_eval(row["country"])
                        except Exception as e:
                                print(e)
                        datax.append({"news_id": row["news_id"],"title":row["title"],"link":row["link"],"keywords":kwd,"creator":row["creator"],"description":row["description"][0:350],"content":row["content"],"publish_date":row["publish_date"],"full_description":row["full_description"],"image_url": image,"source_id":row["source_id"],"country": country,"language":row["language"],"category":row["category"]})
                        
                cur.close()
                c22.close()
                return datax
        def readAllNews(self):
                q="select * from news order by publish_date desc"
                c22=sqlite3.connect(self.db_name)
                c22.row_factory=sqlite3.Row
                cur=c22.cursor()
                cur.execute(q)
                datas=cur.fetchall()
                datax=[]
                country=[]
                for row in datas:
                        kwd=[]
                        image=row["image_url"]
                        if row["image_url"]=="None" or "logo" in row["image_url"]:
                                image=url_for('index_page')+"static/breaking-news.PNG"
                        try:
                                kwd=json.loads(row["keywords"])
                                country=ast.literal_eval(row["country"])
                        except Exception as e:
                                print(e)
                        datax.append({"news_id": row["news_id"],"title":row["title"],"link":row["link"],"keywords":kwd,"creator":row["creator"],"description":row["description"][0:350],"content":row["content"],"publish_date":row["publish_date"],"full_description":row["full_description"],"image_url": image,"source_id":row["source_id"],"country": country,"language":row["language"],"category":row["category"]})
                        
                cur.close()
                c22.close()
                return datax
        def searchNews(self,col,value):
                q="select * from news where "+col+" like ?"
                c22=sqlite3.connect(self.db_name)
                c22.row_factory=sqlite3.Row
                cur=c22.cursor()
                d="%"+str(value)+"%"
                cur.execute(q,(d,))
                datas=cur.fetchall()
                datax=[]
                country=[]
                image=url_for('index_page')+"static/breaking-news.PNG"
                for row in datas:
                        kwd=[]
                        if row["image_url"]=="None" or "logo" in row["image_url"]:
                                image=image
                        else:
                                image=row["image_url"]
                        try:
                                kwd=json.loads(row["keywords"])
                                country=ast.literal_eval(row["country"])
                        except Exception as e:
                                print(e)
                        datax.append({"news_id": row["news_id"],"title":row["title"],"link":row["link"],"keywords":kwd,"creator":row["creator"],"description":row["description"][0:350],"content":row["content"],"publish_date":row["publish_date"],"full_description":row["full_description"],"image_url": image,"source_id":row["source_id"],"country": country,"language":row["language"],"category":row["category"]})
                        
                cur.close()
                c22.close()
                return datax

ca=news()
app=Flask(__name__)

@app.route("/")
def index_page():
    
    cats=ca.categories
    news=ca.readAllNews()
    opts=[]
    return render_template("index.html",categories=cats,news=news,opts=opts)

@app.route("/test")
def test_page():
    cats=ca.categories
    news=ca.readAllNews()
    opts=[]
    return render_template("test.html",categories=cats,news=news,opts=opts)


@app.route("/read/<nid>")
def readnews(nid):
    cats=ca.categories
    news=ca.readNews(nid)
    opts=[]
    return render_template("read.html",categories=cats,news=news,opts=opts)

@app.route("/news/<category>")
def categories(category):
    categoryname=category
    cats=ca.categories
    news=ca.searchNews("category",categoryname)
    opts=[]
    return render_template("category.html",categoryname=categoryname,categories=cats,news=news,opts=opts)


if __name__=="__main__":
    app.run(port="3030", debug=True)
        #nws=news()
        #nws.create_DB()
        #print("Warning! Called Crawl in initial file")
        #nws.get_news()
        #print(nws.error)
        #nws.save_all()

