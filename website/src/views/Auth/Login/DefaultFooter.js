import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, Form, Card, CardBody, Label, CardGroup, Col, Container, Input, InputGroup, CardFooter, InputGroupAddon, InputGroupText, Row } from 'reactstrap';


const propTypes = {
  children: PropTypes.node,
};

const defaultProps = {};

class DefaultFooter extends Component {
  render() {

    // eslint-disable-next-line
    const { children, ...attributes } = this.props;

    return (
      <React.Fragment >
        <style>
          {
            `.app-footer {
                  background: #eceff1;
                  margin-top: -4%;
                  margin-left: 0px !important; 
              }`
          }
        </style>
        
        <Row className="col-12" style={{ 'color': 'black' }}>
                 &copy;  2018.
          
        </Row>
      </React.Fragment>
    );
  }
}

DefaultFooter.propTypes = propTypes;
DefaultFooter.defaultProps = defaultProps;

export default DefaultFooter;