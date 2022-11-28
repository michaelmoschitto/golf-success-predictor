import { Button, Container, Grid, Input, InputLabel, MenuItem, Select, OutlinedInput, TextField } from "@mui/material";
import axios from "axios";
import React from "react";
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import { SelectChangeEvent } from '@mui/material/Select';
import { eventWrapper } from "@testing-library/user-event/dist/utils";

// {
//     "id" : [Integer],
//     "data" :{
//         "Average Score": [Float],
//         "Average SG Total": [Float],
//         "Points": [Float]
//     },
//     "scaler": ["MinMax", "Standard", "None"]
//     "model": [Model name from *models/ folder, omit .pkl file extension],
// }
export const Golf = () => {
    const id = 0;
    const [input, setInput] = React.useState({
        "id": id,
        "data": {
            "Average Score": 0,
            "Average SG Total": 0,
            "Points": 0,
        },
        "scaler": "MinMax",
        "model": "SVM"
    });

    const [result, setResult] = React.useState("")
    const [load, setLoad] = React.useState(false)

    const handleInput = (event) => {
        let data = input?.data
        let value = parseFloat(event.target.value) || 0
        data[event.target.id] = value

        setInput({
            "id": input.id,
            "data": data,
            "scaler": input.scaler,
            "model": input.model
        })
        console.log(input)
    }

    const handleScalar = (event) => {
        setInput({
            "id": input.id,
            "data": input.data,
            "scaler": event.target.value,
            "model": input.model
        })
        console.log(input)
    }

    const handleModel = (event) => {
        setInput({
            "id": input.id,
            "data": input.data,
            "scaler": input.scaler,
            "model": event.target.value
        })
        console.log(input)
    }

    const sendData = () => {
        console.log("Here")
        axios.post("http://127.0.0.1:8080/api/predictPGASuccess", input).then((result) => {
            let prediction = result.data.prediction
            prediction.replace("[", "").replace("]", "")
            prediction = parseFloat(prediction)
            prediction = Math.round(prediction)
            console.log(prediction)
            setResult(prediction)
            setLoad(true)
        }).catch((err) => {
            console.error(err)
            setLoad(true)
        })
    }

    return (
        <div>
            <h1>Predict your golf position</h1>
            <Grid container spacing={2}>
                <Grid item xs={4}>
                    <TextField label="Average Score" type="number" id="Average Score" onChange={handleInput}></TextField>
                </Grid>
                <Grid item xs={4}>
                    <TextField label="Average SG Total" type="number" id="Average SG Total" onChange={handleInput}></TextField>
                </Grid>
                <Grid item xs={4}>
                    <TextField label="Points" type="number" id="Points" onChange={handleInput}></TextField>
                </Grid>
                <Grid item xs={12}>
                    <FormControl variant="outlined" fullWidth>
                        <InputLabel id="demo-simple-select-label">Scaler</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={input.scaler}
                            label="Scaler"
                            onChange={handleScalar}
                        >
                            <MenuItem value={"MinMax"}>MinMax</MenuItem>
                            <MenuItem value={"Standard"}>Standard</MenuItem>
                            <MenuItem value={"None"}>None</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12}>
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Model</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={input.model}
                            label="Model"
                            onChange={handleModel}
                        >
                            <MenuItem value={"DecisionTree"}>Decision Tree</MenuItem>
                            <MenuItem value={"LinearRegressor"}>Linear Regression</MenuItem>
                            <MenuItem value={"NN"}>Neural Network</MenuItem>
                            <MenuItem value={"RidgeRegressor"}>Ridge Regression</MenuItem>
                            <MenuItem value={"SVM"}>SVM</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12}>
                    <Button variant="outlined" onClick={sendData}>Submit</Button>
                </Grid>
                <Grid item xs={12}>
                    {load ? <h1>Your predicted position: {result}</h1> : <div></div>}
                </Grid>
            </Grid>
        </div>
    );
};