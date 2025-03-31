# 1. BEIR dataset(hotpotqa, nq, fever)를 임베딩한 파일 다운로드 및 압축해체
wget https://discos.sogang.ac.kr/file/data/beir_embeddings.tar

### 임베딩에 사용한 모델과 각 데이터셋의 수는 아래와 같습니다. 해당 임베딩 파일을 이용하여 각자 실험에 사용하는 벡터 데이터베이스, 인덱싱 알고리즘에 맞게 인덱싱을 해주세요.
Embedding model - all-MiniLM-L6-v2 (384 dimensions)
Total number of vector embeddings - hotpotqa(5233329), fever(5416568), nq(2681468)

# 2. 실험 쿼리에 사용할 파일 다운로드 및 압축 해제
wget https://discos.sogang.ac.kr/file/data/parquet.tar

# 3. Apache Kafka 세팅
세팅방법 - https://jongsky.tistory.com/89   # kafka version은 어떤 것을 써도 무관하나, 본인의 운영체제 버전에 맞는 것을 찾아서 사용해주세요.

# 4-1. query_traffic.py 에 실험 파라미터를 자신의 환경에 맞게 수정
query_traffic.py 파일에 "as_you_wish_name" 수정, main 문 안에 어떤 트래픽으로 쿼리를 생성할 지 파라미터 조정.
현재 세팅되어 있는 트래픽 분포는 1분마다 3개의 세트로 발생됨. 1 set(5000개 query, 10초), 2 set(3000개 query, 20초), 3 set(2000개 query, 30초) 
1 set로 인해 burst한 트래픽이 짧은 시간에 들어오는 것을 재현할 수 있음.

# 4-2. 실험의 공정성을 위해 매 실험에 앞서 토픽 삭제/재생성하는 스크립트 실행
sh del_topics.sh

# 4-3. 각자 세팅한 벡터데이터베이스의 api를 활용한 프로그램으로 search 실행
  - 민동현 연구원이 commit한 milvus search 참고 (https://github.com/lass-lab/fluffy-moti)
  - faiss를 사용하고자 한다면, https://github.com/akssus12/CaGR_RAG 참고
  - chromaDB를 사용하고자 한다면, https://github.com/akssus12/vector_spark 참고

# 5. 실험에 사용되는 쿼리 변경을 원한다면..
현재 쿼리는 wikipedia question dataset으로 세팅되어 있음. 단순 vector search의 성능 측정을 위한다면, 굳이 고칠 필요 없지만, 혹시 paper에 들어가는 실험에 사용한다고 한다면,
https://github.com/beir-cellar/beir에서 해당 데이터셋(hotpotqa, fever, nq)를 다운로드 받아 queries.corpus를 파싱하여 Kafka topic에 전송하도록 소스를 수정해야함.
