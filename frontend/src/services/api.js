import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${API_URL}/ingest`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};

export const saveConfiguration = async (config) => {
  try {
    // Convert frontend config object to backend format
    const configs = {
      database: config.database,
      postgres_url: config.postgresUrl || null,
      vector_store: config.vectorStore,
      pgvector_url: config.pgvectorUrl || null,
      document_source: config.documentSource,
      sharepoint_site: config.sharepointSite || null,
      sharepoint_username: config.sharepointUsername || null,
      sharepoint_password: config.sharepointPassword || null,
      embedding_provider: config.embeddingProvider,
      embedding_model: config.embeddingModel,
      embedding_api_key: config.embeddingApiKey || null,
      reranking_provider: config.rerankingProvider,
      reranking_model: config.rerankingModel,
      reranking_api_key: config.rerankingApiKey || null,
      llm_provider: config.llmProvider,
      llm_model: config.llmModel,
      llm_api_key: config.llmApiKey || null
    };

    const response = await axios.post(`${API_URL}/config`, { configs });
    return response.data;
  } catch (error) {
    console.error('Error saving configuration:', error);
    throw error;
  }
};

export const getConfiguration = async () => {
  try {
    const response = await axios.get(`${API_URL}/config`);

    // Convert backend format to frontend format
    const configs = response.data.configs;

    return {
      database: configs.database || 'sqlite',
      postgres_url: configs.postgres_url,
      vector_store: configs.vector_store || 'faiss',
      pgvector_url: configs.pgvector_url,
      document_source: configs.document_source || 'local',
      sharepoint_site: configs.sharepoint_site,
      sharepoint_username: configs.sharepoint_username,
      sharepoint_password: configs.sharepoint_password,
      embedding_provider: configs.embedding_provider || 'OpenAI',
      embedding_model: configs.embedding_model || 'text-embedding-3-small',
      embedding_api_key: configs.embedding_api_key,
      reranking_provider: configs.reranking_provider || 'Cohere',
      reranking_model: configs.reranking_model || 'rerank-english-v3.0',
      reranking_api_key: configs.reranking_api_key,
      llm_provider: configs.llm_provider || 'OpenAI',
      llm_model: configs.llm_model || 'gpt-4o-mini',
      llm_api_key: configs.llm_api_key
    };
  } catch (error) {
    if (error.response?.status === 404 || !error.response) {
      // No configuration exists yet, return null
      return null;
    }
    console.error('Error getting configuration:', error);
    throw error;
  }
};

export const getDocuments = async () => {
  try {
    const response = await axios.get(`${API_URL}/documents`);
    return response.data;
  } catch (error) {
    console.error('Error getting documents:', error);
    throw error;
  }
};

export const deleteDocument = async (documentId) => {
  try {
    const response = await axios.delete(`${API_URL}/documents/${documentId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting document:', error);
    throw error;
  }
};
