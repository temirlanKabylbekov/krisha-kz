import psycopg2


class DatabasePipeline:
    def __init__(self, db_host, db_port, db_user, db_password, db_name, batch_size):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

        self.batch_size = batch_size

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host=crawler.settings.get('DB_HOST'),
            db_port=crawler.settings.get('DB_PORT'),
            db_user=crawler.settings.get('DB_USER'),
            db_password=crawler.settings.get('DB_PASSWORD'),
            db_name=crawler.settings.get('DB_NAME'),
            batch_size=crawler.settings.getint('DB_BATCH_SIZE')
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(dbname=self.db_name, user=self.db_user, password=self.db_password, host=self.db_host)
        self.pipeline = SpiderPipeline(spider.name)

    def close_spider(self, spider):
        self.pipeline.close_spider(self, spider)
        self.conn.close()

    def process_item(self, item, spider):
        self.pipeline.process_item(self, item, spider)
        return item


class BaseSpiderPipeline:
    def process_item(self, pipeline, item, spider):
        return

    def close_spider(self, pipeline, spider):
        return


class FlatSpiderPipeline(BaseSpiderPipeline):
    name = 'flat_spider'

    def __init__(self):
        self.batch_data = []

    def flush_to_db(self, pipeline, spider):
        with pipeline.conn.cursor() as cursor:
            values = ','.join([
                str(
                    (
                        item.serialized_title,
                        item.serialized_url,
                        item.serialized_price
                    )
                )
                for item in self.batch_data
            ])
            cursor.execute(f'INSERT INTO flats(title, url, price) VALUES {values}')
            pipeline.conn.commit()

            spider.logger.info(f'loaded in database {len(self.batch_data)} flats by {getattr(spider, "part", "0")} instance')

    def process_item(self, pipeline, item, spider):
        if len(self.batch_data) < pipeline.batch_size:
            self.batch_data.append(item)
            return

        self.flush_to_db(pipeline, spider)
        self.batch_data = []

    def close_spider(self, pipeline, spider):
        if self.batch_data:
            self.flush_to_db(pipeline, spider)


def SpiderPipeline(spider_name):
    for PipelineClass in BaseSpiderPipeline.__subclasses__():
        if PipelineClass.name == spider_name:
            return PipelineClass()
    return BaseSpiderPipeline()
