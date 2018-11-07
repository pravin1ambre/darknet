import React, { Component } from 'react';
import { Card, CardBody,CardHeader,  FormGroup, Button,
  Col, Input, Table,
  InputGroup,  Row } from 'reactstrap';
import axios from 'axios';
import Env from '../../enviorment';
import 'moment-timezone';
import Action from './Action'


class Cfg extends Component {
  constructor(props) {
    super();
    this.state = {
      records:[],
    }
    this.getRecords = this.getRecords.bind(this)
    this.getRecords()
  }
  
  getRecords(){
    axios.get(Env.Url+'configuration').then(res =>{
      console.log(res.data)
      this.setState({records : res.data})
    })
  }

  searchElement(evt) {
    if(evt.target.value == ''){
      this.getRecords()
    }else{
      axios.get(Env.Url+'search/'+evt.target.value).then(res =>{
        this.setState({records : res.data})
      })
    }
  }

  actiondata(data){
    this.action.initial_method(data)
  }

  render() {
    return (
      <div className="animated fadeIn">
      <Action onRef={ref => (this.action = ref)} />
        <Row>
              <Col>
                <Card>
                    <CardHeader>

                        <Row>
                          <Col xs="12" sm="7">
                                <i className="fa fa-align-justify"></i> Configuration
                          </Col>
                          <Col xs="12" sm="3">                      
                          <InputGroup>
                              <Input type="text" id="input1-group2" onChange={this.searchElement.bind(this)} className="search-color" name="input1-group2" placeholder="Search by name" />                        
                            </InputGroup>
                          </Col>
                        </Row>
                    </CardHeader>
                    <CardBody>
                      <Table hover bordered striped responsive size="sm">
                        <thead >
                        <tr>  
                          <th >Mac Address</th>
                          <th >Action</th>                                
                        </tr>
                        </thead>
                        <tbody>
                            {(this.state.records !=undefined && this.state.records.length >0) ? this.state.records.map((data, index) => (
                              <tr key={index}>
                                <td>{data.mac_address}</td>
                                <td > 
                                    <i className="fa fa-eye fa-lg mt-2"  onClick={ ((e) => this.actiondata(data))}></i>
                                </td>
                              </tr>
                            )): 'No records Found'}
                        </tbody>
                      </Table>                      
                    </CardBody>
                </Card>
              </Col>
          </Row>
      </div>
    );
  }
}

export default Cfg;
