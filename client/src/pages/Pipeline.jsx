import React, { useState, useRef } from "react";
import { Stepper } from 'primereact/stepper';
import { StepperPanel } from 'primereact/stepperpanel';
import { Card } from 'primereact/card';
import { Avatar } from 'primereact/avatar';

import Uploader from '../components/Uploader';
import MetaData from '../components/MetaData';
import BusinessNeed from "../components/BusinessNeed";
import Genie from '../static/genie.png'

import '../styles/Pipeline.css';

export default function Pipeline() {
    const stepperRef = useRef(null);
    const [uploadedData, setUploadedData] = useState(null);

    // Function to increment the step
    const moveForward = (data) => {
        setUploadedData(data);
        stepperRef.current.nextCallback();
    };

    return (
        <>
            {/* Section for displaying avatar and name */}
            <div className="grid">
                <div className="col-1">
                    <Avatar image={Genie} size="large" shape="circle" />
                </div>
                <div className="col-4">
                    <h1>Pipeline Genie</h1>
                </div>
            </div>

            {/* Stepper for data-pipeline */}
            <Card id="card">
                <Stepper ref={stepperRef} readOnly={true}>
                    <StepperPanel header="Choose Data">
                        <Uploader onSuccess={moveForward} />
                    </StepperPanel>
                    <StepperPanel header="Analyze Schema">
                        <MetaData id={uploadedData} onSuccess={moveForward} />
                    </StepperPanel>
                    <StepperPanel header="Choose Business Need">
                        <BusinessNeed id={uploadedData} />
                    </StepperPanel>
                    <StepperPanel header="Load Data">
                        TODO: Add summary of data, button to download data
                    </StepperPanel>
                </Stepper>
            </Card>
        </>
    );
}