import React, { Component } from 'react';
import { Button,Badge, Card, CardBody, CardFooter,CardHeader,Pagination, 
  Col, Container, Input, PaginationItem,PaginationLink, Table,FormGroup,Label,
  InputGroup, InputGroupAddon, InputGroupText, Row, Progress } from 'reactstrap';

// import Tables from '../../Components/Tables';
import axios from 'axios';
import Env from '../../../enviorment';
import Moment from 'react-moment';
import 'moment-timezone';
import cookie from 'react-cookies';
import SkyLight, {SkyLightStateless} from 'react-skylight';
import Showimage from './Showimage'

var data = {
  title  : 'Image list',
  fields : ['Objects','TimeStamp','Mac_Address','Image','Prediction Image','Thumbnail'],
  limits : [5,10,15,20,25,50,100,200]
}

class Image extends Component {
  constructor(props) {
    super();
    this.state = {
      records:'',skip:10,next:false,prev:false
    }
    this.getRecords = this.getRecords.bind(this)
    this.getRecords()
  }
  
  showImage(name,image){
    this.showimg.initial_method(name,image)
  }
  
  getRecords(evt=null){
    if(evt === 'prev'){
      this.state.skip = this.state.skip -10
    }
    if(evt === 'next'){
      this.state.skip = this.state.skip + 10
    }    
    axios.get(Env.Url+'images/'+this.state.skip).then(res =>{
      if(res.data.length>0){
        this.setState({records : res.data})
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

      // var data = []
      // for (var i in this.state.records){
      //   var name = (this.state.records[i].name).toLowerCase()
      //   if (!name.search((evt.target.value).toLowerCase())){
      //     console.log(evt.target.value)
      //     data.push(this.state.records[i])
      //   }
      // } 
      // this.setState({records : data})
    }
  }

  
  render() {
    return (
      <div className="animated fadeIn">
      <Showimage onRef={ref => (this.showimg = ref)} />
        <Row>
              <Col>
                <Card>
                    <CardHeader>

                        <Row>
                          <Col xs="12" sm="7">
                                <i className="fa fa-align-justify"></i> {data.title}
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
                        <tr >            
                            {data.fields.length > 0 && data.fields.map((field, index) => (
                                <th key={index}>{field}</th>
                            ))}
                        </tr>
                        </thead>
                        <tbody>
                            {(this.state.records !=undefined && this.state.records.length >0) ? this.state.records.map((data, index) => (
                                <tr key={index}>
                                <td>{data.objects != undefined && Object.keys(data.objects).map(function(key,index) {
                                        return <div>  {key} : {data.objects[key]} {data.objects.length} {index <(data.objects.length) && <hr /> }  </div>  
                                    })}
                                </td>
                                <td>{data.timestamp}</td>
                                <td>{data.mac_address}</td>
                                  <td > 
                                        <i className="fa fa-image fa-lg mt-2"  onClick={ ((e) => this.showImage(data.name,data.source))}></i>
                                  </td>
                                  <td > 
                                        <i className="fa fa-image fa-lg mt-2"  onClick={ ((e) => this.showImage(data.name,data.prediction_image))}></i>
                                  </td>
                                  <td > 
                                        <i className="fa fa-image fa-lg mt-2"  onClick={ ((e) => this.showImage(data.name,data.thumbnail))}></i>
                                  </td>
                                </tr>
                            )): 'No records Found'}
                        </tbody>
                      </Table>
                      
                      <nav>
                        <Row>

                          <Col xs='12'  sm='8'>
                            <Pagination>
                              <PaginationItem onClick={ ((e) => this.getRecords('prev'))} disabled={this.state.prev}><PaginationLink previous tag="button">Prev</PaginationLink></PaginationItem>
                              <PaginationItem  onClick={ ((e) => this.getRecords('next'))}  disabled={this.state.next}><PaginationLink next tag="button">Next</PaginationLink></PaginationItem>                              
                            </Pagination>
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

export default Image;
