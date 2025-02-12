import React, { useState, useEffect } from "react";
import { Skeleton } from "primereact/skeleton";
import { Divider } from "primereact/divider";
import { Dropdown } from "primereact/dropdown";
import { Button } from "primereact/button";

export default function BusinessNeed({ id, onSuccess }) {
    const [metadata, setMetadata] = useState(null);
    const [response, setResponse] = useState(null);
    const [selectedBusinessNeed, setSelectedBusinessNeed] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitLoading, setSubmitLoading] = useState(false);

    useEffect(() => {
        async function handleTransform() {
            setError(null);
            try {
                const response = await fetch(`http://localhost:8000/transform/clean/${id}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setMetadata(data.metadata);
                    setResponse(data.response);
                    if (onSuccess) {
                        onSuccess(data);
                    }
                } else {
                    const errorMessage = await response.text();
                    setError(errorMessage || "An error occurred.");
                }
            } catch (err) {
                console.error("Fetch error:", err);
                setError("Failed to fetch transformed data.");
            } finally {
                setLoading(false);
            }
        }

        if (id) {
            handleTransform();
        }
    }, [id, onSuccess]);

    // Function to send the selected business need to the FastAPI backend
    const sendBusinessNeedToBackend = async () => {
        if (!selectedBusinessNeed) {
            alert("Please select a business need before submitting.");
            return;
        }

        setSubmitLoading(true);
        try {
            const response = await fetch("http://localhost:8000/transform/process-business-need", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    id: id,
                    business_need: selectedBusinessNeed.need,
                    transformations: selectedBusinessNeed.transformations,
                }),
            });

            if (response.ok) {
                alert("Business need sent successfully!");
            } else {
                const errorMessage = await response.text();
                alert(`Error: ${errorMessage}`);
            }
        } catch (err) {
            console.error("Submission error:", err);
            alert("Failed to submit business need.");
        } finally {
            setSubmitLoading(false);
        }
    };

    return (
        <div>
            {loading && !error && (
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
                    <p><strong>File Size:</strong> {(metadata.size / 1000000).toFixed(2)} MBs</p>
                    <p><strong>Last Modified:</strong> {new Date(metadata.last_modified).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}</p>
                    <p><strong>Row Count:</strong> {metadata.rows.toLocaleString()}</p>

                    <Divider />

                    <h2>Suggestions for Business Needs</h2>
                    <Dropdown
                        value={selectedBusinessNeed}
                        onChange={(e) => setSelectedBusinessNeed(e.value)}
                        options={response.business_needs}
                        optionLabel="need"
                        showClear
                        placeholder="Select a Business Need"
                    />

                    <Button 
                        label={submitLoading ? "Submitting..." : "Submit"} 
                        icon="pi pi-check" 
                        className="p-mt-2" 
                        onClick={sendBusinessNeedToBackend} 
                        disabled={!selectedBusinessNeed || submitLoading} 
                    />
                </div>
            )}

            {!loading && error && (
                <div style={{ color: "red" }}>
                    <p>Error: {error}</p>
                </div>
            )}
        </div>
    );
}
