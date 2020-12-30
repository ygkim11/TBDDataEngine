import os
import sys

if len(sys.argv) == 1:
    raise Exception('please provide topic name')
else:
    topic_name = sys.argv[1]
    kafka_path = 'C:\\Users\\simpl\\kafka_2.13-2.7.0\\kafka\\bin\\windows'
    topic_cmd = f"""
    {kafka_path}\\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic {topic_name}
    """
    os.system(topic_cmd)