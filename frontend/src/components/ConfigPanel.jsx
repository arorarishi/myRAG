import { useState, useEffect } from 'react';
import { PROVIDERS } from '../constants/providers';
import { saveConfiguration, getConfiguration } from '../services/api';
import './ConfigPanel.css';

function ConfigPanel() {
    const [config, setConfig] = useState({
        // Database
        database: 'sqlite',
        postgresUrl: '',

        // Vector Store
        vectorStore: 'faiss',
        pgvectorUrl: '',

        // Document Source
        documentSource: 'local',
        sharepointSite: '',
        sharepointUsername: '',
        sharepointPassword: '',

        // Embedding
        embeddingProvider: 'OpenAI',
        embeddingModel: 'text-embedding-3-small',
        embeddingApiKey: '',

        // Reranking
        rerankingProvider: 'Cohere',
        rerankingModel: 'rerank-english-v3.0',
        rerankingApiKey: '',

        // LLM
        llmProvider: 'OpenAI',
        llmModel: 'gpt-4o-mini',
        llmApiKey: ''
    });

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    // Load configuration on mount
    useEffect(() => {
        const loadConfig = async () => {
            try {
                const savedConfig = await getConfiguration();
                if (savedConfig) {
                    setConfig({
                        database: savedConfig.database,
                        postgresUrl: savedConfig.postgres_url || '',
                        vectorStore: savedConfig.vector_store,
                        pgvectorUrl: savedConfig.pgvector_url || '',
                        documentSource: savedConfig.document_source,
                        sharepointSite: savedConfig.sharepoint_site || '',
                        sharepointUsername: savedConfig.sharepoint_username || '',
                        sharepointPassword: savedConfig.sharepoint_password || '',
                        embeddingProvider: savedConfig.embedding_provider,
                        embeddingModel: savedConfig.embedding_model,
                        embeddingApiKey: savedConfig.embedding_api_key || '',
                        rerankingProvider: savedConfig.reranking_provider,
                        rerankingModel: savedConfig.reranking_model,
                        rerankingApiKey: savedConfig.reranking_api_key || '',
                        llmProvider: savedConfig.llm_provider,
                        llmModel: savedConfig.llm_model,
                        llmApiKey: savedConfig.llm_api_key || ''
                    });
                }
            } catch (error) {
                console.error('Failed to load configuration:', error);
            }
        };
        loadConfig();
    }, []);

    const handleProviderChange = (type, provider) => {
        const providerData = PROVIDERS[type].find(p => p.name === provider);
        const defaultModel = providerData?.models[0] || '';

        setConfig({
            ...config,
            [`${type}Provider`]: provider,
            [`${type}Model`]: defaultModel
        });
    };

    const handleSave = async () => {
        setLoading(true);
        setMessage('');
        try {
            await saveConfiguration(config);
            setMessage('Configuration saved successfully!');
            setTimeout(() => setMessage(''), 3000);
        } catch (error) {
            setMessage('Failed to save configuration');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="config-panel">
            <h2>RAG Configuration</h2>

            {/* Database Configuration */}
            <section className="config-section">
                <h3>Database Configuration</h3>
                <div className="radio-group">
                    <label>
                        <input
                            type="radio"
                            value="sqlite"
                            checked={config.database === 'sqlite'}
                            onChange={(e) => setConfig({ ...config, database: e.target.value })}
                        />
                        SQLite (Local)
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="postgresql"
                            checked={config.database === 'postgresql'}
                            onChange={(e) => setConfig({ ...config, database: e.target.value })}
                        />
                        PostgreSQL
                    </label>
                </div>

                {config.database === 'postgresql' && (
                    <input
                        type="text"
                        placeholder="postgresql://user:password@localhost:5432/dbname"
                        value={config.postgresUrl}
                        onChange={(e) => setConfig({ ...config, postgresUrl: e.target.value })}
                        className="full-width"
                    />
                )}
            </section>

            {/* Vector Store Configuration */}
            <section className="config-section">
                <h3>Vector Database</h3>
                <div className="radio-group">
                    <label>
                        <input
                            type="radio"
                            value="faiss"
                            checked={config.vectorStore === 'faiss'}
                            onChange={(e) => setConfig({ ...config, vectorStore: e.target.value })}
                        />
                        FAISS (Persistent)
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="pgvector"
                            checked={config.vectorStore === 'pgvector'}
                            onChange={(e) => setConfig({ ...config, vectorStore: e.target.value })}
                        />
                        PostgreSQL pgvector
                    </label>
                </div>

                {config.vectorStore === 'pgvector' && (
                    <input
                        type="text"
                        placeholder="postgresql://user:password@localhost:5432/vectordb"
                        value={config.pgvectorUrl}
                        onChange={(e) => setConfig({ ...config, pgvectorUrl: e.target.value })}
                        className="full-width"
                    />
                )}
            </section>

            {/* Embedding Model */}
            <section className="config-section">
                <h3>Embedding Model</h3>
                <div className="provider-config">
                    <select
                        value={config.embeddingProvider}
                        onChange={(e) => handleProviderChange('embedding', e.target.value)}
                    >
                        {PROVIDERS.embedding.map(p => (
                            <option key={p.name} value={p.name}>{p.name}</option>
                        ))}
                    </select>

                    <input
                        type="text"
                        placeholder="Model name"
                        value={config.embeddingModel}
                        onChange={(e) => setConfig({ ...config, embeddingModel: e.target.value })}
                    />

                    {PROVIDERS.embedding.find(p => p.name === config.embeddingProvider)?.requiresApiKey && (
                        <input
                            type="password"
                            placeholder="API Key"
                            value={config.embeddingApiKey}
                            onChange={(e) => setConfig({ ...config, embeddingApiKey: e.target.value })}
                        />
                    )}
                </div>
                <div className="model-suggestions">
                    Recommended: {PROVIDERS.embedding.find(p => p.name === config.embeddingProvider)?.models.join(', ')}
                </div>
            </section>

            {/* Reranking Model */}
            <section className="config-section">
                <h3>ReRanking Model</h3>
                <div className="provider-config">
                    <select
                        value={config.rerankingProvider}
                        onChange={(e) => handleProviderChange('reranking', e.target.value)}
                    >
                        {PROVIDERS.reranking.map(p => (
                            <option key={p.name} value={p.name}>{p.name}</option>
                        ))}
                    </select>

                    <input
                        type="text"
                        placeholder="Model name"
                        value={config.rerankingModel}
                        onChange={(e) => setConfig({ ...config, rerankingModel: e.target.value })}
                    />

                    {PROVIDERS.reranking.find(p => p.name === config.rerankingProvider)?.requiresApiKey && (
                        <input
                            type="password"
                            placeholder="API Key"
                            value={config.rerankingApiKey}
                            onChange={(e) => setConfig({ ...config, rerankingApiKey: e.target.value })}
                        />
                    )}
                </div>
                <div className="model-suggestions">
                    Recommended: {PROVIDERS.reranking.find(p => p.name === config.rerankingProvider)?.models.join(', ')}
                </div>
            </section>

            {/* LLM Model */}
            <section className="config-section">
                <h3>LLM Model</h3>
                <div className="provider-config">
                    <select
                        value={config.llmProvider}
                        onChange={(e) => handleProviderChange('llm', e.target.value)}
                    >
                        {PROVIDERS.llm.map(p => (
                            <option key={p.name} value={p.name}>{p.name}</option>
                        ))}
                    </select>

                    <input
                        type="text"
                        placeholder="Model name"
                        value={config.llmModel}
                        onChange={(e) => setConfig({ ...config, llmModel: e.target.value })}
                    />

                    {PROVIDERS.llm.find(p => p.name === config.llmProvider)?.requiresApiKey && (
                        <input
                            type="password"
                            placeholder="API Key"
                            value={config.llmApiKey}
                            onChange={(e) => setConfig({ ...config, llmApiKey: e.target.value })}
                        />
                    )}
                </div>
                <div className="model-suggestions">
                    Recommended: {PROVIDERS.llm.find(p => p.name === config.llmProvider)?.models.join(', ')}
                </div>
            </section>

            {/* Document Source */}
            <section className="config-section">
                <h3>Document Source</h3>
                <div className="radio-group">
                    <label>
                        <input
                            type="radio"
                            value="local"
                            checked={config.documentSource === 'local'}
                            onChange={(e) => setConfig({ ...config, documentSource: e.target.value })}
                        />
                        Local Files
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="sharepoint"
                            checked={config.documentSource === 'sharepoint'}
                            onChange={(e) => setConfig({ ...config, documentSource: e.target.value })}
                        />
                        SharePoint
                    </label>
                </div>

                {config.documentSource === 'sharepoint' && (
                    <div className="sharepoint-config">
                        <input
                            type="text"
                            placeholder="SharePoint Site URL"
                            value={config.sharepointSite}
                            onChange={(e) => setConfig({ ...config, sharepointSite: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Username"
                            value={config.sharepointUsername}
                            onChange={(e) => setConfig({ ...config, sharepointUsername: e.target.value })}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={config.sharepointPassword}
                            onChange={(e) => setConfig({ ...config, sharepointPassword: e.target.value })}
                        />
                    </div>
                )}
            </section>

            {message && <div className="status-message">{message}</div>}

            <button className="save-btn" onClick={handleSave} disabled={loading}>
                {loading ? 'Saving...' : 'Save Configuration'}
            </button>
        </div>
    );
}

export default ConfigPanel;
