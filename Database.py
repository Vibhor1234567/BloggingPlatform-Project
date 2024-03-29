import mysql.connector

conn = mysql.connector.connect(host='localhost',user='root',password='12345',port=3306)
print("connected")
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS BLOGGINGPLATFORM")

cur.execute("use BLOGGINGPLATFORM")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(250) UNIQUE NOT NULL,
            password VARCHAR(250) NOT NULL,
            email VARCHAR(250) NOT NULL)
            """)

cur.execute("""
CREATE TABLE IF NOT EXISTS posts(post_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(250) NOT NULL,
            description TEXT NOT NULL,
            author_id INT NOT NULL,
            image_url VARCHAR(250),
            publication_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(user_id)
            )
            """)

cur.execute("""
CREATE TABLE IF NOT EXISTS subscriptions(subscription_id INT AUTO_INCREMENT PRIMARY KEY,
            plan_name VARCHAR(50) NOT NULL,
            post_limit INT NOT NULL,
            expiration_period INT NOT NULL
            )
            """)

cur.execute("""
CREATE TABLE IF NOT EXISTS user_subscribed_subscription(
            user_id INT,
            subscription_id INT,
            start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
            end_date TIMESTAMP,
            PRIMARY KEY(user_id, subscription_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(subscription_id) REFERENCES subscriptions(subscription_id)
            )
            """)


cur.close()
# print(cur)


conn.commit()
conn.close()
print("cursor executed successfully")
