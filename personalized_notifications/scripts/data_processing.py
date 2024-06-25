from pyspark.sql import SparkSession
from starburst import Starburst

def load_and_process_data():
    spark = SparkSession.builder.appName("PersonalizedNotifications").getOrCreate()

    # Starburst ile veri çekme
    starburst = Starburst(
        host='starburst-host',
        user='username',
        password='password',
        catalog='catalog-name',
        schema='schema-name'
    )

    query = """
    SELECT customernumber, event_name, category, subcategory
    FROM countlydev.pageview_event_sg
    """
    
    df = spark.read.format("jdbc").options(
        url=starburst.get_jdbc_url(),
        dbtable=f"({query}) AS pageview_data",
        driver="io.trino.jdbc.TrinoDriver"
    ).load()

    return df

if __name__ == "__main__":
    df = load_and_process_data()
    df.show()
