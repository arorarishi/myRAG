export const PROVIDERS = {
    embedding: [
        {
            name: 'OpenAI',
            models: ['text-embedding-3-small', 'text-embedding-3-large', 'text-embedding-ada-002'],
            requiresApiKey: true
        },
        {
            name: 'Cohere',
            models: ['embed-english-v3.0', 'embed-multilingual-v3.0'],
            requiresApiKey: true
        },
        {
            name: 'HuggingFace',
            models: ['sentence-transformers/all-MiniLM-L6-v2', 'BAAI/bge-small-en-v1.5'],
            requiresApiKey: false
        },
        {
            name: 'Voyage AI',
            models: ['voyage-2', 'voyage-large-2'],
            requiresApiKey: true
        },
        {
            name: 'DeepInfra',
            models: ['BAAI/bge-base-en-v1.5', 'sentence-transformers/all-MiniLM-L6-v2'],
            requiresApiKey: true
        }
    ],
    reranking: [
        {
            name: 'Cohere',
            models: ['rerank-english-v3.0', 'rerank-multilingual-v3.0'],
            requiresApiKey: true
        },
        {
            name: 'Jina AI',
            models: ['jina-reranker-v1-base-en', 'jina-reranker-v2-base-multilingual'],
            requiresApiKey: true
        },
        {
            name: 'DeepInfra',
            models: ['BAAI/bge-reranker-v2-m3', 'mixedbread-ai/mxbai-rerank-large-v1'],
            requiresApiKey: true
        },
        {
            name: 'Local',
            models: ['cross-encoder/ms-marco-MiniLM-L-12-v2'],
            requiresApiKey: false
        }
    ],
    llm: [
        {
            name: 'OpenAI',
            models: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'],
            requiresApiKey: true
        },
        {
            name: 'Anthropic',
            models: ['claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022'],
            requiresApiKey: true
        },
        {
            name: 'DeepInfra',
            models: ['meta-llama/Meta-Llama-3.1-70B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1'],
            requiresApiKey: true
        },
        {
            name: 'Groq',
            models: ['llama-3.1-70b-versatile', 'mixtral-8x7b-32768'],
            requiresApiKey: true
        }
    ]
};
