from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, File

class StandartOutput(BaseModel):
    message: str


class Ingredientes(BaseModel):
    ingrediente: str

class Fotos(BaseModel):
    fotos: str

class ReceitaBasica(BaseModel):
    titulo: str
    instrucoes: str
    ingredientes: List[Ingredientes]

class BuscaTitulo(BaseModel):
    titulo: str
