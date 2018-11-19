import React, { Component } from 'react';
import { Button,Badge, Card, CardBody, CardFooter,CardHeader,Pagination, 
  Col, Container, Input, PaginationItem,PaginationLink, Table,FormGroup,Label,
  InputGroup, InputGroupAddon, InputGroupText, Row, Progress } from 'reactstrap';
import axios from 'axios';
import Env from '../../enviorment';
import 'moment-timezone';
import Action from './Action'


class Cfg extends Component {
  constructor(props) {
    super();
    this.state = {
      records:'',skip:0,next:false,prev:false
    }
    this.getRecords = this.getRecords.bind(this)
    this.getRecords()
  }
  
  getRecords(evt=null){
    if(evt === 'prev'){
      this.state.skip = this.state.skip -10
    }
    if(evt === 'next'){
      this.state.skip = this.state.skip + 10
    }    
    axios.get(Env.Url+'configuration/'+this.state.skip).then(res =>{
      if(res.data.data.length>0){
        this.setState({records : res.data.data})
        this.setState({count : res.data.count})
        this.setState({pages : res.data.pages})
        this.setState({current_page : res.data.current_page})
      }
      
    }).catch(error => {
      this.state.skip =10
  });

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
                      <nav>
                        <Row>

                          <Col xs='12'  sm='2'>
                            <Pagination>
                              <PaginationItem onClick={ ((e) => this.getRecords('prev'))} disabled={this.state.prev}><PaginationLink previous tag="button">Prev</PaginationLink></PaginationItem>
                              <PaginationItem  onClick={ ((e) => this.getRecords('next'))}  disabled={this.state.next}><PaginationLink next tag="button">Next</PaginationLink></PaginationItem>                              
                            </Pagination>
                          </Col>
                          <Col xs="12" sm="2">
                                    count : {this.state.count}
                          </Col>
                          <Col xs="12" sm="2">
                                    pages : {this.state.pages}
                          </Col>
                          <Col xs="12" sm="2">
                                    current_page : {this.state.current_page}
                          </Col>
                        </Row>
                      </nav>

                    </CardBody>
                </Card>
              </Col>
          </Row>
      </div>
    );
  }
}

export default Cfg;
