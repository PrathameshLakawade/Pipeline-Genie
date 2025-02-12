import React, { useRef, useState } from 'react';
import { FileUpload } from 'primereact/fileupload';
import { ProgressBar } from 'primereact/progressbar';
import { Button } from 'primereact/button';
import { Tooltip } from 'primereact/tooltip';
import { Tag } from 'primereact/tag';

export default function Uploader({ onSuccess }) {
    const [totalSize, setTotalSize] = useState(0);
    const [loading, setLoading] = useState(false);
    const fileUploadRef = useRef(null);

    // Function to select files
    const selectFiles = (e) => {
        let _totalSize = totalSize;
        let files = e.files;

        Object.keys(files).forEach((key) => {
            _totalSize += files[key].size || 0;
        });

        setTotalSize(_totalSize);
    };

    // Function to upload files
    const uploadFiles = async (e) => {
        setLoading(true);
        let _totalSize = 0;
    
        e.files.forEach((file) => {
            _totalSize += file.size || 0;
        });
    
        setTotalSize(_totalSize);
    
        try {
            const formData = new FormData();
            e.files.forEach((file) => {
                formData.append('files', file);
            });
    
            const response = await fetch('http://localhost:8000/extract/upload', {
                method: 'POST',
                body: formData,
            });
    
            if (response.ok) {
                const result = await response.json();
                clearSelection();
                if (onSuccess) onSuccess(result.id);
            }
        } catch (error) {
            console.error('Upload error:', error);
        } finally {
            setLoading(false);
        }
    };    

    // Function to remove selected files
    const removeFiles = (file, callback) => {
        setTotalSize(totalSize - file.size);
        callback();
    };

    // Function to clear selection
    const clearSelection = () => {
        setTotalSize(0);
    };

    // Function to display options
    const header = (options) => {
        const { className, chooseButton, uploadButton, cancelButton } = options;
        const formattedValue = fileUploadRef.current ? fileUploadRef.current.formatSize(totalSize) : '0 B';
    
        return (
            <div className={className} style={{ backgroundColor: 'transparent', display: 'flex', alignItems: 'center' }}>
                {chooseButton}
                {uploadButton}
                {cancelButton}
                <div className="flex align-items-center gap-3 ml-auto">
                    <span>{`${formattedValue} / 50 MB`}</span>
                    <ProgressBar value={(totalSize / 52428800) * 100} showValue={false} style={{ width: '10rem', height: '12px' }} />
                </div>
            </div>
        );
    };
    
    // Function to display uploaded files
    const items = (file, props) => {
        return (
            <div className="flex align-items-center flex-wrap">
                <div className="flex align-items-center" style={{ width: '40%' }}>
                    <span className="flex flex-column text-left ml-3">
                        {file.name}
                        <small>Uploaded on: {new Date().toLocaleDateString()}</small>
                    </span>
                </div>
                <Tag value={props.formatSize} severity="warning" className="px-3 py-2" />
                <Button type="button" icon="pi pi-times" className="p-button-outlined p-button-rounded p-button-danger ml-auto" onClick={() => removeFiles(file, props.onRemove)} />
            </div>
        );
    };

    // Function to display empty uploader
    const empty = () => {
        return (
            <div className="flex align-items-center flex-column">
                <i className="pi pi-file mt-3 p-5" style={{ fontSize: '5em', borderRadius: '50%', backgroundColor: 'var(--surface-b)', color: 'var(--surface-d)' }}></i>
                <span style={{ fontSize: '1.2em', color: 'var(--text-color-secondary)' }} className="my-5">
                    Choose or Drop CSV Files Here
                </span>
            </div>
        );
    };

    const chooseOptions = { icon: 'pi pi-fw pi-file', className: 'custom-choose-btn p-button-rounded p-button-outlined' };
    const uploadOptions = { icon: 'pi pi-fw pi-upload', className: 'custom-upload-btn p-button-success p-button-rounded p-button-outlined' };
    const cancelOptions = { icon: 'pi pi-fw pi-times', className: 'custom-cancel-btn p-button-danger p-button-rounded p-button-outlined' };

    return (
        <>
            {/* Options */}
            <Tooltip target=".custom-choose-btn" content="Choose" position="bottom" />
            <Tooltip target=".custom-upload-btn" content="Upload" position="bottom" />
            <Tooltip target=".custom-cancel-btn" content="Clear" position="bottom" />

            {/* File Uploader */}
            <FileUpload
                ref={fileUploadRef}
                name="files"
                url="http://localhost:8000/extract/upload"
                multiple
                accept=".csv"
                maxFileSize={52428800}
                customUpload
                uploadHandler={uploadFiles}
                onSelect={selectFiles}
                onError={clearSelection}
                onClear={clearSelection}
                headerTemplate={header}
                itemTemplate={items}
                emptyTemplate={empty}
                chooseOptions={chooseOptions}
                uploadOptions={uploadOptions}
                cancelOptions={cancelOptions}
            />

            {/* Loader */}
            {loading && (
                <>
                    <h3 className='mt-4'>Uploading File(s) and Initiating Schema Analysis Process</h3>
                    <ProgressBar className='mt-2' mode="indeterminate" style={{ height: '0.5rem' }} />
                </>
            )}
        </>
    );
}