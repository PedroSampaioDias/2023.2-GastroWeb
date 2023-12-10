import { api } from 'src/boot/axios'

export const createRecipe = async (body) => {
  return api.post('/criar_receitas', body)
}

export const listAllRecipe = async () =>
  api.get('/get_all_receitas')

export const searchByName = async ( params ) => {
  return api.get('/busca_por_titulo', { params })
}

export const searchByTagCategory = async ( {tag, categoria} ) => {
  const params = {
    tag,
    categoria
  }
  return api.get('/busca_categoria_e_tag', { params })
}

export const searchById = async ( params ) => {
  return api.get('/get_receita_por_id', { params })
}



