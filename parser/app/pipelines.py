import psycopg2
import pytz
from datetime import datetime

from app import settings
from app.items import FlatItemSerializer
from app.monitoring import send_message


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
        self.pipeline.open_spider(self, spider)

    def close_spider(self, spider):
        self.pipeline.close_spider(self, spider)
        self.conn.close()

    def process_item(self, item, spider):
        self.pipeline.process_item(self, item, spider)
        return item


class BaseSpiderPipeline:
    def process_item(self, pipeline, item, spider):
        return

    def open_spider(self, pipeline, spider):
        return

    def close_spider(self, pipeline, spider):
        return


class FlatSpiderPipeline(BaseSpiderPipeline):
    name = 'flat_spider'

    def __init__(self):
        self.batch_data = []
        self.table_name = settings.FLAT_TABLE_NAME
        self.current_date = datetime.now(pytz.timezone(settings.TIMEZONE)).date()

    def flush_to_db(self, pipeline, spider):
        with pipeline.conn.cursor() as cursor:
            values = [
                (
                    item.krisha_id,
                    item.title,
                    item.url,
                    item.pub_date,
                    item.views_count,
                    item.seller_phone,
                    item.price,
                    item.rooms_count,
                    item.total_area,
                    item.ceiling_height,
                    item.region,
                    item.city,
                    item.address,
                    item.flat_floor,
                    item.longitude,
                    item.attitude,
                    item.construction_year,
                    item.floors_count,
                    item.wall_type,
                    item.seller_user_type,
                    item.description,
                    self.current_date
                )
                for item in self.batch_data
            ]
            format = ','.join(['%s'] * len(values[0]))
            values = ','.join(cursor.mogrify(f'({format})', x).decode('utf-8') for x in values)

            try:
                cursor.execute(f'INSERT INTO {self.table_name} VALUES {values}')
                pipeline.conn.commit()
            except Exception as e:
                spider.logger.error(f'{e} database error')
                pipeline.conn.rollback()
                return

            spider.logger.warning(f'loaded in database {len(self.batch_data)} flats by {getattr(spider, "part", "0")} instance')

    def process_item(self, pipeline, item, spider):
        if len(self.batch_data) < pipeline.batch_size:
            self.batch_data.append(FlatItemSerializer(item))
            return

        self.flush_to_db(pipeline, spider)
        self.batch_data = []

    def close_spider(self, pipeline, spider):
        if self.batch_data:
            self.flush_to_db(pipeline, spider)

        with pipeline.conn.cursor() as cursor:
            cursor.execute(f'SELECT COUNT(*) FROM {self.table_name} WHERE parsed_date = %s', (self.current_date,))
            flats_count = cursor.fetchone()[0]

        send_message(f'на момент завершения {spider.get_part() + 1}-го паука в таблице {self.table_name} {flats_count} квартир(ы)')

    def open_spider(self, pipeline, spider):
        send_message(f'запущен {spider.get_part() + 1}-ый паук из {spider.get_total()}')


def SpiderPipeline(spider_name):
    for PipelineClass in BaseSpiderPipeline.__subclasses__():
        if PipelineClass.name == spider_name:
            return PipelineClass()
    return BaseSpiderPipeline()
