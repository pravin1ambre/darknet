import React, { Component } from 'react';
import { HashRouter, Route, Switch, BrowserRouter as Router,Redirect, Link } from 'react-router-dom';
import './App.css';
import cookie from 'react-cookies';
// Styles
// CoreUI Icons Set
import '@coreui/icons/css/coreui-icons.min.css';
// Import Flag Icons Set
import 'flag-icon-css/css/flag-icon.min.css';
// Import Font Awesome Icons Set
import 'font-awesome/css/font-awesome.min.css';
// Import Simple Line Icons Set
import 'simple-line-icons/css/simple-line-icons.css';
// Import Main styles for this application
import './scss/style.css';
import axios from 'axios';

// Containers
import { DefaultLayout } from './containers';
// Pages
import { Page404, Page500 } from './views/Pages';
import { Login, Register } from './views/Auth';


const fakeAuth = {
  isAuthenticated: false,
  authenticate(cb){
    this.isAuthenticated = true
    setTimeout(cb, 100)
  },
  signout(cb){
    this.isAuthenticated = false
    setTimeout(cb, 100)
  }
}

const PrivateRoute = ({ component:Component, ...rest}) =>(
  <Route {...rest} render={(props)=>(
    fakeAuth.isAuthenticated === true 
      ? <Component {...props} />
      : <Redirect to =  '/login' />
  )}/>
)

// import { renderRoutes } from 'react-router-config';
// axios.defaults.headers.common['Authorization'] = 'Bearer ' + cookie.load("token");

class App extends Component {
  render() {
    return (
      <HashRouter>
        <Switch>
          <Route exact path="/login" name="Login Page" component={Login} />
          <Route exact path="/register" name="Register Page" component={Register} />
          <Route exact path="/404" name="Page 404" component={Page404} />
          <Route exact path="/500" name="Page 500" component={Page500} />
          <Route path="/" name="Home" component={DefaultLayout} />
          <PrivateRoute path='/register' component={Register}/>
        </Switch>
      </HashRouter>
    );
  }
}

export default App;
