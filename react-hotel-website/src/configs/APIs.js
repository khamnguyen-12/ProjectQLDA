import axios from "axios";
import moment from "moment";
import cookie from "react-cookies";

export const BASE_URL = 'http://192.168.1.233:8000/';

// export const formatNS= (dateString) => {
//     const [year, month, day] = dateString.split('-');
//     return `${day}/${month}/${year}`;
//   };


// export const formatDate = (date)=>{
//     return moment(date).format(' HH:mm - DD/MM/YYYY');
// };


export const endpoints = {

 'login': '/o/token/',
 'current-user': '/accounts/current-user/',
 'signin': '/accounts/',
 
}   


export const authAPI = () => {
    const token = cookie.load('token');
    return axios.create({
        baseURL: BASE_URL,
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
}

export default axios.create({
    baseURL: BASE_URL
});