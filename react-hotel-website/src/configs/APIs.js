import axios from "axios";
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
 'current_user': '/accounts/current_user/',
 'signup': '/accounts/',
 'list_reservations' : '/reservations/',
 'deactivate_reservation': (id) => `/reservations/${id}/deactivate/`, // Thêm hàm cho deactivate với tham số id
 'update_reservation': (id) => `/reservations/${id}/`, // Update reservation endpoint
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