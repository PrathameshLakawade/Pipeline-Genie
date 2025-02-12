import React, { useEffect, useState } from 'react';
import { Skeleton } from 'primereact/skeleton';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Divider } from 'primereact/divider';
import { Button } from 'primereact/button';

export default function MetaData({ id, onSuccess }) {
    const [metadata, setMetadata] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Function to fetch file details
        async function fetchMetaData() {
            try {
                const response = await fetch(`http://localhost:8000/extract/metadata/${id}`, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const result = await response.json();
                    setMetadata(result.metadata);
                } else {
                    const errorMessage = await response.text();
                    setError(errorMessage);
                }
            } catch (error) {
                console.error('Fetch error:', error);
                setError('An error occurred while fetching metadata');
            } finally {
                setLoading(false);
            }
        }

        if (id) {
            fetchMetaData();
        }
    }, [id, onSuccess]);

    // Function to map columns and their data types
    const transformDataTypes = () => {
        if (!metadata || !metadata.data_types) return [];
        return Object.entries(metadata.data_types).map(([key, value]) => ({
            column: key,
            dataType: value,
        }));
    };

    // Function to render mock rows
    const renderSkeletonRows = () => {
        return Array.from({ length: 5 }).map((_, i) => ({
            column: <Skeleton width="10rem" key={`column-${i}`} />,
            dataType: <Skeleton width="8rem" key={`datatype-${i}`} />,
        }));
    };

    return (
        <>
            {loading && !error && (
                <div>
                    {/* Data Details */}
                    <h2>Details</h2>
                    <Skeleton width="15rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />

                    <Divider />

                    {/* Data Schema */}
                    <h2>Schema</h2>
                    <DataTable value={renderSkeletonRows()} size='small' showGridlines>
                        <Column field="column" header="Column Name(s)" />
                        <Column field="dataType" header="Data Type(s)" />
                    </DataTable>
                </div>
            )}

            {!loading && metadata && (
                <div>
                    {/* Data Details */}
                    <h2>Details</h2>
                    <p><strong>Upload Location:</strong> {metadata.s3_uri}</p>
                    <p><strong>File Size:</strong> {(metadata.size / 1000000).toFixed(2)} MBs</p>
                    <p><strong>Last Modified:</strong> {new Date(metadata.last_modified).toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' })}</p>
                    <p><strong>Row Count:</strong> {metadata.rows.toLocaleString()}</p>

                    <Divider />

                    {/* Data Schema */}
                    <h2>Schema</h2>
                    <DataTable value={transformDataTypes()} size='small' showGridlines>
                        <Column field="column" header="Column Name(s)" />
                        <Column field="dataType" header="Data Type(s)" />
                    </DataTable>

                    <h3 className='mt-4'>Verify the Details and Schema of the Uploaded File(s) and Provide a Confirmation to Initiate Data Cleaning</h3>
                    <Button onClick={() => onSuccess(id)} label="Confirm" severity="secondary" rounded />
                </div>
            )}

            {error && (
                <div style={{ color: 'red' }}>
                    <p>Error: {error}</p>
                </div>
            )}
        </>
    );
}
