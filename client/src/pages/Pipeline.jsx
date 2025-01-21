import React, { useState, useRef } from "react";
import { Stepper } from 'primereact/stepper';
import { StepperPanel } from 'primereact/stepperpanel';
import { Card } from 'primereact/card';
import Uploader from '../components/Uploader';
import MetaData from '../components/MetaData';
import '../styles/Pipeline.css';

export default function Pipeline() {
    const stepperRef = useRef(null);
    const [uploadedData, setUploadedData] = useState(null);

    const handleUploadSuccess = (data) => {
        setUploadedData(data);
        stepperRef.current.nextCallback();
    };

    return (
    <Card id="card">
        <Stepper ref={stepperRef}>
            <StepperPanel header="Choose Data">
                <Uploader onSuccess={handleUploadSuccess} />
            </StepperPanel>
            <StepperPanel header="Data Summary">
                <MetaData fileName={uploadedData} onSuccess={(result) => console.log('Metadata fetched: ', result)} />
            </StepperPanel>
            <StepperPanel header="Business Need">
                Business Need
            </StepperPanel>
            <StepperPanel header="Load Data">
                Load Data
            </StepperPanel>
        </Stepper>
    </Card>
    );
}