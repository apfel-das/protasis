import axios from 'axios';
export const BASE_URL = process.env.REACT_APP_BASE_URL;
export const BASE_PORT = process.env.REACT_APP_BASE_PORT;

const client = axios.create({
    baseURL: BASE_URL+':'+BASE_PORT,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS'
    }
});



export default client;