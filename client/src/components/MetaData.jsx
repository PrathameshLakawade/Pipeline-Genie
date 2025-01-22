import React, { useEffect, useRef, useState } from 'react';
import { Toast } from 'primereact/toast';
import { Skeleton } from 'primereact/skeleton';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Divider } from 'primereact/divider';

export default function MetaData({ fileName, onSuccess }) {
    const toast = useRef(null);
    const [metadata, setMetadata] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

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
                    if (onSuccess) onSuccess(result.file_name);
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
            } finally {
                setLoading(false);
            }
        }

        if (fileName) {
            fetchMetaData();
        }
    }, [fileName, onSuccess]);

    const transformDataTypes = () => {
        if (!metadata || !metadata.data_types) return [];
        return Object.entries(metadata.data_types).map(([key, value]) => ({
            column: key,
            dataType: value,
        }));
    };

    const renderSkeletonRows = () => {
        return Array.from({ length: 5 }).map((_, i) => ({
            column: <Skeleton width="10rem" key={`column-${i}`} />,
            dataType: <Skeleton width="8rem" key={`datatype-${i}`} />,
        }));
    };

    return (
        <div>
            <Toast ref={toast} />

            {loading && !error && (
                <div>
                    <h2>Metadata</h2>
                    <Skeleton width="15rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />
                    <Skeleton width="12rem" height="1rem" className="mb-2" />
                    <Divider />
                    <h2>Schema</h2>
                    <DataTable value={renderSkeletonRows()} showGridlines>
                        <Column field="column" header="Column Name" />
                        <Column field="dataType" header="Data Type" />
                    </DataTable>
                </div>
            )}

            {!loading && metadata && (
                <div>
                    <h2>Metadata</h2>
                    <p><strong>File Size:</strong> {metadata.file_size / 1000000} MBs</p>
                    <p><strong>Last Modified:</strong> {metadata.last_modified}</p>
                    <p><strong>Row Count:</strong> {metadata.row_count}</p>
                    <Divider />
                    <h2>Schema</h2>
                    <DataTable value={transformDataTypes()} size='small' showGridlines>
                        <Column field="column" header="Column Name" />
                        <Column field="dataType" header="Data Type" />
                    </DataTable>
                </div>
            )}

            {error && (
                <div style={{ color: 'red' }}>
                    <p>Error: {error}</p>
                </div>
            )}
        </div>
    );
}
