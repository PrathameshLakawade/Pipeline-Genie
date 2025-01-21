import React, { useEffect, useRef, useState } from 'react';
import { Toast } from 'primereact/toast';

export default function MetaData({ fileName, onSuccess }) {
    const toast = useRef(null);
    const [metadata, setMetadata] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchMetaData() {
            try {
                const response = await fetch(`http://localhost:8000/data-pipeline/metadata/${fileName}`, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const result = await response.json();

                    setMetadata(result.metadata);
                    toast.current.show({
                        severity: 'success',
                        summary: 'Success',
                        detail: result.message || 'Successfully fetched metadata!',
                    });
                    if (onSuccess) onSuccess(result);
                } else {
                    const errorMessage = await response.text();
                    setError(errorMessage);
                    toast.current.show({
                        severity: 'error',
                        summary: 'Error',
                        detail: 'Failed to fetch metadata',
                    });
                }
            } catch (error) {
                console.error('Fetch error:', error);
                setError('An error occurred while fetching metadata');
                toast.current.show({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'An error occurred while fetching metadata',
                });
            }
        }

        if (fileName) {
            fetchMetaData();
        }
    }, [fileName, onSuccess]);

    return (
        <div>
            <h3>Data Summary</h3>
            <Toast ref={toast} />
            
            {/* Show loading message */}
            {!metadata && !error && <p>Loading metadata...</p>}
            
            {/* Show metadata if available */}
            {metadata && (
                <div>
                    <h4>Metadata</h4>
                    <p><strong>File Size:</strong> {metadata.file_size} bytes</p>
                    <p><strong>Last Modified:</strong> {metadata.last_modified}</p>
                    <p><strong>Row Count:</strong> {metadata.row_count}</p>
                    <p><strong>Columns:</strong></p>
                    <ul>
                        {metadata.columns.map((col) => (
                            <li key={col}>
                                {col} ({metadata.data_types[col]})
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Show error message if there is an error */}
            {error && (
                <div style={{ color: 'red' }}>
                    <p>Error: {error}</p>
                </div>
            )}
        </div>
    );
}
