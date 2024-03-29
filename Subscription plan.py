from datetime import datetime, timedelta

# Define subscription plans with expiration dates
subscription_plans = {
    'basic': {
        'post_limit': 5,
        'expiration_period': timedelta(days=10)
    },
    'premium': {
        'post_limit': 10,
        'expiration_period': timedelta(days=10)
    }
}

basic_plan_details = subscription_plans['basic']
print(basic_plan_details)
# Output: {'post_limit': 5, 'expiration_period': timedelta(days=10)}

# Access individual details
basic_post_limit = basic_plan_details['post_limit']
basic_expiration_period = basic_plan_details['expiration_period']
print(basic_post_limit)  # Output: 5
print(basic_expiration_period)  # Output: 10 days, 0:00:00


# Function to check if a user has reached their post limit for the subscription
def has_reached_post_limit(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to count the number of posts by the user
    cursor.execute("SELECT COUNT(*) FROM posts WHERE author_id = %s", (user_id,))
    post_count = cursor.fetchone()[0]

    conn.close()

    # Get the user's subscription plan
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT s.post_limit FROM subscriptions s
    INNER JOIN user_subscribed_subscription uss ON s.subscription_id = uss.subscription_id
    WHERE uss.user_id = %s AND uss.end_date > NOW()
    """, (user_id,))
    post_limit = cursor.fetchone()

    conn.close()

    if post_limit:
        return post_count >= post_limit[0]
    else:
        return True  # No active subscription or subscription plan does not define a post limit, restrict posting


# Function to check if a user has an active subscription
def has_active_subscription(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to check if the user has an active subscription
    cursor.execute("""
    SELECT * FROM user_subscribed_subscription
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))
    active_subscription = cursor.fetchone()

    conn.close()

    return active_subscription is not None

# Function to check if a user has reached their post limit for the subscription
def has_reached_post_limit(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to count the number of posts by the user
    cursor.execute("SELECT COUNT(*) FROM posts WHERE author_id = %s", (user_id,))
    post_count = cursor.fetchone()[0]

    conn.close()

    # Get the user's subscription plan
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subscription_id FROM user_subscribed_subscription
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))
    subscription_id = cursor.fetchone()

    if subscription_id:
        cursor.execute("""
        SELECT post_limit FROM subscriptions
        WHERE subscription_id = %s
        """, (subscription_id,))
        post_limit = cursor.fetchone()[0]

        return post_count >= post_limit
    else:
        return True  # No active subscription, restrict posting

    conn.close()

# Example usage:
def post_blog(user_id, title, description):
    if has_active_subscription(user_id) and not has_reached_post_limit(user_id):
        # Allow posting
        # Insert the blog post into the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, description, author_id) VALUES (%s, %s, %s)", (title, description, user_id))
        conn.commit()
        conn.close()
        return "Blog posted successfully!"
    else:
        return "You have reached your post limit or your subscription has expired. Please purchase a new subscription."

# Example usage
user_id = 1  # Assuming the user ID
title = "My First Blog Post"
description = "This is the content of my first blog post."

print(post_blog(user_id, title, description))



# Function to purchase a new subscription plan
def purchase_subscription(user_id, plan_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get the subscription details based on the plan name
    cursor.execute("SELECT * FROM subscriptions WHERE plan_name = %s", (plan_name,))
    subscription_details = cursor.fetchone()
    if subscription_details is None:
        conn.close()
        return "Invalid subscription plan."

    subscription_id = subscription_details[0]
    post_limit = subscription_details[2]
    expiration_period = subscription_details[3]

    # Mark previous subscriptions as expired
    cursor.execute("""
    UPDATE user_subscribed_subscription
    SET end_date = NOW()
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))

    # Insert new subscription into user_subscribed_subscription table
    start_date = datetime.now()
    end_date = start_date + expiration_period
    cursor.execute("""
    INSERT INTO user_subscribed_subscription (user_id, subscription_id, start_date, end_date)
    VALUES (%s, %s, %s, %s)
    """, (user_id, subscription_id, start_date, end_date))

    conn.commit()
    conn.close()

    return "Subscription purchased successfully!"

# Example usage:
user_id = 1  # Assuming the user ID
plan_name = "premium"  # Plan name to purchase

print(purchase_subscription(user_id, plan_name))