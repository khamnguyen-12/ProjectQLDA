import React, { useState, useReducer } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import Navbar from "./components/Navbar/Navbar";
import Footer from "./components/Footer/Footer";
import Login from "./components/Account/Login";
import Signup from './components/Account/Signup';
import MainContent from './components/MainContent/MainContent';
import Info from './components/Navbar/Info';
import MyUserReducer from './components/MyReducer/MyUserReducer';
import cookie from "react-cookies";
import { MyDispatchContext, MyUserContext } from './configs/MyContext';
import ManageBookings from './components/Staff/ManageBookings';
const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, cookie.load("user") || null);
  const [showMainContent, setShowMainContent] = useState(true);
  return (
    <BrowserRouter>
      <MyUserContext.Provider value={user}>
        <MyDispatchContext.Provider value={dispatch}>
          <Navbar />
          <Routes>
            <Route exact path='/' Component={MainContent} /> 
            <Route
              path='/login'
              element={
                <Login
                  setShowMainContent={setShowMainContent}
                />
              }
            />
            <Route path='/info' element={<Info />} />
            <Route path='/signup' element={<Signup />} />
            <Route path='/manage-bookings' element={<ManageBookings />} />
          </Routes>
          <Footer />
        </MyDispatchContext.Provider>
      </MyUserContext.Provider>
    </BrowserRouter>
  );
}

export default App;
