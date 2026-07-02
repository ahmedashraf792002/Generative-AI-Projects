from .BaseController import BaseController
from .ProjectController import ProjectController
import os

from langchain_community.document_loaders import (
    TextLoader,
    PyMuPDFLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum


class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(
            project_id=project_id
        )

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1].lower()

    def get_file_loader(self, file_id: str):

        file_ext = self.get_file_extension(file_id=file_id)

        file_path = os.path.join(
            self.project_path,
            file_id
        )

        loaders = {
            ProcessingEnum.TXT.value: lambda: TextLoader(
                file_path,
                encoding="utf-8"
            ),

            ProcessingEnum.PDF.value: lambda: PyMuPDFLoader(
                file_path
            ),

            ProcessingEnum.DOCX.value: lambda: UnstructuredWordDocumentLoader(
                file_path
            ),

            ProcessingEnum.CSV.value: lambda: CSVLoader(
                file_path
            ),

            ProcessingEnum.XLSX.value: lambda: UnstructuredExcelLoader(
                file_path
            )
        }

        loader_factory = loaders.get(file_ext)

        if loader_factory is None:
            raise ValueError(
                f"Unsupported file extension: {file_ext}"
            )

        return loader_factory()

    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id=file_id)

        return loader.load()

    def process_file_content(
        self,
        file_content: list,
        file_id: str,
        chunk_size: int = 100,
        overlap_size: int = 20
    ):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            {
                **rec.metadata,
                "file_id": file_id
            }
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks