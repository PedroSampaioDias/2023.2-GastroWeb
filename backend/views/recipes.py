from fastapi import  APIRouter, Request, UploadFile, File, HTTPException, Query, Form
from fastapi.responses import JSONResponse
from schemas.models import ReceitaBasica, Ingredientes
from database.connection import async_session
from database.models import Receitas, Fotos, Ingrediente
from sqlalchemy import select, join
import os
from typing import List
import json

recipes = APIRouter()

 
@recipes.post("/criarReceitas")
async def criar_receita( 
    titulo: str = Form(...),
    instrucoes: str = Form(...),
    ingredientes: List[str] = Form(...),
    files: List[UploadFile] = File(...)
):
    async with async_session() as sessao:
        try:
            nova_receita = Receitas(
                titulo=titulo,
                instrucoes=instrucoes
            )
          
            sessao.add(nova_receita)

            for ingrediente in ingredientes:
                novo_ingrediente = Ingrediente(
                    ingrediente=ingrediente,
                    receita=nova_receita
                )
                sessao.add(novo_ingrediente)

            os.makedirs("uploads", exist_ok=True)

            file_paths = []

            for file in files:
                file_path = os.path.join("uploads", file.filename)
                with open(file_path, "wb") as image_file:
                    image_file.write(file.file.read())
                file_paths.append(file_path)

            for file_path in file_paths:
                nova_foto = Fotos(
                    foto=file_path,
                    receita=nova_receita
                    )
                sessao.add(nova_foto)

            await sessao.commit()
            return { "message" : "receita adicionada com sucesso!"}
        except Exception as e:
            return{"error": str(e)}

        

@recipes.post("/fotos")
async def postar_fotos(id_receita:int, files: List[UploadFile] = File(...)):

    async with async_session() as sessao:
        try:
            os.makedirs("uploads", exist_ok=True)

            # Lista para armazenar os caminhos dos arquivos
            file_paths = []

            for file in files:
                file_path = os.path.join("uploads", file.filename)
                with open(file_path, "wb") as image_file:
                    image_file.write(file.file.read())
                file_paths.append(file_path)

            # Salvar os caminhos dos arquivos no banco de dados
            for file_path in file_paths:
                new_photo = Fotos(
                    foto=file_path,
                    id_receita=id_receita
                    )
                sessao.add(new_photo)

            await sessao.commit()

            return {"message": "Files uploaded successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@recipes.get("/getfotos")
async def read_photos():
    async with async_session() as session:
        result = await session.execute(select(Fotos))
        photos = result.scalars().all()

    return photos


@recipes.get("/getreceitas")
async def busca_titulo():
    async with async_session() as sessao:

        result = await sessao.execute(select(Receitas))
        busca = result.scalars().all()
    
    return busca

@recipes.get("/buscareceitas")
async def busca_titulo(titulo: str = Query(..., title="Title to search")):
    async with async_session() as sessao:
        
        query = select(Receitas).where(Receitas.titulo.ilike(f"%{titulo}%"))
        result = await sessao.execute(query)
        busca = result.scalars().all()

    return busca



@recipes.get("/obter_fotos_por_receita")
async def obter_fotos_por_receita(receita_id: int):
    async with async_session() as sessao:
        try:
            stmt = (
                select(Fotos)
                .select_from(join(Receitas, Fotos, Receitas.id == Fotos.id_receita))
                .where(Receitas.id == receita_id)
            )
            result = await sessao.execute(stmt)
            fotos = result.scalars().all()
            return fotos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

@recipes.get("/listar_ingredientes")
async def listar_ingredientes(receita_id: int):
    async with async_session() as sessao:
        stmt = (
            select(Ingrediente)
            .join(Receitas)
            .filter(Receitas.id == receita_id)
        )
        result = await sessao.execute(stmt)
        ingredientes = result.scalars().all()

        return ingredientes