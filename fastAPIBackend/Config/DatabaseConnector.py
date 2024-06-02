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
    def close(self):
        if self.conn:
            self.conn.close()
