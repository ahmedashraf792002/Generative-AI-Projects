from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_PROJECT_NAME.value
        ]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[
                DataBaseEnum.COLLECTION_PROJECT_NAME.value
            ]

            indexes = Project.get_indexes()

            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_project(self, project: Project):

        result = await self.collection.insert_one(
            project.dict(by_alias=True, exclude_unset=True)
        )

        # مهم جداً
        project.id = result.inserted_id

        return project

    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:

            project = Project(
                project_id=project_id
            )

            project = await self.create_project(project)

            # للتأكد من رجوع الـ ObjectId الصحيح
            record = await self.collection.find_one(
                {"_id": project.id}
            )

            return Project(**record)

        return Project(**record)

    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        total_documents = await self.collection.count_documents({})

        total_pages = total_documents // page_size

        if total_documents % page_size:
            total_pages += 1

        cursor = (
            self.collection.find()
            .skip((page - 1) * page_size)
            .limit(page_size)
        )

        projects = []

        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_pages
    
    async def get_last_project(self):
        project = await self.collection.find_one(
            sort=[("_id", -1)]
        )
        return project