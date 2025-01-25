import React, { useState, useEffect } from 'react';
import { Skeleton } from 'primereact/skeleton';
import { Divider } from 'primereact/divider';

export default function BusinessNeed({ id, onSuccess }) {
    const [metadata, setMetadata] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        async function handleTransform() {
            setLoading(true);
            setError(null);

            try {
                const response = await fetch(`http://localhost:8000/transform/clean/${id}`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setMetadata(data.metadata);
                    if (onSuccess) {
                        onSuccess(data);
                    }
                } else {
                    const errorMessage = await response.text();
                    setError(errorMessage || 'An error occurred.');
                }
            } catch (err) {
                console.error('Fetch error:', err);
                setError('Failed to fetch transformed data.');
            } finally {
                setLoading(false);
            }
        }

        if (id) {
            handleTransform();
        }
    }, [id, onSuccess]);

    return (
        <div>
            {loading && (
                <div>
                    <h2>Details</h2>
                    <Skeleton width="15rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />
                    <Skeleton width="10rem" height="1rem" className="mb-2" />

                    <Divider />

                    <h2>Suggestions for Business Needs</h2>
                    <Skeleton width="20rem" height="1rem" className="mb-2" />
                    <Skeleton width="20rem" height="1rem" className="mb-2" />
                    <Skeleton width="20rem" height="1rem" className="mb-2" />
                </div>
            )}

            {!loading && metadata && (
                <div>
                    <h2>Details</h2>
                    <p><strong>Current Location:</strong> {metadata.s3_uri}</p>
                    <p><strong>File Size:</strong> {metadata.size / 1000000} MBs</p>
                    <p><strong>Last Modified:</strong> {metadata.last_modified}</p>
                    <p><strong>Row Count:</strong> {metadata.rows}</p>

                    <Divider />

                    <h2>Suggestions for Business Needs</h2>
                    <p>No Suggestions!</p>
                </div>
            )}

            {!loading && error && (
                <div style={{ color: 'red' }}>
                    <p>Error: {error}</p>
                </div>
            )}
        </div>
    );
}
