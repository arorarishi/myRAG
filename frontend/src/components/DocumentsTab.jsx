import { useState, useEffect } from 'react';
import { uploadPDF, getDocuments, deleteDocument } from '../services/api';
import './DocumentsTab.css';

function DocumentsTab({ vectorDb, metadataDb }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState('');
    const [documents, setDocuments] = useState([]);
    const [loadingDocs, setLoadingDocs] = useState(true);

    useEffect(() => {
        loadDocuments();
    }, []);

    const loadDocuments = async () => {
        try {
            setLoadingDocs(true);
            const docs = await getDocuments();
            setDocuments(docs);
        } catch (error) {
            console.error('Failed to load documents:', error);
        } finally {
            setLoadingDocs(false);
        }
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setUploadStatus('');
    };

    const handleUpload = async () => {
        if (!file) return;

        setLoading(true);
        setUploadStatus('Uploading and processing...');
        try {
            const result = await uploadPDF(file);
            setUploadStatus(`✓ ${result.message} (${result.num_chunks} chunks)`);
            setFile(null);
            // Reload documents list
            await loadDocuments();
        } catch (err) {
            const errorMessage = err.response?.data?.detail || err.message || 'Failed to process document';
            setUploadStatus(`✗ ${errorMessage}`);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (docId) => {
        if (!confirm('Are you sure you want to delete this document?')) return;

        try {
            await deleteDocument(docId);
            alert('Document deleted successfully');
            await loadDocuments();
        } catch (error) {
            console.error('Delete error:', error);
            const errorMessage = error.response?.data?.detail || error.message || 'Failed to delete document';
            alert(`Failed to delete document: ${errorMessage}`);
        }
    };

    const getStatusBadge = (status) => {
        const badges = {
            completed: { class: 'status-completed', text: 'Completed' },
            processing: { class: 'status-processing', text: 'Processing' },
            failed: { class: 'status-failed', text: 'Failed' }
        };
        return badges[status] || badges.processing;
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };

    return (
        <div className="documents-container">
            <div className="chat-header">
                <h2>Document Management</h2>
                <p>Upload and manage your documents</p>
            </div>

            <div className="upload-section">
                <div className="upload-area">
                    <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileChange}
                        id="file-upload"
                        style={{ display: 'none' }}
                    />
                    <label htmlFor="file-upload" className="upload-label">
                        {file ? file.name : 'Choose PDF File'}
                    </label>
                    <button
                        onClick={handleUpload}
                        disabled={!file || loading}
                        className="upload-btn-secondary"
                    >
                        {loading ? 'Processing...' : 'Upload & Index'}
                    </button>
                </div>

                {uploadStatus && (
                    <div className={`upload-status ${uploadStatus.startsWith('✗') ? 'error' : 'success'}`}>
                        {uploadStatus}
                    </div>
                )}

                <div className="db-info-box">
                    <div>Vector DB: <strong>{vectorDb}</strong></div>
                    <div>Metadata DB: <strong>{metadataDb}</strong></div>
                </div>
            </div>

            <div className="documents-list">
                <h3>Indexed Documents ({documents.length})</h3>

                {loadingDocs ? (
                    <p className="loading-text">Loading documents...</p>
                ) : documents.length === 0 ? (
                    <p className="empty-text">No documents uploaded yet. Upload a PDF to get started!</p>
                ) : (
                    <div className="documents-table-wrapper">
                        <table className="documents-table">
                            <thead>
                                <tr>
                                    <th>Filename</th>
                                    <th>Upload Date</th>
                                    <th>Chunks</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {documents.map((doc) => {
                                    const badge = getStatusBadge(doc.status);
                                    return (
                                        <tr key={doc.id}>
                                            <td className="filename-cell">
                                                <div className="filename">{doc.filename}</div>
                                                {doc.error_message && (
                                                    <div className="error-message-inline">
                                                        ⚠️ {doc.error_message}
                                                    </div>
                                                )}
                                            </td>
                                            <td>{formatDate(doc.upload_date)}</td>
                                            <td className="center-cell">{doc.num_chunks}</td>
                                            <td>
                                                <span className={`status-badge ${badge.class}`}>
                                                    {badge.text}
                                                </span>
                                            </td>
                                            <td className="actions-cell">
                                                <button
                                                    className="delete-btn"
                                                    onClick={() => handleDelete(doc.id)}
                                                    title="Delete document"
                                                >
                                                    🗑️ Delete
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

export default DocumentsTab;
