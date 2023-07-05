import React, { useState } from "react";
import { Container, Button, Header, Table, Segment } from 'semantic-ui-react';
import Papa from 'papaparse';
import './PredictForm.css'; 

const PredictForm = () => {
    const [file, setFile] = useState(null);
    const [data, setData] = useState([]);
    const [predictions, setPredictions] = useState([]);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        Papa.parse(file, {
            header: true,
            complete: async (results) => {
                setData(results.data); // Store the data
                const response = await fetch('http://localhost:5000/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(results.data),
                });

                const result = await response.json();
                setPredictions(result.predictions);
            }
        });
    };

    return (
        <Container className="predict-form-container"> 
            <Segment padded="very" className="segment-border">
                <Header as='h2' textAlign='center'>Stock Prediction</Header>
                <form onSubmit={handleSubmit} style={{marginTop:"5%", marginBottom:"5%"}}>
                    <input type='file' accept='.csv' onChange={handleFileChange}/>
                    <Button type='submit' fluid style={{marginTop:"10%", background:"rgb(150,75,0)", color:"white"}}> Predict </Button>
                </form>
            </Segment>
            {predictions.length > 0 && (
                <Container className="table-container">
                    <Segment className="segment-border">
                        <Table celled>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell>Date</Table.HeaderCell>
                                    <Table.HeaderCell>Prediction</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>

                            <Table.Body>
                                {predictions.map((prediction, index) => (
                                    <Table.Row key={index}>
                                        <Table.Cell>{data[index]['Date']}</Table.Cell>
                                        <Table.Cell>{prediction}</Table.Cell>
                                    </Table.Row>
                                ))}
                            </Table.Body>
                        </Table>
                    </Segment>
                </Container>
            )}
        </Container>
    );
};

export default PredictForm;
