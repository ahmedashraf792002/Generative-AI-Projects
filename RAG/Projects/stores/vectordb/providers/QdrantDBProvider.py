from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
from models.db_schemes.data_chunk import RetrievedDocument
import logging
from typing import List
import uuid


class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str):

        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT
        else:
            self.distance_method = models.Distance.COSINE

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> List:
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str):
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)

    def create_collection(
        self,
        collection_name: str,
        embedding_size: int,
        do_reset: bool = False,
    ):
        if do_reset:
            self.delete_collection(collection_name)

        if not self.is_collection_existed(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method,
                ),
            )
            return True

        return False

    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict =None,
        record_id=None,
    ):

        if not self.is_collection_existed(collection_name):
            self.logger.error(
                f"Collection '{collection_name}' does not exist."
            )
            return False

        if record_id is None:
            record_id = str(uuid.uuid4())

        try:
            self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=record_id,
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata,
                        },
                    )
                ],
            )

        except Exception as e:
            self.logger.exception(e)
            return False

        return True

    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list =None,
        record_ids: list =None,
        batch_size: int = 50,
    ):

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = [str(uuid.uuid4()) for _ in texts]

        for i in range(0, len(texts), batch_size):

            batch_texts = texts[i:i + batch_size]
            batch_vectors = vectors[i:i + batch_size]
            batch_metadata = metadata[i:i + batch_size]
            batch_ids = record_ids[i:i + batch_size]

            points = []

            for text, vector, meta, point_id in zip(
                batch_texts,
                batch_vectors,
                batch_metadata,
                batch_ids,
            ):

                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": meta,
                        },
                    )
                )

            try:
                self.client.upsert(
                    collection_name=collection_name,
                    points=points,
                )

            except Exception as e:
                self.logger.exception(e)
                return False

        return True

    

    def search_by_vector(
        self,
        collection_name: str,
        vector: list,
        limit: int = 5,
    ):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
        )

        return [
            RetrievedDocument(
                text=result.payload.get("text", ""),
                score=result.score,
                metadata=result.payload.get("metadata", {}),
            )
            for result in results
        ]