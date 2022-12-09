import axios, { Axios } from 'axios';

export const Http: Axios = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL!,
});
