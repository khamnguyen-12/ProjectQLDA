import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// import Navbar from "./components/Navbar/Navbar";
// import Hero from "./components/Hero/Hero";
// import JoinUs from "./components/JoinUs/JoinUs";
// import Features from "./components/Features/Features";
// import Sale from "./components/Sale/Sale";
// import Pricing from "./components/Pricing/Pricing";
// import Gallery from "./components/Gallery/Gallery";
// import Trainers from "./components/Trainers/Trainers";
// import Summer from "./components/Summer/Summer";
// import Footer from "./components/Footer/Footer";

import Login from "./components/Account/Login";
import SignUp from './components/Account/Signin';
import SignIn from './components/Account/Signin';
// import Signup from "./components/Account/Signup"


const App = () => {
  return (
    // <div className="App">
    //   <Navbar />
    //   <Hero />
    //   <JoinUs />
    //   <Features />
    //   <Sale />
    //   <Pricing />
    //   <Gallery />
    //   <Trainers />
    //   <Summer />
    //   <Footer />

    <BrowserRouter>
      <Routes>
        {/* <Route path='/' element = {<Home />}></Route> */}
        <Route path='/login' element = {<Login />}></Route>
        <Route path='/signin' element = {<SignIn />}></Route>

      </Routes>
    </BrowserRouter>

    // </div>
  );
}

export default App;
