import React, { Component } from 'react';
import { Button, Card, CardBody,Label, CardGroup, Col, CardFooter, Container, Input, InputGroup, InputGroupAddon, InputGroupText, Row } from 'reactstrap';
import './login.css';
import axios from 'axios';
import Env from '../../../enviorment';
import {unregister} from '../../../intercepter';
import logo from '../../../assets/img/brand/logo.jpg'
import cookie from 'react-cookies';
import DeepLinkDecorator from 'react-deep-link/lib/decorator';

import {
  AppHeaderDropdown,
  AppNavbarBrand,
  AppSidebarToggler,
  AppAside,
  AppBreadcrumb,
  AppFooter,
  AppHeader,
  AppSidebar,
  AppSidebarFooter,
  AppSidebarForm,
  AppSidebarHeader,
  AppSidebarMinimizer,
  AppSidebarNav,
} from '@coreui/react';

import DefaultHeader from './DefaultHeader';
import DefaultFooter from './DefaultFooter';

class Login extends Component {
  constructor (props) {
    super(props);
    this.state = {visible: false};
    this.state = {
      username: '',
      password: '',
      formErrors: {username: '', password: ''},
      usernameValid: false,
      passwordValid: false,
      formValid: false,
      succss:false,
      forgotEmail:''
    }
  }

  handleUserInput = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    this.setState({[name]: value},
                  () => { this.validateField(name, value) });
  }

  validateField(fieldName, value) {
    let fieldValidationErrors = this.state.formErrors;
    let usernameValid = this.state.usernameValid;
    let passwordValid = this.state.passwordValid;

    switch(fieldName) {
      case 'username':
        usernameValid = value.length >0;
        fieldValidationErrors.username = usernameValid ? '' : 'Please enter the username';
        break;
      case 'password':
        passwordValid = value.length >= 6;
        fieldValidationErrors.password = passwordValid ? '': 'Password should atleast 6 char long';
        break;
      default:
        break;
    }
    this.setState({formErrors: fieldValidationErrors,
                    usernameValid: usernameValid,
                    passwordValid: passwordValid
                  }, this.validateForm);
  }
  
  login(){
    var data = {username : this.state.username,password:this.state.password}
    axios.post(Env.Url+ 'login/',data)
      .then(response => {
        // cookie.save('token', response.data.access, { path: '/' })
        // cookie.save('type', response.data.type, { path: '/' })
        // cookie.save('user_id', response.data.user_id, { path: '/' })
        // cookie.save('username', response.data.username, { path: '/' })
        this.props.history.push('/image');
        window.location.reload()
      }).catch(err => {
        this.props.history.push('/image');
        
      })
  }

  validateForm() {
    this.setState({formValid: this.state.usernameValid && this.state.passwordValid});
  }

  errorClass(error) {
    return(error.length === 0 ? '' : 'has-error');
  }

render() {
    return (

      <div className="app">
        <AppHeader fixed>
          <DefaultHeader />
        </AppHeader>
        <div className="app flex-row align-items-center">
            <Container>
              <Row className="justify-content-center">
                <Col md="6">
                  <Card className="mx-5">
                    <CardBody className="p-3" style={{marginBottom :  '5%'}}>
                      <div style={{ display: 'flex', justifyContent: 'center', marginTop :  '5%'  }}>
                          <AppNavbarBrand
                              full={{src: logo,  width: 200, height: '100' }}                  
                            /> 
                      </div>
                      <p style={{ display: 'flex', justifyContent: 'center'}} className="text-muted">Sign in to your  account</p>
                      <InputGroup className="mb-3">
                        <InputGroupAddon addonType="prepend">
                          <InputGroupText>
                            <i className="icon-user"></i>
                          </InputGroupText>
                        </InputGroupAddon>
                        <Input type="text" name="username" value={this.state.username} onChange={this.handleUserInput}   size="4" placeholder="Username" />
                      </InputGroup>
                      <p className="onerror">{this.state.formErrors.username}</p>

                      <InputGroup className="mb-3">
                        <InputGroupAddon addonType="prepend">
                          <InputGroupText>
                            <i className="icon-lock"></i>
                          </InputGroupText>
                        </InputGroupAddon>
                        <Input type="password"  name="password" size="4" value={this.state.password} onChange={this.handleUserInput} placeholder="Password" />
                      </InputGroup>
                      <p className="onerror"> {this.state.formErrors.password}</p>
                      <Row>
                          <Col xs="6">
                          <Button color="tn-color" onClick={((e) => this.login())}   disabled={!this.state.formValid} className="btn btn-primary">Sign In</Button>
                          </Col>
                          <Col xs="6" className="text-right">
                            <a href="#" className="active">Forgot password?</a>
                          </Col>
                      </Row>

                    </CardBody>
                    {/* <CardFooter className="p-4">
                      <Row>
                        <Col xs="12" sm="6">
                          <Button className="btn-facebook" block><span>facebook</span></Button>
                        </Col>
                        <Col xs="12" sm="6">
                          <Button className="btn-twitter" block><span>twitter</span></Button>
                        </Col>
                      </Row>
                    </CardFooter> */}
                  </Card>
                </Col>
              </Row>
            </Container>
        </div>
        <AppFooter  >
              <DefaultFooter />
            </AppFooter> 
      </div>
 
    );
  }
}

export default Login;
