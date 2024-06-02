import psycopg2

class Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="git_repo_data",
            user="postgres",
            host='localhost',
            password="root",
            port=5432
        )

    def get_connection(self):
        return self.conn

    def insertRepo(self, repo):
        cur=self.conn.cursor()
        cur.execute("INSERT INTO repos(repo) values('"+str(repo)+"');")
        # Make the changes to the database persistent
        self.conn.commit()
        # Close cursor and communication with the database
        cur.close()
    
    def getRepoId(self, repo):
        cur=self.conn.cursor()
        cur.execute("SELECT repo_id from repos where repo='"+str(repo)+"';")
        repoId=cur.fetchall()
        # print(repoId)
        # Make the changes to the database persistent
        self.conn.commit()
        # Close cursor and communication with the database
        cur.close()
        # return repoId[0][0] 
        if(len(repoId)==0):
            self.insertRepo(repo)
            return self.getRepoId(repo)
        else:
            return repoId[0][0]
    
    def insertClass(self, repo_id, className):
        cur=self.conn.cursor()
        cur.execute("INSERT INTO classes(repo_id, class) values("+str(repo_id)+", '"+str(className)+"');")
        # Make the changes to the database persistent
        self.conn.commit()
        # Close cursor and communication with the database
        cur.close()
    
    def getFile(self, repo_id, fileName):
        cur=self.conn.cursor()
        cur.execute("SELECT file_id from file_name where repo_id="+str(repo_id)+" and file='"+str(fileName)+"';")
        repoId=cur.fetchall()
        # print(repoId)
        # Make the changes to the database persistent
        self.conn.commit()
        # Close cursor and communication with the database
        cur.close()
        # return repoId[0][0] 
        
        return repoId[0][0]

    def insertFunctionMetadata(self, repo_id, file_id, class__name, function_name, function_code):
        try:
            cur=self.conn.cursor()
            cur.execute("INSERT INTO function_metadata(repo_id, file_id, class, function_name, code) values("+str(repo_id)+", "+str(file_id)+", '"+str(class__name)+"','"+str(function_name)+"', '"+str(function_code)+"');")
            # Make the changes to the database persistent
            self.conn.commit()
            # Close cursor and communication with the database
            cur.close()
            return 1
        except Exception as e:
            self.conn.rollback()
            cur.close()
            return 0

    def insertFile(self, repo_id, fileName):
        cur=self.conn.cursor()
        cur.execute("INSERT INTO file_name(repo_id, file) values("+str(repo_id)+", '"+str(fileName)+"');")
        # Make the changes to the database persistent
        self.conn.commit()
        # Close cursor and communication with the database
        cur.close()
        return self.getFile(repo_id, fileName)
        
    def close(self):
        if self.conn:
            self.conn.close()
