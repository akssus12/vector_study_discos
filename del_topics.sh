# delete topic for fair experiment
~/your_kafka_source/bin/kafka-topics.sh --delete --bootstrap-server ip_address:9092 --topic as_you_wish_topic

# create topic for fair experiment
~/your_kafka_source/bin/kafka-topics.sh --create --bootstrap-server ip_address:9092 replication-factor 1 --partitions 1 --topic as_you_wish_topic

